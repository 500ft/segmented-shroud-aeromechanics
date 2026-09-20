#!/usr/bin/env python3
"""Generate one OpenFOAM case for the TMR 2D NACA 0012 validation (A0.1).

Conditions follow the TMR 2DN00 specification: M = 0.15 (treated as incompressible),
Re = 6e6 per chord, fully turbulent. With U = 1 m/s and chord = 1 m, nu = 1/6e6.

Freestream turbulence is the TMR specification converted to these units, not a guess:
  SA  : nuTilda_inf / nu_inf = 3           -> nut/nu ~ 0.21
  SST : k_inf = 9e-9 a_inf^2, omega_inf = 1e-6 a_inf^2 / nu_inf   -> nut/nu ~ 0.009
with a_inf = U/M.
"""
import argparse, math, os, shutil

HEAD = ('FoamFile\n{{\n    version 2.0;\n    format ascii;\n    class {cls};\n'
        '    object {obj};\n}}\n')

U_INF, CHORD, MACH = 1.0, 1.0, 0.15
NU = 1.0 / 6.0e6
A_INF = U_INF / MACH
K_INF = 9.0e-9 * A_INF ** 2
OMEGA_INF = 1.0e-6 * A_INF ** 2 / NU
NUTILDA_INF = 3.0 * NU

MODELS = {
    "SpalartAllmaras": dict(fields=("nuTilda",), extra=""),
    "kOmegaSST": dict(fields=("k", "omega"), extra=""),
}


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


def field(case, obj, cls, dims, internal, patches):
    body = HEAD.format(cls=cls, obj=obj)
    body += f"dimensions      {dims};\ninternalField   uniform {internal};\n\nboundaryField\n{{\n"
    for name, spec in patches.items():
        body += f"    {name}\n    {{\n"
        for k, v in spec.items():
            body += f"        {k:<16}{v};\n"
        body += "    }\n"
    body += "}\n"
    w(f"{case}/0/{obj}", body)


def build(case, mesh_msh, model, alpha_deg, thickness, end_time=6000):
    if os.path.exists(case):
        shutil.rmtree(case)
    a = math.radians(alpha_deg)
    ux, uy = U_INF * math.cos(a), U_INF * math.sin(a)
    lift = (-math.sin(a), math.cos(a), 0.0)
    drag = (math.cos(a), math.sin(a), 0.0)
    free = dict(type="freestream", freestreamValue=f"uniform ({ux:.12g} {uy:.12g} 0)")

    field(case, "U", "volVectorField", "[0 1 -1 0 0 0 0]", f"({ux:.12g} {uy:.12g} 0)", {
        "airfoil": dict(type="noSlip"),
        "farfield": free, "outlet": free,
        "front": dict(type="empty"), "back": dict(type="empty")})
    field(case, "p", "volScalarField", "[0 2 -2 0 0 0 0]", "0", {
        "airfoil": dict(type="zeroGradient"),
        "farfield": dict(type="freestreamPressure", freestreamValue="uniform 0"),
        "outlet": dict(type="freestreamPressure", freestreamValue="uniform 0"),
        "front": dict(type="empty"), "back": dict(type="empty")})
    field(case, "nut", "volScalarField", "[0 2 -1 0 0 0 0]", "0", {
        "airfoil": dict(type="nutLowReWallFunction", value="uniform 0"),
        "farfield": dict(type="calculated", value="uniform 0"),
        "outlet": dict(type="calculated", value="uniform 0"),
        "front": dict(type="empty"), "back": dict(type="empty")})

    if model == "SpalartAllmaras":
        field(case, "nuTilda", "volScalarField", "[0 2 -1 0 0 0 0]", f"{NUTILDA_INF:.12g}", {
            "airfoil": dict(type="fixedValue", value="uniform 0"),
            "farfield": dict(type="freestream", freestreamValue=f"uniform {NUTILDA_INF:.12g}"),
            "outlet": dict(type="freestream", freestreamValue=f"uniform {NUTILDA_INF:.12g}"),
            "front": dict(type="empty"), "back": dict(type="empty")})
    else:
        field(case, "k", "volScalarField", "[0 2 -2 0 0 0 0]", f"{K_INF:.12g}", {
            "airfoil": dict(type="fixedValue", value="uniform 1e-16"),
            "farfield": dict(type="freestream", freestreamValue=f"uniform {K_INF:.12g}"),
            "outlet": dict(type="freestream", freestreamValue=f"uniform {K_INF:.12g}"),
            "front": dict(type="empty"), "back": dict(type="empty")})
        field(case, "omega", "volScalarField", "[0 0 -1 0 0 0 0]", f"{OMEGA_INF:.12g}", {
            "airfoil": dict(type="omegaWallFunction", value=f"uniform {OMEGA_INF:.12g}"),
            "farfield": dict(type="freestream", freestreamValue=f"uniform {OMEGA_INF:.12g}"),
            "outlet": dict(type="freestream", freestreamValue=f"uniform {OMEGA_INF:.12g}"),
            "front": dict(type="empty"), "back": dict(type="empty")})

    w(f"{case}/constant/transportProperties",
      HEAD.format(cls="dictionary", obj="transportProperties") +
      f"transportModel  Newtonian;\nnu              {NU:.12g};\n")
    w(f"{case}/constant/momentumTransport",
      HEAD.format(cls="dictionary", obj="momentumTransport") +
      f"simulationType  RAS;\nRAS\n{{\n    model           {model};\n"
      "    turbulence      on;\n    printCoeffs     on;\n}\n")
    w(f"{case}/constant/turbulenceProperties",
      HEAD.format(cls="dictionary", obj="turbulenceProperties") +
      f"simulationType  RAS;\nRAS\n{{\n    RASModel        {model};\n"
      "    turbulence      on;\n    printCoeffs     on;\n}\n")

    aref = CHORD * thickness
    w(f"{case}/system/controlDict",
      HEAD.format(cls="dictionary", obj="controlDict") +
      f"""application     simpleFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         {end_time};
deltaT          1;
writeControl    timeStep;
writeInterval   {end_time};
purgeWrite      1;
writeFormat     ascii;
writePrecision  10;
timeFormat      general;
runTimeModifiable false;

functions
{{
    forceCoeffs1
    {{
        type            forceCoeffs;
        libs            (forces);
        writeControl    timeStep;
        writeInterval   1;
        log             no;
        patches         (airfoil);
        rho             rhoInf;
        rhoInf          1;
        liftDir         ({lift[0]:.12g} {lift[1]:.12g} 0);
        dragDir         ({drag[0]:.12g} {drag[1]:.12g} 0);
        CofR            (0.25 0 0);
        pitchAxis       (0 0 1);
        magUInf         {U_INF};
        lRef            {CHORD};
        Aref            {aref:.12g};
    }}
}}
""")
    # Non-orthogonality reaches ~86 deg near the trailing edge and in the far wake, so the
    # Laplacian and surface-normal gradients are limited rather than fully corrected.
    w(f"{case}/system/fvSchemes",
      HEAD.format(cls="dictionary", obj="fvSchemes") + """
ddtSchemes      { default steadyState; }
gradSchemes     { default cellLimited Gauss linear 1; }
divSchemes
{
    default         none;
    div(phi,U)      bounded Gauss linearUpwind grad(U);
    div(phi,nuTilda) bounded Gauss linearUpwind grad(nuTilda);
    div(phi,k)      bounded Gauss linearUpwind grad(k);
    div(phi,omega)  bounded Gauss linearUpwind grad(omega);
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}
laplacianSchemes { default Gauss linear limited corrected 0.33; }
interpolationSchemes { default linear; }
snGradSchemes   { default limited corrected 0.33; }
wallDist        { method meshWave; }
""")
    w(f"{case}/system/fvSolution",
      HEAD.format(cls="dictionary", obj="fvSolution") + """
solvers
{
    p
    {
        solver          GAMG;
        smoother        GaussSeidel;
        tolerance       1e-9;
        relTol          0.01;
    }
    "(U|nuTilda|k|omega)"
    {
        solver          PBiCGStab;
        preconditioner  DILU;
        tolerance       1e-10;
        relTol          0.01;
    }
}

SIMPLE
{
    nNonOrthogonalCorrectors 2;
    consistent      yes;
    residualControl
    {
        p               1e-7;
        U               1e-8;
        "(nuTilda|k|omega)" 1e-8;
    }
}

relaxationFactors
{
    equations
    {
        U               0.8;
        "(nuTilda|k|omega)" 0.7;
    }
}
""")
    return dict(case=case, model=model, alpha_deg=alpha_deg, nu=NU, k_inf=K_INF,
                omega_inf=OMEGA_INF, nutilda_inf=NUTILDA_INF, Aref=aref)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("case"); ap.add_argument("mesh")
    ap.add_argument("--model", required=True, choices=sorted(MODELS))
    ap.add_argument("--alpha", type=float, required=True)
    ap.add_argument("--thickness", type=float, default=1.0)
    ap.add_argument("--end", type=int, default=6000)
    a = ap.parse_args()
    print(build(a.case, a.mesh, a.model, a.alpha, a.thickness, a.end))
