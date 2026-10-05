#!/usr/bin/env python3
"""Export the recovered Akturk-Camci tip curve; no complete rotor or duct is implied."""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/reference/akturk-camci'


def read_csv(name):
    with (SOURCE / name).open(newline='') as stream:
        return list(csv.DictReader(stream))


def local_point(point, leading, trailing, chord):
    dx, dy = trailing[0] - leading[0], trailing[1] - leading[1]
    length_squared = dx * dx + dy * dy
    px, py = point[0] - leading[0], point[1] - leading[1]
    return (chord * (px * dx + py * dy) / length_squared,
            chord * (py * dx - px * dy) / length_squared)


def extract():
    record = json.loads((SOURCE / 'geometry.json').read_text())
    stations = read_csv(record['blade_stations']['file'])
    rows = read_csv(record['digitised_tip']['file'])
    pixels = [(float(r['image_x_px']), float(r['image_y_px'])) for r in rows]
    leading = pixels[0]
    trailing = pixels[next(i for i, r in enumerate(rows) if r['surface'] == 'trailing_edge')]
    chord = float(stations[-1]['chord_mm'])
    allowances = record['digitised_tip']['chosen_extraction_allowances']
    pixel_delta = allowances['pixel_coordinate_half_width_px']
    chord_delta = allowances['chord_rounding_half_width_mm']
    points = []
    for point in pixels:
        xy = local_point(point, leading, trailing, chord)
        # Sample corners of the declared input ranges. This is a sensitivity
        # envelope, not a confidence interval or a bound on drawing fidelity.
        samples = []
        for signs in itertools.product((-1, 1), repeat=7):
            perturbed_le = tuple(leading[i] + signs[i+2]*pixel_delta for i in range(2))
            perturbed_te = tuple(trailing[i] + signs[i+4]*pixel_delta for i in range(2))
            perturbed_point = tuple(point[i] + signs[i]*pixel_delta for i in range(2))
            if point == leading:
                perturbed_point = perturbed_le
            elif point == trailing:
                perturbed_point = perturbed_te
            samples.append(local_point(perturbed_point, perturbed_le, perturbed_te,
                                       chord + signs[6]*chord_delta))
        points.append((*xy, 0.0, min(p[0] for p in samples), max(p[0] for p in samples),
                       min(p[1] for p in samples), max(p[1] for p in samples)))
    return record, stations, rows, points


def export(destination):
    record, stations, rows, points = extract()
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / 'tip-section-mm.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['surface', 'x_mm', 'y_mm', 'z_mm', 'x_corner_min_mm',
                         'x_corner_max_mm', 'y_corner_min_mm', 'y_corner_max_mm'])
        writer.writerows([r['surface'], *(f'{x:.6f}' for x in p)] for r, p in zip(rows, points))
    # Plain XYZ millimetres for a CAD curve import with explicitly selected units.
    (destination / 'tip-section-mm.txt').write_text(''.join(
        f'{p[0]:.6f}\t{p[1]:.6f}\t{p[2]:.6f}\n' for p in points))
    q = {key: item['value'] for key, item in record['read'].items() if 'value' in item}
    tip_radius = float(stations[-1]['radius_mm'])
    shroud_mm = q['shroud_inner_radius'] * 25.4
    gap_mm = shroud_mm - tip_radius
    height_mm = tip_radius - q['hub_radius']
    audit = {
        'status': record['status'],
        'source': 'data/reference/akturk-camci/geometry.json',
        'shroud_inner_radius_mm': shroud_mm,
        'blade_height_mm': height_mm,
        'radial_gap_from_printed_radii_mm': gap_mm,
        'clearance_from_printed_radii_percent_height': 100 * gap_mm / height_mm,
        'clearance_label_percent_height': q['clearance_labels'][0],
        'tip_thickness_inch_converted_mm': q['tip_thickness_inch'] * 25.4,
        'tip_thickness_metric_mm': q['tip_thickness_metric'],
        'nominal_speed_rad_s': q['nominal_speed'] * 2 * math.pi / 60,
        'normalisation_diameter_m': 2 * shroud_mm / 1000,
        'point_count_including_closure': len(points),
        'coordinate_note': 'Six output decimals retain the transform; uncertainty is in the source record.',
        'cad_note': 'Partial tip curve only. Missing geometry and conflicts remain in the source record.',
    }
    (destination / 'geometry-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    polyline = ' '.join(f'{50 + 10*p[0]:.3f},{190 - 10*p[1]:.3f}' for p in points)
    dots = ''.join(f'<circle cx="{50+10*p[0]:.3f}" cy="{190-10*p[1]:.3f}" r="1.6"/>' for p in points)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="780" height="320" viewBox="0 0 780 320">
<rect width="780" height="320" fill="white"/>
<g font-family="sans-serif" fill="#152332"><text x="30" y="30" font-size="20">Digitised tip section: local chord frame, millimetres</text>
<text x="30" y="55" font-size="14">Partial geometry. No section stacking or complete duct profile recovered.</text>
<text x="40" y="215">LE</text><text x="675" y="215">TE</text>
<text x="30" y="280" font-size="13">Points follow Figure 2. Straight segments join picks; no airfoil fit or thickness correction.</text></g>
<line x1="50" y1="190" x2="{50+10*float(stations[-1]['chord_mm'])}" y2="190" stroke="#aaaaaa"/>
<polyline points="{polyline}" fill="none" stroke="#157b84" stroke-width="1.5"/>
<g fill="#152332">{dots}</g></svg>'''
    (destination / 'tip-section.svg').write_text(svg + '\n')
    return audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    print(json.dumps(export(parser.parse_args().output_dir), indent=2))
