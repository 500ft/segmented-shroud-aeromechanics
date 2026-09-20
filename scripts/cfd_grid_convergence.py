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
    return dict(apparent_order=p, sign=s, note=note, r21=r21, r32=r32,
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
    ap.add_argument("--u-d", type=float, required=True, dest="u_d")
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
               reference=dict(value=a.reference, U_D_k1=a.u_d))

    ok = [m for m in models if "error" not in models[m]]
    if ok:
        comp = {}
        for m in ok:
            S = models[m]["phi_fine"]; U_num = models[m]["U_num_absolute"]
            E = S - a.reference
            U_val = math.sqrt(U_num ** 2 + a.u_d ** 2)          # U_input unquantified, see note
            comp[m] = dict(S=S, D=a.reference, comparison_error_E=E,
                           U_num=U_num, U_D=a.u_d, U_input="unquantified",
                           U_val=U_val, abs_E_le_U_val=abs(E) <= U_val,
                           E_percent_of_D=100 * E / a.reference)
        out["validation"] = comp
        vals = [models[m]["phi_fine"] for m in ok]
        out["model_form_sensitivity"] = dict(
            models=ok, values={m: models[m]["phi_fine"] for m in ok},
            range=max(vals) - min(vals) if len(vals) > 1 else 0.0,
            note="Reported as a sensitivity range between discrete model choices. "
                 "Per the uncertainty decision record this is NOT combined into U_val.")
        verdicts = {m: ("VALIDATED_AT_U_VAL" if comp[m]["abs_E_le_U_val"] else "NOT_VALIDATED")
                    for m in ok}
        if any("oscillatory" in (models[m].get("note") or "") for m in ok):
            verdicts = {m: "INCONCLUSIVE" for m in ok}
        out["verdict_per_model"] = verdicts
        out["claim_boundary"] = ("A0.1 validates a two-dimensional airfoil workflow at this condition only. "
                                 "It says nothing about rotating-frame loading, three-dimensional flow, ducts or tip gaps. "
                                 "U_D covers trip repeatability only and excludes tunnel systematics, so it is a lower "
                                 "bound and the validation statement is correspondingly narrow.")
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
