"""Checks on the first recovered reference geometry and its CAD export."""
import csv
import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reference_geometry', ROOT / 'scripts/export_reference_geometry.py')
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


class ReferenceGeometryTests(unittest.TestCase):
    def test_local_frame_on_rotated_chord(self):
        self.assertEqual(geometry.local_point((4, 3), (4, 3), (1, 7), 10), (0, 0))
        self.assertEqual(geometry.local_point((1, 7), (4, 3), (1, 7), 10), (10, 0))
        self.assertEqual(geometry.local_point((0, 0), (4, 3), (1, 7), 10), (0, 10))

    def test_published_stations_and_recovered_polygon(self):
        record, stations, rows, points = geometry.extract()
        tip = float(stations[-1]['radius_mm'])
        radii = [float(r['radius_mm']) for r in stations]
        self.assertEqual(radii, sorted(set(radii)))
        for row in stations:
            self.assertLessEqual(abs(float(row['radius_mm']) / tip - float(row['r_over_rtip_printed'])), 0.005)
        self.assertEqual(points[0][:3], points[-1][:3])
        self.assertEqual(points[0], (0, 0, 0, 0, 0, 0, 0))
        te = next(i for i, r in enumerate(rows) if r['surface'] == 'trailing_edge')
        self.assertAlmostEqual(points[te][0], float(stations[-1]['chord_mm']))
        self.assertAlmostEqual(points[te][1], 0)
        # Image-upper contour must lie above image-lower contour in the declared frame.
        self.assertGreater(sum(p[1] for p in points[1:te]) / (te - 1),
                           sum(p[1] for p in points[te+1:-1]) / (len(points) - te - 2))
        for x, y, z, xmin, xmax, ymin, ymax in points:
            self.assertTrue(all(math.isfinite(v) for v in (x, y, z, xmin, xmax, ymin, ymax)))
            self.assertLessEqual(xmin, x)
            self.assertLessEqual(x, xmax)
            self.assertLessEqual(ymin, y)
            self.assertLessEqual(y, ymax)
        # Check for crossings between non-adjacent polyline segments.
        def cross(a, b, c):
            return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
        segments = list(zip(points, points[1:]))
        for i, (a, b) in enumerate(segments):
            self.assertNotEqual(a[:2], b[:2])
            for j in range(i+2, len(segments)):
                if i == 0 and j == len(segments)-1:
                    continue
                c, d = segments[j]
                self.assertFalse(cross(a,b,c)*cross(a,b,d) < 0 and cross(c,d,a)*cross(c,d,b) < 0)

    def test_export_preserves_conflicts_and_units(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            audit = geometry.export(out)
            q = json.loads((geometry.SOURCE / 'geometry.json').read_text())['read']
            tip = float(geometry.read_csv('blade-stations.csv')[-1]['radius_mm'])
            expected_gap = 25.4*q['shroud_inner_radius']['value']-tip
            self.assertAlmostEqual(audit['radial_gap_from_printed_radii_mm'], expected_gap)
            self.assertNotEqual(audit['clearance_from_printed_radii_percent_height'], audit['clearance_label_percent_height'])
            self.assertNotEqual(audit['tip_thickness_inch_converted_mm'], audit['tip_thickness_metric_mm'])
            self.assertEqual(audit['status'], 'partial_geometry')
            with (out / 'tip-section-mm.csv').open() as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), audit['point_count_including_closure'])
            self.assertEqual(len((out / 'tip-section-mm.txt').read_text().splitlines()), len(rows))
            self.assertEqual(json.loads((out / 'geometry-audit.json').read_text()), audit)


if __name__ == '__main__':
    unittest.main()
