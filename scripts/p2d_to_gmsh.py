#!/usr/bin/env python3
"""Convert a NASA TMR 2D Plot3D C-grid to a one-cell-thick gmsh mesh for OpenFOAM.

The TMR NACA 0012 grids are C-grids whose j=0 line runs: wake cut, airfoil, wake cut.
The two wake-cut segments are exactly coincident (verified: pair distance 0.0), so they are a
branch cut, not a boundary. Their nodes are merged here, which makes the cut internal faces and
lets the wake close properly. Leaving them separate would put a spurious wall in the wake.

Patches written: airfoil (wall), farfield, outlet (the two downstream end columns),
front and back (set to empty after conversion, since this is a 2D case).
"""
import argparse, sys
import numpy as np


def read_p2d(path):
    tok = open(path).read().split()
    k = 0
    nblocks = int(tok[k]); k += 1
    if nblocks != 1:
        raise SystemExit(f"expected 1 block, got {nblocks}")
    ni, nj = int(tok[k]), int(tok[k + 1]); k += 2
    n = ni * nj
    x = np.array(tok[k:k + n], dtype=float).reshape((nj, ni)).T; k += n
    y = np.array(tok[k:k + n], dtype=float).reshape((nj, ni)).T; k += n
    if k != len(tok):
        raise SystemExit(f"trailing tokens in {path}: consumed {k} of {len(tok)}")
    return ni, nj, x, y


def airfoil_span(x, y, ni):
    """Indices on j=0 that lie on the airfoil (0 <= x <= 1 and off the y=0 cut line)."""
    on = (x[:, 0] >= -1e-6) & (x[:, 0] <= 1.0 + 1e-6) & (np.abs(y[:, 0]) < 0.07)
    idx = np.where(on)[0]
    lo, hi = int(idx.min()), int(idx.max())
    if not np.all(np.diff(idx) == 1):
        raise SystemExit("airfoil indices on j=0 are not contiguous")
    if lo != ni - 1 - hi:
        raise SystemExit(f"C-grid not symmetric about the cut: lo={lo} hi={hi} ni={ni}")
    return lo, hi


def convert(src, dst, thickness):
    ni, nj, x, y = read_p2d(src)
    lo, hi = airfoil_span(x, y, ni)

    # Merge the coincident branch-cut nodes on j=0: i>=hi maps onto ni-1-i.
    # The range starts at hi, not hi+1: the trailing edge is SHARP, so the airfoil's two surface
    # endpoints (i=lo and i=hi) are the same physical point. Leaving them as separate nodes stops
    # the first wake-cut face pair from matching and leaves two stray boundary faces at the TE.
    merged = 0
    for i in range(hi, ni):
        d = np.hypot(x[i, 0] - x[ni - 1 - i, 0], y[i, 0] - y[ni - 1 - i, 0])
        if d > 1e-9:
            raise SystemExit(f"wake-cut nodes not coincident at i={i}: distance {d:.3e}")
        merged += 1

    def canon(i, j):
        return (ni - 1 - i, j) if (j == 0 and i >= hi) else (i, j)

    ids, coords = {}, []
    for k in (0, 1):
        for j in range(nj):
            for i in range(ni):
                ci, cj = canon(i, j)
                key = (ci, cj, k)
                if key not in ids:
                    ids[key] = len(coords) + 1                     # gmsh node ids are 1-based
                    coords.append((x[ci, cj], y[ci, cj], k * thickness))
                ids[(i, j, k)] = ids[key]

    def nid(i, j, k):
        return ids[(i, j, k)]

    # Orientation: make the (i,j) quad counter-clockwise so the extruded hex has positive volume.
    x0, y0 = x[0, 0], y[0, 0]
    ax, ay = x[1, 0] - x0, y[1, 0] - y0
    bx, by = x[0, 1] - x0, y[0, 1] - y0
    flip = (ax * by - ay * bx) < 0

    def quad(i, j):
        q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
        return q[::-1] if flip else q

    hexes, faces = [], []
    for j in range(nj - 1):
        for i in range(ni - 1):
            q = quad(i, j)
            hexes.append([nid(a, b, 0) for a, b in q] + [nid(a, b, 1) for a, b in q])

    def side(n0, n1, k_low=0):
        """A vertical boundary quad between two adjacent in-plane nodes."""
        return [nid(*n0, k_low), nid(*n1, k_low), nid(*n1, k_low + 1), nid(*n0, k_low + 1)]

    for i in range(lo, hi):                                        # airfoil wall
        faces.append((2, side((i, 0), (i + 1, 0))))
    for i in range(ni - 1):                                        # farfield
        faces.append((3, side((i, nj - 1), (i + 1, nj - 1))))
    for j in range(nj - 1):                                        # downstream end columns
        faces.append((4, side((0, j), (0, j + 1))))
        faces.append((4, side((ni - 1, j), (ni - 1, j + 1))))
    for j in range(nj - 1):                                        # front and back
        for i in range(ni - 1):
            q = quad(i, j)
            faces.append((5, [nid(a, b, 1) for a, b in q]))
            faces.append((6, [nid(a, b, 0) for a, b in q[::-1]]))

    names = {1: "internal", 2: "airfoil", 3: "farfield", 4: "outlet", 5: "front", 6: "back"}
    with open(dst, "w") as f:
        f.write("$MeshFormat\n2.2 0 8\n$EndMeshFormat\n")
        f.write(f"$PhysicalNames\n{len(names)}\n")
        f.write(f'3 1 "{names[1]}"\n')
        for t in (2, 3, 4, 5, 6):
            f.write(f'2 {t} "{names[t]}"\n')
        f.write("$EndPhysicalNames\n")
        f.write(f"$Nodes\n{len(coords)}\n")
        for n, (px, py, pz) in enumerate(coords, 1):
            f.write(f"{n} {px:.16g} {py:.16g} {pz:.16g}\n")
        f.write("$EndNodes\n")
        f.write(f"$Elements\n{len(hexes) + len(faces)}\n")
        e = 0
        for h in hexes:
            e += 1
            f.write(f"{e} 5 2 1 1 " + " ".join(map(str, h)) + "\n")
        for tag, q in faces:
            e += 1
            f.write(f"{e} 3 2 {tag} {tag} " + " ".join(map(str, q)) + "\n")
        f.write("$EndElements\n")

    return dict(ni=ni, nj=nj, cells=len(hexes), nodes=len(coords), boundary_faces=len(faces),
                airfoil_lo=lo, airfoil_hi=hi, merged_cut_nodes=merged, flipped=bool(flip))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--thickness", type=float, default=1.0)
    a = ap.parse_args()
    info = convert(a.src, a.dst, a.thickness)
    print(" ".join(f"{k}={v}" for k, v in info.items()))
