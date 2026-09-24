#!/usr/bin/env python3
"""Grid-convergence and validation analysis for the A0.1 case (Celik et al. 2008 + ASME V&V 20).

Numerical uncertainty follows Celik, I. B. et al., "Procedure for Estimation and Reporting of
Uncertainty Due to Discretization in CFD Applications", ASME J. Fluids Eng. 130(7), 2008:
apparent order from three systematically refined grids, Richardson extrapolation, and a
grid-convergence index with factor of safety 1.25.

The validation comparison follows the uncertainty decision record: U_val combines numerical,
input and experimental uncertainty in quadrature, and turbulence-model spread is reported
separately as a sensitivity range, never folded into U_val.

usage: python scripts/cfd_grid_convergence.py --runs <dir> --out <uncertainty.json>
"""
import argparse, json, math, os, re, sys

FS = 1.25                      # Celik factor of safety for three-grid studies
PLATEAU_REL = 1.0e-4           # engineering quantity must be flat to this over the window
PLATEAU_WINDOW = 500


def read_coeffs(path):
    header, rows = None, []
    for line in open(path):
        if line.startswith("#"):
            if "Time" in line and "Cl" in line:
                header = line.lstrip("#").split()
            continue
        p = line.split()
        if p:
            rows.append([float(v) for v in p])
    if header is None:
        raise SystemExit(f"no column header in {path}")
    return header, rows


def series(path, quantity):
    header, rows = read_coeffs(path)
    i = header.index(quantity)
    return [r[0] for r in rows], [r[i] for r in rows]


def plateau(values, window=PLATEAU_WINDOW, tol=PLATEAU_REL):
    """(converged, relative variation) of the engineering quantity over the last `window` steps."""
    w = values[-window:] if len(values) >= window else values
    mean = sum(w) / len(w)
    rel = (max(w) - min(w)) / abs(mean) if mean else float("inf")
    return rel <= tol, rel


def apparent_order(phi1, phi2, phi3, r21, r32, tol=1e-12, itmax=200):
    """Celik eq. (3): solve p = |ln|e32/e21| + q(p)| / ln(r21) by fixed-point iteration."""
    e21, e32 = phi2 - phi1, phi3 - phi2
    if e21 == 0 or e32 == 0:
        return None, None, "zero difference between grid levels"
    s = math.copysign(1.0, e32 / e21)
    p = abs(math.log(abs(e32 / e21))) / math.log(r21)
    for _ in range(itmax):
        q = math.log((r21 ** p - s) / (r32 ** p - s))
        pn = abs(math.log(abs(e32 / e21)) + q) / math.log(r21)
        if abs(pn - p) < tol:
            p = pn
            break
        p = pn
    monotonic = s > 0
    return p, s, None if monotonic else "oscillatory convergence (sign change between levels)"


def gci(phi1, phi2, phi3, h1, h2, h3):
    r21, r32 = h2 / h1, h3 / h2
    p, s, note = apparent_order(phi1, phi2, phi3, r21, r32)
    if p is None:
        return dict(error=note)
    phi_ext21 = (r21 ** p * phi1 - phi2) / (r21 ** p - 1)
    e_a21 = abs((phi1 - phi2) / phi1)
    e_ext21 = abs((phi_ext21 - phi1) / phi_ext21)
    gci21 = FS * e_a21 / (r21 ** p - 1)
    # DIAGNOSTIC ONLY, not a check. With equal refinement ratios and the order fitted from the
    # same three values, r^p = |(phi3-phi2)/(phi2-phi1)| identically, and this ratio then reduces
    # algebraically to |phi1/phi2|. It therefore confirms nothing about the asymptotic range: one
    # three-grid set gives two ADJACENT pairs, not two independent triplets. It is retained
    # because it is cheap and its value is still worth seeing, and tests/test_cfd_records.py
    # demonstrates the identity so nobody reads it as evidence again.
    e_a32 = abs((phi2 - phi3) / phi2)
    gci32 = FS * e_a32 / (r32 ** p - 1)
    asymptotic_ratio = gci32 / (r21 ** p * gci21) if gci21 else None
    # Deliberately NOT used to gate a verdict: see the note above.
    in_asymptotic_range = None
    return dict(apparent_order=p, sign=s, note=note, r21=r21, r32=r32,
                gci_coarse_triplet_fraction=gci32,
                asymptotic_ratio=asymptotic_ratio,
                asymptotic_ratio_is_diagnostic_only=True,
                asymptotic_ratio_identity="equals |phi_fine/phi_medium| for equal r with a fitted order",
                in_asymptotic_range=in_asymptotic_range,
                phi_fine=phi1, phi_medium=phi2, phi_coarse=phi3,
                richardson_extrapolated=phi_ext21,
                approx_rel_error=e_a21, extrap_rel_error=e_ext21,
                gci_fine_fraction=gci21, gci_fine_percent=100 * gci21,
                U_num_absolute=gci21 * abs(phi1),
                factor_of_safety=FS,
                monotonic=bool(s > 0))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quantity", default="Cl")
    ap.add_argument("--reference", type=float, required=True)
    ap.add_argument("--u-d", type=float, default=None, dest="u_d")
    ap.add_argument("--u-input", type=float, default=None, dest="u_input")
    ap.add_argument("--alpha", type=float, required=True)
    a = ap.parse_args()

    levels = [("g3", 57344), ("g2", 14336), ("g1", 3584)]      # fine -> coarse
    models, cases = {}, {}
    for short in ("SA", "SST"):
        per = {}
        for g, cells in levels:
            case = os.path.join(a.runs, f"{g}_{short}_a{a.alpha:g}")
            f = os.path.join(case, "postProcessing", "forceCoeffs1", "0", "coefficient.dat")
            if not os.path.isfile(f):
                per[g] = dict(status="MISSING", path=f)
                continue
            t, v = series(f, a.quantity)
            conv, rel = plateau(v)
            cd_t, cd_v = series(f, "Cd")
            per[g] = dict(status="PASS" if conv else "UNCONVERGED", cells=cells,
                          iterations=int(t[-1]), value=v[-1], cd=cd_v[-1],
                          plateau_relative_variation=rel, plateau_tolerance=PLATEAU_REL,
                          h=1.0 / math.sqrt(cells))
        cases[short] = per
        usable = [g for g, _ in levels if per[g].get("status") == "PASS"]
        if len(usable) == 3:
            phi = [per[g]["value"] for g, _ in levels]
            h = [per[g]["h"] for g, _ in levels]
            models[short] = gci(phi[0], phi[1], phi[2], h[0], h[1], h[2])
        else:
            models[short] = dict(error=f"need three converged levels, have {usable}")

    out = dict(schema_version=1, quantity=a.quantity, alpha_deg=a.alpha,
               grid_levels=[g for g, _ in levels], cases=cases, per_model=models,
               # Only models whose order was actually computed appear here. A model that
               # could not be evaluated is recorded with its reason in per_model instead;
               # writing a null order would look like a reported result.
               observed_order={m: models[m]["apparent_order"] for m in models
                               if models[m].get("apparent_order") is not None},
               reference=dict(value=a.reference, U_D_k1=a.u_d, U_input=a.u_input,
                              U_D_interpretation="spread across trip treatments is TREATMENT SENSITIVITY, "
                                                 "not repeatability: the grit sizes are different "
                                                 "experimental conditions, not repeats of one"))

    ok = [m for m in models if "error" not in models[m]]
    if ok:
        comp = {}
        for m in ok:
            S = models[m]["phi_fine"]; U_num = models[m]["U_num_absolute"]
            E = S - a.reference
            # An unquantified component cannot be silently dropped: combining only the known
            # terms and calling the result U_val treats the unknown as zero, which is the one
            # thing it is not. Where a required component is missing, U_val is null and the
            # missing components are named; a partial combination is reported under its own name
            # so it can never be mistaken for a complete validation uncertainty.
            missing = [n for n, v in (("U_input", a.u_input), ("U_D", a.u_d)) if v is None]
            partial = math.sqrt(U_num ** 2 + sum(v ** 2 for v in (a.u_input, a.u_d) if v is not None))
            complete = None if missing else partial
            comp[m] = dict(S=S, D=a.reference, comparison_error_E=E,
                           U_num=U_num, U_D=a.u_d, U_input=a.u_input,
                           missing_components=missing,
                           partial_combination_of_known_terms=partial,
                           U_val=complete,
                           abs_E_le_U_val=(abs(E) <= complete) if complete is not None else None,
                           screen="consistency screen for this project, not a universal pass/fail rule",
                           E_percent_of_D=100 * E / a.reference)
        out["validation"] = comp
        vals = [models[m]["phi_fine"] for m in ok]
        out["model_form_sensitivity"] = dict(
            models=ok, values={m: models[m]["phi_fine"] for m in ok},
            range=max(vals) - min(vals) if len(vals) > 1 else 0.0,
            note="Reported as a sensitivity range between discrete model choices. "
                 "Per the uncertainty decision record this is NOT combined into U_val.")
        verdicts = {}
        for m in ok:
            c = comp[m]
            if c["U_val"] is None:
                verdicts[m] = "INCOMPLETE_UNCERTAINTY"
            elif c["abs_E_le_U_val"]:
                verdicts[m] = "CONSISTENT_AT_U_VAL"
            else:
                verdicts[m] = "INCONSISTENT_AT_U_VAL"
        for m in ok:
            if "oscillatory" in (models[m].get("note") or ""):
                verdicts[m] = "INCONCLUSIVE"

        out["verdict_per_model"] = verdicts
        out["claim_boundary"] = ("A0.1 validates a two-dimensional airfoil workflow at this condition only. "
                                 "It says nothing about rotating-frame loading, three-dimensional flow, ducts or tip gaps. "
                                 "U_D covers one contrast across grit treatments and excludes tunnel systematics, so it is a "
                                 "lower bound on experimental uncertainty and the comparison is correspondingly narrow. "
                                 "Different grits are different conditions, so that spread is treatment sensitivity, "
                                 "not repeatability.")
    else:
        out["verdict_per_model"] = {m: "INCONCLUSIVE" for m in models}
        out["claim_boundary"] = "No verdict: the grid study did not produce three converged levels."

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w").write(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("verdict_per_model",) if k in out}, indent=1))
    for m in models:
        e = models[m]
        if "error" in e:
            print(f"{m}: {e['error']}")
        else:
            print(f"{m}: p={e['apparent_order']:.3f} phi_fine={e['phi_fine']:.6f} "
                  f"GCI={e['gci_fine_percent']:.3f}% U_num={e['U_num_absolute']:.5f} "
                  f"monotonic={e['monotonic']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
