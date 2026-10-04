# Akturk-Camci partial geometry

These published station values and the preserved tip trace support the executed
[reference feasibility audit](../../../evidence/task-reference-feasibility-2026-10-04/README.md).
They are insufficient to construct the complete reference assembly.

[geometry.json](geometry.json) records attribution, source URLs and hashes,
units, local coordinates, chosen extraction allowances and missing dimensions.
The CSVs are reused unchanged from the preservation commit identified there.
Generate the millimetre curve and inspection SVG with:

```bash
python scripts/export_reference_geometry.py --output-dir /tmp/shroud-reference-export
```

Public author copies provide access to the ASME papers. No explicit data reuse
licence was identified. The project's MIT licence covers its code; it does not
relicense those papers or establish rights in third-party data. Source PDFs and
images are not distributed here.
