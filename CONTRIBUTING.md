# Contributing

Contributions should make the proposed research easier to audit, reproduce, or falsify.

## Evidence rules

- Label every artifact as `literature`, `planned`, `CAD`, `FEA`, `CFD`, or `measured`.
- Never present conceptual geometry as a fabricated specimen.
- Record specimen identity, manufacturing process, geometry, closure settings, operating point, and instrument calibration for every future run.
- Compare aerodynamic conditions at matched thrust unless a protocol explicitly justifies another basis.
- Preserve negative results and simple-model victories.
- Do not use “performance duct,” “strike-safe,” or “validated” without evidence scoped to a registered operating envelope.

## Before opening a pull request

```bash
python scripts/check_repo_contract.py
python scripts/acquisition_ledger.py --check
python scripts/reference_coverage.py --check
python scripts/clearance_uncertainty_budget.py --check
python -m unittest discover -s tests -v
```

Physical contributions additionally require an approved rotor-stand risk assessment. A contribution to this repository is not authorization to operate rotating hardware.

## Public disclosure boundary

This is a public repository. Before contributing potentially enabling mechanism, geometry, or
fabrication detail that may be intended for patent protection, complete
[`XC-02`](docs/TASKS.md#xc-02--record-the-publication-and-disclosure-path-before-adding-implementation-sensitive-detail)
and obtain appropriate guidance. NYU-affiliated contributors can start with
[Technology Opportunities &amp; Ventures](https://tov.med.nyu.edu/for-innovators/intellectual-property-101/).
This repository does not provide legal advice.
