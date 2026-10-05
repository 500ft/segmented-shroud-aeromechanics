#!/usr/bin/env python3
"""Reproduce the geometry comparison on the reused Akturk-Camci inputs."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import tempfile

from export_reference_geometry import SOURCE, export, read_csv

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence/task-reference-feasibility-2026-10-04'


def calculate():
    geometry = json.loads((SOURCE / 'geometry.json').read_text())
    reference = json.loads((EVIDENCE / 'reference.json').read_text())
    stations = read_csv('blade-stations.csv')
    pixels = read_csv('tip-trace-pixels.csv')
    q = {k: v['value'] for k, v in geometry['read'].items() if 'value' in v}
    tip = float(stations[-1]['radius_mm'])
    hub = q['hub_radius']
    casing = q['shroud_inner_radius'] * 25.4
    with tempfile.TemporaryDirectory() as folder:
        export(Path(folder))
        with (Path(folder) / 'tip-section-mm.csv').open() as stream:
            curve = list(csv.DictReader(stream))
        export_matches = {
            name: hashlib.sha256((Path(folder) / name).read_bytes()).hexdigest() == digest
            for name, digest in reference['preservation']['export_sha256'].items()
        }
    assert all(export_matches.values()), 'Reused export differs from preservation snapshot'
    # Independent construction using a unit chord vector and its normal.
    le = [float(pixels[0][k]) for k in ('image_x_px', 'image_y_px')]
    te_row = next(p for p in pixels if p['surface'] == 'trailing_edge')
    te = [float(te_row[k]) for k in ('image_x_px', 'image_y_px')]
    length = math.dist(le, te)
    ex, ey = [(te[i]-le[i])/length for i in range(2)]
    scale = float(stations[-1]['chord_mm']) / length
    error = 0.0
    for p, c in zip(pixels, curve):
        dx, dy = float(p['image_x_px'])-le[0], float(p['image_y_px'])-le[1]
        xy = ((dx*ex+dy*ey)*scale, (-dx*ey+dy*ex)*scale)
        error = max(error, abs(xy[0]-float(c['x_mm'])), abs(xy[1]-float(c['y_mm'])))
    assert error <= 0.5e-6 + 1e-12, 'Transform differs beyond CSV output rounding'
    assert curve[0] == curve[-1], 'Tip polyline is not closed'
    # Half-last-digit ranges are an arithmetic sensitivity, not experimental uncertainty.
    casing_half_mm, radius_half_mm = 0.005*25.4, 0.05
    clearance_range = [
        100*((casing-casing_half_mm)-(tip+radius_half_mm))/((tip+radius_half_mm)-(hub-radius_half_mm)),
        100*((casing+casing_half_mm)-(tip-radius_half_mm))/((tip-radius_half_mm)-(hub+radius_half_mm)),
    ]
    label = q['clearance_labels'][0]
    case_speeds = sorted(set([reference['reference_conditions']['pressure_profile_rpm'],
                             reference['reference_conditions']['thrust_coefficient_marker_rpm'][-1],
                             q['nominal_speed']]))
    return {
        'verdict': reference['feasibility']['verdict'],
        'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [SOURCE/'geometry.json', SOURCE/'blade-stations.csv',
                                   SOURCE/'tip-trace-pixels.csv', EVIDENCE/'reference.json']},
        'station_count': len(stations),
        'trace_points_including_closure': len(pixels),
        'first_station_to_hub_unrecovered_span_mm': float(stations[0]['radius_mm'])-hub,
        'chord_pixel_length': length,
        'tip_scale_mm_per_pixel': scale,
        'independent_transform_max_error_mm': error,
        'preserved_exports_byte_identical': export_matches,
        'gap_from_printed_radii_mm': casing-tip,
        'clearance_from_printed_radii_percent_height': 100*(casing-tip)/(tip-hub),
        'clearance_label_difference_percentage_points': 100*(casing-tip)/(tip-hub)-label,
        'clearance_print_rounding_range_percent_height': clearance_range,
        'printed_label_within_rounding_range': clearance_range[0] <= label <= clearance_range[1],
        'rounding_note': 'Independent half-last-digit allowances on printed casing inches and rotor/hub millimetres; not manufacturing tolerances or a probability interval.',
        'tip_thickness_unit_disagreement_mm': q['tip_thickness_inch']*25.4-q['tip_thickness_metric'],
        'instrument_torque_accuracy_only_power_sensitivity': [
            {'rpm': rpm, 'omega_rad_s': 2*math.pi*rpm/60,
             'plus_minus_W_from_quoted_torque_accuracy':
                 2*math.pi*rpm/60*reference['uncertainty']['moment_xyz_accuracy_N_m']['plus_minus']}
            for rpm in case_speeds],
        'power_sensitivity_note': 'Omega times quoted torque accuracy with speed held exact. Full power uncertainty and its confidence remain unknown.',
        'solver_run': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculate()
    path = EVIDENCE / 'geometry-comparison.json'
    if args.check:
        assert json.loads(path.read_text()) == result, 'Geometry comparison is out of date'
        print('Geometry comparison reproduced: ' + result['verdict'])
    else:
        path.write_text(json.dumps(result, indent=2) + '\n')
        print(path.relative_to(ROOT))
