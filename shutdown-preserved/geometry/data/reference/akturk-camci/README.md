# Akturk-Camci reference geometry

Nine blade stations and a 65-point closed tip outline have been recovered.
The [geometry record](geometry.json) holds the published duct dimensions,
source URLs and hashes, operating point, clearance definition, uncertainties
and missing geometry. Its status is `partial_geometry`.

## Files and use

- [blade-stations.csv](blade-stations.csv): Table 1 transcribed in its printed
  units. The dimensional radii take precedence over rounded radius ratios.
- [tip-trace-pixels.csv](tip-trace-pixels.csv): picks from the journal's isolated
  tip profile. Pixel origin, source image identifier, scale and selection
  allowances are in `digitised_tip` in the geometry record.
- [exporter](../../../scripts/export_reference_geometry.py): converts that
  trace to a local chord frame in millimetres. It also evaluates the recorded
  clearance and thickness discrepancies without correcting the source.

From the repository root:

```sh
python3 scripts/export_reference_geometry.py --output-dir results/generated/reference-geometry
python3 -m unittest discover -s tests -p test_reference_geometry.py -v
```

The output directory contains a closed XYZ curve (`tip-section-mm.txt`), a
CSV with coordinate sensitivity ranges, an SVG preview and
`geometry-audit.json` with unit conversions. Generated files have no separate
parameter inputs and stay outside version control. Select millimetres when
importing the XYZ curve into CAD. Preserve the local frame; a blade assembly
needs section placement data. A CAD spline through the picks would introduce
a further interpolation choice and should be checked against the polyline.

## Extraction and review

The author-hosted conference and journal copies were both inspected. Table 1
agrees across those copies. The journal Figure 2 embedded image was extracted
at native resolution with PyMuPDF, selected columns were inspected for dark
pixel runs, and points were chosen manually along the isolated contour.
The resulting trace was overlaid on the source figure and visually checked.
The exported outline was also rendered and inspected.

To repeat the image inspection, download the journal URL in `sources`, verify
its SHA-256, then extract the PDF image identified in `digitised_tip.image`.
For example, with PyMuPDF available in a temporary environment:

```python
import hashlib
import json
from pathlib import Path
import pymupdf

record = json.loads(Path('data/reference/akturk-camci/geometry.json').read_text())
pdf = Path('/path/to/downloaded-journal.pdf')
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == record['sources']['journal']['sha256']
with pymupdf.open(pdf) as document:
    source_image = document.extract_image(record['digitised_tip']['image']['pdf_xref'])
assert hashlib.sha256(source_image['image']).hexdigest() == record['digitised_tip']['image']['sha256']
Path('/tmp/shroud-tip-source.' + source_image['ext']).write_bytes(source_image['image'])
```

The exporter itself uses only the Python standard library. Each coordinate
sensitivity range comes from sampling the corners of the declared point,
endpoint and chord allowances. The ranges share calibration errors and are
not independent point tolerances. Source drawing fidelity remains unquantified.
No uncertainty for manufactured geometry is inferred from printing precision.

## Remaining geometry

The `missing_geometry` entries in the geometry record describe the unresolved
blade sections, duct contour and assembly placement. The tip curve and duct
scalar constraints cannot form a complete reference solid. Additional source
geometry or owner approval of stated approximations is required before that
CAD build. The record gives the exact request; no full-rotor, duct solid or
Fluent case is included in this extraction.
