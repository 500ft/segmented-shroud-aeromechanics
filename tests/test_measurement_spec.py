"""The measurement-requirements draft must carry the budget register exactly (plan D6).

Only the table between the two HTML comment markers is parsed; nothing else in the draft is
checked here. Channel adequacy and acceptance logic are a human review (T16)."""
import csv, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SPEC = ROOT / "docs/measurement-system-spec.md"
REGISTER = ROOT / "docs/clearance-measurement-budget.csv"
START, END = "<!-- budget-register:start -->", "<!-- budget-register:end -->"
COLUMNS = ["term", "unit", "value", "evidence_state", "source", "interpretation", "next_input"]


def budget_table(text):
    """Rows of the delimited table between the markers, as dicts keyed by the header cells."""
    body = text.split(START, 1)[1].split(END, 1)[0]
    lines = [l.strip() for l in body.strip().splitlines() if l.strip().startswith("|")]
    cells = [[c.strip() for c in l.strip("|").split("|")] for l in lines]
    header, rows = cells[0], [r for r in cells[2:]]           # cells[1] is the separator row
    return [dict(zip(header, r)) for r in rows]


def register(path=REGISTER):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def compare(rows, reg):
    """Defects between the spec table and the register; empty means they agree."""
    out, terms = [], [r.get("term") for r in rows]
    if set(rows[0]) != set(COLUMNS) if rows else True:
        out.append("table columns differ from the contract")
    dup = sorted({t for t in terms if terms.count(t) > 1})
    if dup:
        out.append(f"duplicate term rows {dup}")
    expected = {r["term"]: r for r in reg}
    if set(terms) != set(expected):
        out.append(f"term set differs: missing {sorted(set(expected) - set(terms))}, extra {sorted(set(terms) - set(expected))}")
    for r in rows:
        e = expected.get(r.get("term"))
        if e is None:
            continue
        want = dict(unit=e["unit"], value=e["value"] or "pending", evidence_state=e["evidence_state"], source=e["source"])
        for k, v in want.items():
            if r.get(k) != v:
                out.append(f"{r['term']}: {k} is {r.get(k)!r}, register has {v!r}")
    return out


class SpecRegisterTests(unittest.TestCase):
    def test_draft_table_matches_the_register(self):
        rows = budget_table(SPEC.read_text())
        self.assertEqual(len(rows), len(register()))
        self.assertEqual(compare(rows, register()), [])

    def test_counterexamples_are_rejected(self):
        reg = register(); good = budget_table(SPEC.read_text())
        self.assertEqual(compare(good, reg), [])
        cases = {
            "wrong unit": lambda rows: rows[0].update(unit="mm"),
            "wrong state": lambda rows: rows[0].update(evidence_state="measured"),
            "wrong value": lambda rows: rows[0].update(value="30"),
            "wrong source": lambda rows: rows[0].update(source="made up"),
            "duplicate term": lambda rows: rows.append(dict(rows[0])),
            "missing term": lambda rows: rows.pop(),
            "pending replaced by a number": lambda rows: next(r for r in rows if r["value"] == "pending").update(value="10"),
        }
        for name, mutate in cases.items():
            rows = [dict(r) for r in good]; mutate(rows)
            self.assertTrue(compare(rows, reg), f"{name} was not rejected")


if __name__ == "__main__":
    unittest.main()
