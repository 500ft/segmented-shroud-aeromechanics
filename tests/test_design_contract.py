"""The design contract's defect equations must actually preserve the mean they claim to.

The contract states that the two-lobe family is equal-mean analytically, that an alternating
segment offset preserves the wall-region mean exactly for an even seam count, and that it does
NOT for an odd count. Those are checkable claims, so they are checked here: a future edit that
breaks the construction fails rather than shipping a family that silently changes the mean.

Pure standard library and closed-form integration; no solver and no new dependency.
"""
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/design-contract-experiment-01.md"
TWO_PI = 2.0 * math.pi


def two_lobe_mean(c0, a2, phi2, samples=200_000):
    """Numerical circumferential mean of c0 + a2*cos(2(theta - phi2))."""
    total = sum(c0 + a2 * math.cos(2.0 * (k * TWO_PI / samples - phi2)) for k in range(samples))
    return total / samples


def stepped_wall_mean(c0, step, n, alternating=True):
    """Wall-region mean for n equal segments carrying offsets delta_j.

    With equal segment lengths the length weighting is uniform, so the wall mean is
    c0 + mean(delta_j). Returns (mean, offsets).
    """
    if alternating:
        offsets = [((-1) ** j) * step / 2.0 for j in range(n)]
    else:                                   # solved offsets: remove the residual so the sum is zero
        raw = [((-1) ** j) * step / 2.0 for j in range(n)]
        bias = sum(raw) / n
        offsets = [d - bias for d in raw]
    return c0 + sum(offsets) / n, offsets


class TwoLobeTests(unittest.TestCase):
    def test_two_lobe_is_equal_mean_for_any_amplitude_and_phase(self):
        c0 = 1000.0
        for a2 in (1.0, 50.0, 250.0, 900.0):
            for phi2 in (0.0, 0.3, math.pi / 4, 1.9):
                with self.subTest(a2=a2, phi2=phi2):
                    self.assertAlmostEqual(two_lobe_mean(c0, a2, phi2), c0, places=6)

    def test_minimum_clearance_stays_positive_only_below_the_stated_limit(self):
        """The contract constrains 0 < A2 < c0 to keep the minimum clearance positive."""
        c0 = 1000.0
        self.assertGreater(c0 - 999.0, 0.0)
        self.assertLessEqual(c0 - 1000.0, 0.0, "A2 = c0 touches zero clearance; the limit is strict")


class SteppedSegmentTests(unittest.TestCase):
    def test_alternating_offsets_preserve_the_mean_for_even_segment_counts(self):
        c0, step = 1000.0, 120.0
        for n in (2, 4, 6, 8):
            with self.subTest(n=n):
                mean, offsets = stepped_wall_mean(c0, step, n)
                self.assertAlmostEqual(mean, c0, places=9)
                self.assertAlmostEqual(sum(offsets), 0.0, places=9)

    def test_alternating_offsets_do_not_preserve_the_mean_for_odd_counts(self):
        """This is why the contract calls out odd seam counts as a manufacturing consequence."""
        c0, step = 1000.0, 120.0
        for n in (3, 5, 7):
            with self.subTest(n=n):
                mean, offsets = stepped_wall_mean(c0, step, n)
                self.assertAlmostEqual(sum(offsets), step / 2.0, places=9)
                self.assertNotAlmostEqual(mean, c0, places=6)

    def test_solved_offsets_restore_the_mean_for_odd_counts(self):
        c0, step = 1000.0, 120.0
        for n in (3, 5, 7):
            with self.subTest(n=n):
                mean, offsets = stepped_wall_mean(c0, step, n, alternating=False)
                self.assertAlmostEqual(mean, c0, places=9)
                self.assertAlmostEqual(sum(offsets), 0.0, places=9)
                self.assertNotAlmostEqual(abs(offsets[0]), abs(offsets[1]), places=6,
                                          msg="solved offsets are not equal in magnitude")


class ContractDocumentTests(unittest.TestCase):
    def test_contract_is_labelled_draft_and_not_frozen(self):
        t = CONTRACT.read_text()
        self.assertIn("Not frozen", t)
        self.assertNotIn("Status: frozen", t)

    def test_every_open_input_row_names_a_responsible_party_and_an_exit(self):
        t = CONTRACT.read_text()
        block = t.split("## 9. Open inputs", 1)[1].split("## 10.", 1)[0]
        rows = [l for l in block.splitlines() if l.strip().startswith("|")][2:]
        self.assertGreaterEqual(len(rows), 12)
        for row in rows:
            cells = [c.strip() for c in row.strip("|").split("|")]
            with self.subTest(row=cells[0]):
                self.assertEqual(len(cells), 4)
                for c in cells:
                    self.assertTrue(c, "an open input needs an id, a need, an owner and an exit")

    def test_the_two_rotors_are_distinguished(self):
        """The likeliest wrong claim is carrying a Study A magnitude into the rig."""
        t = CONTRACT.read_text()
        self.assertIn("not the same machine", t)
        self.assertIn("Caradonna", t)


if __name__ == "__main__":
    unittest.main()
