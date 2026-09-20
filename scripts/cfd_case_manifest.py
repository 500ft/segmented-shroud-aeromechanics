#!/usr/bin/env python3
"""Build the committed record for one A0.1 CFD case.

Writes a manifest carrying the identity the repository's CFD record test requires, plus a
downsampled convergence history. The full solver output and mesh stay outside version control
under the work order's data policy (decision D11); the manifest records their hashes and the
command that regenerates them.
"""
import argparse, hashlib, json, os, re, subprocess, sys

REQUIRED_STATUS = {"PASS", "FAILED", "UNCONVERGED"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
    return header, rows


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case", required=True, help="run directory in the scratch area")
    ap.add_argument("--out", required=True, help="committed case directory in the repository")
    ap.add_argument("--mesh", required=True, help="committed gzipped Plot3D grid")
    ap.add_argument("--mesh-msh", required=True, help="intermediate gmsh mesh (not committed)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--alpha", type=float, required=True)
    ap.add_argument("--cells", type=int, required=True)
    ap.add_argument("--solver-digest", required=True)
    ap.add_argument("--solver-version", required=True)
    ap.add_argument("--source-sha256", required=True)
    ap.add_argument("--source-locator", required=True)
    ap.add_argument("--stride", type=int, default=50)
    a = ap.parse_args()

    coeff = os.path.join(a.case, "postProcessing", "forceCoeffs1", "0", "coefficient.dat")
    header, rows = read_coeffs(coeff)
    if header is None or not rows:
        raise SystemExit(f"no usable coefficient data in {coeff}")
    ci = {n: i for i, n in enumerate(header)}
    cl = [r[ci["Cl"]] for r in rows]
    cd = [r[ci["Cd"]] for r in rows]
    w = cl[-500:] if len(cl) >= 500 else cl
    rel = (max(w) - min(w)) / abs(sum(w) / len(w))
    status = "PASS" if rel <= 1e-4 else "UNCONVERGED"

    runinfo = ""
    if os.path.isfile(os.path.join(a.case, "RUNINFO")):
        runinfo = open(os.path.join(a.case, "RUNINFO")).read().strip()
    walltime = None
    m = re.search(r"walltime=(\d+)s", runinfo)
    if m:
        walltime = int(m.group(1))

    os.makedirs(a.out, exist_ok=True)
    hist = os.path.join(a.out, "convergence.dat")
    with open(hist, "w") as f:
        f.write("# downsampled from the solver's force-coefficient history\n")
        f.write("# iteration\tCl\tCd\n")
        for k in range(0, len(rows), a.stride):
            f.write(f"{int(rows[k][0])}\t{cl[k]:.10g}\t{cd[k]:.10g}\n")
        if (len(rows) - 1) % a.stride:
            f.write(f"{int(rows[-1][0])}\t{cl[-1]:.10g}\t{cd[-1]:.10g}\n")

    logs = {}
    for name in ("log.simpleFoam", "log.checkMesh", "log.gmshToFoam"):
        p = os.path.join(a.case, name)
        if os.path.isfile(p):
            logs[name] = dict(sha256=sha256(p), bytes=os.path.getsize(p),
                              committed=False, tail=open(p, errors="ignore").read()[-600:])

    manifest = dict(
        case_id=os.path.basename(a.case.rstrip("/")),
        study="A0.1", rung="A0.1",
        source_document_sha256=a.source_sha256,
        source_locator=a.source_locator,
        geometry_revision="TMR modified NACA 0012, sharp trailing edge, scale factor 1.008930411365",
        mesh_input_sha256=sha256(a.mesh),
        mesh_sha256=sha256(a.mesh_msh),
        cell_count=a.cells,
        solver_image_digest=a.solver_digest,
        solver_version=a.solver_version,
        turbulence_model=a.model,
        boundary_conditions=dict(airfoil="noSlip wall, nutLowReWallFunction",
                                 farfield="freestream / freestreamPressure",
                                 outlet="freestream / freestreamPressure",
                                 front_back="empty (two-dimensional)"),
        operating_point=dict(mach=0.15, reynolds_chord=6.0e6, alpha_deg=a.alpha,
                             U_inf=1.0, chord=1.0, nu=1.0 / 6.0e6,
                             regime="incompressible; Prandtl-Glauert factor 1.011 recorded as a declared bias"),
        convergence_rule="Cl flat to 1e-4 relative over the last 500 iterations",
        convergence_observed=dict(iterations=int(rows[-1][0]),
                                  plateau_relative_variation=rel,
                                  walltime_s=walltime, runinfo=runinfo),
        outputs=dict(Cl=cl[-1], Cd=cd[-1], units="dimensionless"),
        status=status,
        git_commit=git("rev-parse", "HEAD"),
        uncommitted_artifacts=dict(
            note="Mesh and solver output are outside version control per work-order decision D11.",
            logs=logs,
            regenerate=(f"python scripts/p2d_to_gmsh.py <grid>.p2dfmt <mesh>.msh && "
                        f"python scripts/make_case.py <case> <mesh>.msh --model {a.model} --alpha {a.alpha:g} && "
                        f"docker run --rm --platform linux/arm64 -v <dir>:/w {a.solver_digest.split(':')[0] or 'image'} "
                        f"... gmshToFoam && simpleFoam")),
    )
    if manifest["status"] not in REQUIRED_STATUS:
        raise SystemExit(f"bad status {manifest['status']}")
    open(os.path.join(a.out, "case.manifest.json"), "w").write(json.dumps(manifest, indent=1) + "\n")
    print(f"{manifest['case_id']}: status={status} Cl={cl[-1]:.6f} Cd={cd[-1]:.6f} "
          f"rel={rel:.2e} iters={int(rows[-1][0])} walltime={walltime}s")


if __name__ == "__main__":
    sys.exit(main())
