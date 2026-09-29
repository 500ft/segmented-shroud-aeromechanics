"""The research and CAD ledgers must stay parseable, and each row must be a whole row.

Nothing else reads these files, so a write that mangled one (a literal backslash-n as the line
terminator collapsed the whole ledger to a single line) would pass every other check.
"""
import csv
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


class LedgerTests(unittest.TestCase):
    def rows(self, name):
        with open(DOCS / name, newline="") as f:
            return list(csv.DictReader(f))

    def test_the_research_ledger_parses_into_many_rows(self):
        self.assertGreater(len(self.rows("SPRINT_TASKS.csv")), 30)

    def test_identifiers_are_unique_and_non_empty(self):
        for name in ("SPRINT_TASKS.csv", "CAD_TASKS.csv"):
            ids = [r["id"] for r in self.rows(name)]
            self.assertTrue(all(ids), name)
            self.assertEqual(len(ids), len(set(ids)), "%s has a duplicate id" % name)

    def test_no_row_contains_a_literal_escaped_newline(self):
        for name in ("SPRINT_TASKS.csv", "CAD_TASKS.csv"):
            for r in self.rows(name):
                for k, v in r.items():
                    self.assertNotIn("\\n", v or "", "%s %s.%s" % (name, r["id"], k))

    def test_every_row_has_every_column_filled_or_explicitly_empty(self):
        for name in ("SPRINT_TASKS.csv", "CAD_TASKS.csv"):
            for r in self.rows(name):
                self.assertNotIn(None, r.values(), "%s %s is ragged" % (name, r["id"]))
                self.assertNotIn(None, r.keys(), "%s %s has extra cells" % (name, r["id"]))

    def test_a_status_is_present_on_every_row(self):
        for name in ("SPRINT_TASKS.csv", "CAD_TASKS.csv"):
            for r in self.rows(name):
                self.assertTrue((r["status"] or "").strip(), "%s %s has no status" % (name, r["id"]))


if __name__ == "__main__":
    unittest.main()
