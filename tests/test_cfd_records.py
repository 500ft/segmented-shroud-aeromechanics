"""CFD record discipline and historical-evidence preservation (work order, testing requirements).

Three things are enforced here:

1. Every CFD case manifest carries enough identity to reproduce the case.
2. No reported grid-convergence index is built on fewer than three mesh levels, and nothing
   claims validation without a rung-scoped claim boundary.
3. The historical acquisition and reading evidence is byte-identical. Those files are the
   provenance record of work that cannot be re-run; a later lane must never rewrite them.

No CFD manifest exists yet. The manifest checks therefore pass vacuously today and begin
biting the moment the first case is written. The negative controls run against synthetic
documents so the checks are proven to reject real defects now, not merely to be silent.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFD_ROOT = ROOT / "results/generated/cfd"
EVIDENCE = ROOT / "evidence/task-a0-validation"

REQUIRED_MANIFEST_FIELDS = {
    "case_id", "study", "rung", "source_document_sha256", "source_locator",
    "geometry_revision", "mesh_input_sha256", "mesh_sha256", "cell_count",
    "solver_image_digest", "solver_version", "turbulence_model",
    "boundary_conditions", "operating_point", "convergence_rule",
    "outputs", "status", "git_commit",
}
ALLOWED_STATUS = {"PASS", "FAILED", "UNCONVERGED"}
MIN_GRID_LEVELS = 3

# Evidence labels permitted by the work order (D2a added VERIFIED_FROM_ARCHIVE).
ALLOWED_EVIDENCE_LABELS = {
    "VERIFIED_FROM_SOURCE", "VERIFIED_FROM_ARCHIVE",
    "DERIVED_FROM_SOURCE", "ASSUMED_FOR_MESH_ONLY", "MISSING",
}

# Files that record work which cannot be re-run. They are immutable by policy.
IMMUTABLE = {
    "docs/day3-reading-records.json": "477e256e15e81824ae88836e308f0a28633ab92db2c3b2ffd8fb9fff77e1257f",
    "docs/source-eligibility-register.json": "b8bf3f28b245025117c966a0391e42d5aa4eedae4c9955f7d938698f463d1deb",
    "evidence/task-2026-09-09/database-export.json": "4298f5e712c7a9232e2f28cfa794289b84823063b8fd314586e6f0df16360644",
    "evidence/task-2026-09-11-public/database-export.json": "d7ca70193a82f67eea761b5dec3becfd9a71f2919d922f7801e4e836da5bad52",
    "evidence/task-day3-2026-09-09/acquisition-ledger.json": "b7065da87c45d786cf8dda7add4347bd2f9cd3922aba39eed4ff7a05b0acf895",
    "docs/clearance-measurement-budget.csv": "fdb1d74fb5492ea637c6e0fb5c56ac5fd908a49a9a00e84da7da1baa132f4f81",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def manifest_problems(doc):
    """Defects in one CFD case manifest; empty list means it carries reproducible identity."""
    out = []
    missing = REQUIRED_MANIFEST_FIELDS - set(doc)
    if missing:
        out.append(f"missing fields: {sorted(missing)}")
    if doc.get("status") not in ALLOWED_STATUS:
        out.append(f"status must be one of {sorted(ALLOWED_STATUS)}, got {doc.get('status')!r}")
    if not str(doc.get("solver_image_digest", "")).startswith("sha256:"):
        out.append("solver_image_digest must be a pinned sha256 digest, not a moving tag")
    cells = doc.get("cell_count")
    if not isinstance(cells, int) or cells <= 0:
        out.append("cell_count must be a positive integer")
    return out


def uncertainty_problems(doc):
    """Defects in a reported uncertainty/verdict record."""
    out = []
    levels = doc.get("grid_levels")
    if not isinstance(levels, list) or len(levels) < MIN_GRID_LEVELS:
        out.append(f"a reported GCI needs at least {MIN_GRID_LEVELS} grid levels, got {levels!r}")
    order = doc.get("observed_order")
    if order is None:
        out.append("observed order of convergence must be computed and reported, not assumed")
    elif isinstance(order, dict):
        bad = [k for k, v in order.items() if not isinstance(v, (int, float)) or v != v]
        if not order or bad:
            out.append(f"observed order missing or not numeric for: {bad or 'every model'}")
    elif not isinstance(order, (int, float)):
        out.append("observed order must be a number or a per-model mapping of numbers")
    verdict = str(doc.get("verdict", ""))
    if verdict.upper().startswith("VALIDATED") and not str(doc.get("claim_boundary", "")).strip():
        out.append("a validated verdict requires an explicit rung-scoped claim_boundary")
    return out


class CfdManifestTests(unittest.TestCase):
    def test_committed_manifests_are_reproducible(self):
        found = sorted(CFD_ROOT.rglob("*.manifest.json")) if CFD_ROOT.exists() else []
        for path in found:
            with self.subTest(manifest=str(path.relative_to(ROOT))):
                self.assertEqual(manifest_problems(json.loads(path.read_text())), [])

    def test_committed_uncertainty_records_are_sound(self):
        found = sorted(CFD_ROOT.rglob("uncertainty.json")) if CFD_ROOT.exists() else []
        for path in found:
            with self.subTest(record=str(path.relative_to(ROOT))):
                self.assertEqual(uncertainty_problems(json.loads(path.read_text())), [])


class CfdNegativeControlTests(unittest.TestCase):
    """The checks must reject real defects, not merely stay quiet while nothing exists."""

    def good_manifest(self):
        return {f: "x" for f in REQUIRED_MANIFEST_FIELDS} | {
            "status": "PASS", "cell_count": 12225,
            "solver_image_digest": "sha256:" + "0" * 64,
        }

    def test_missing_field_is_rejected(self):
        doc = self.good_manifest()
        del doc["mesh_sha256"]
        self.assertTrue(any("mesh_sha256" in p for p in manifest_problems(doc)))

    def test_moving_tag_instead_of_digest_is_rejected(self):
        doc = self.good_manifest()
        doc["solver_image_digest"] = "opencfd/openfoam-default:latest"
        self.assertTrue(any("pinned sha256" in p for p in manifest_problems(doc)))

    def test_unknown_status_is_rejected(self):
        doc = self.good_manifest()
        doc["status"] = "looks fine"
        self.assertTrue(any("status must be" in p for p in manifest_problems(doc)))

    def test_good_manifest_passes(self):
        self.assertEqual(manifest_problems(self.good_manifest()), [])

    def test_two_mesh_gci_is_rejected(self):
        doc = {"grid_levels": ["coarse", "fine"], "observed_order": 2.0, "verdict": "NUMERICALLY_BOUNDED"}
        self.assertTrue(any("at least 3 grid levels" in p for p in uncertainty_problems(doc)))

    def test_assumed_order_is_rejected(self):
        doc = {"grid_levels": [1, 2, 3], "observed_order": None, "verdict": "NUMERICALLY_BOUNDED"}
        self.assertTrue(any("observed order" in p for p in uncertainty_problems(doc)))

    def test_validated_without_claim_boundary_is_rejected(self):
        doc = {"grid_levels": [1, 2, 3], "observed_order": 1.9, "verdict": "VALIDATED_AT_U_VAL", "claim_boundary": "  "}
        self.assertTrue(any("claim_boundary" in p for p in uncertainty_problems(doc)))
        doc["claim_boundary"] = "2D airfoil workflow only; says nothing about rotors, ducts or tip gaps."
        self.assertEqual(uncertainty_problems(doc), [])


class HistoricalPreservationTests(unittest.TestCase):
    def test_immutable_evidence_is_byte_identical(self):
        for rel, digest in IMMUTABLE.items():
            with self.subTest(path=rel):
                path = ROOT / rel
                self.assertTrue(path.is_file(), f"{rel} is missing")
                self.assertEqual(
                    sha256(path), digest,
                    f"{rel} changed. This file records work that cannot be re-run. "
                    "If the change is genuinely intended, it needs its own reviewed change and a new hash here.",
                )


class A0EvidenceRecordTests(unittest.TestCase):
    def test_source_inventory_labels_are_from_the_allowed_set(self):
        doc = json.loads((EVIDENCE / "source-inventory.json").read_text())
        rows = doc["a0_1_parameters"] + doc["a0_2_parameters"]
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(parameter=row["parameter"]):
                self.assertIn(row["evidence_label"], ALLOWED_EVIDENCE_LABELS)
                self.assertTrue(str(row["locator"]).strip(), "every parameter needs a locator")

    def test_every_missing_parameter_is_listed_as_blocking_or_explained(self):
        doc = json.loads((EVIDENCE / "source-inventory.json").read_text())
        for row in doc["a0_1_parameters"] + doc["a0_2_parameters"]:
            if row["evidence_label"] == "MISSING":
                with self.subTest(parameter=row["parameter"]):
                    self.assertTrue(str(row.get("note", "")).strip(),
                                    "a MISSING parameter must state its consequence")

    def test_a01_acceptance_is_frozen_before_results(self):
        doc = json.loads((EVIDENCE / "a01-acceptance.json").read_text())
        self.assertTrue(doc["gated"], "at least one gated quantity is required")
        self.assertTrue(doc["kill_criteria"])
        self.assertTrue(str(doc["claim_boundary"]).strip())
        for item in doc["reported_not_gated"]:
            with self.subTest(quantity=item["quantity"]):
                self.assertTrue(str(item["why_not_gated"]).strip(),
                                "an ungated quantity must say why it is not gated")

    def test_container_record_pins_a_digest(self):
        doc = json.loads((EVIDENCE / "container-smoke.json").read_text())
        self.assertTrue(doc["image"]["digest"].startswith("sha256:"))
        self.assertTrue(doc["image"]["pinned"])
        self.assertEqual(doc["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
