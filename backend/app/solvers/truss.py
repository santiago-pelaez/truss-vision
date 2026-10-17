import numpy as np

from app.schemas.scene import SceneModel


def _length_factor(units: str) -> float:
    return {"m": 1.0, "ft": 0.3048, "in": 0.0254}.get(units, 1.0)


def _force_factor(unit: str) -> float:
    return {"kN": 1000.0, "N": 1.0, "lb": 4.4482216152605}.get(unit, 1.0)


def solve_truss(scene: SceneModel) -> dict:
    if scene.spatial or scene.kind != "truss":
        raise ValueError("Only planar trusses are supported.")
    if scene.pointLoads or scene.distributedLoads:
        raise ValueError("The truss solver accepts joint loads only.")
    if not scene.nodes or not scene.members:
        raise ValueError("A truss needs nodes and members.")

    index = {node.id: i for i, node in enumerate(scene.nodes)}
    n = len(scene.nodes)
    dof = 2 * n
    stiffness = np.zeros((dof, dof), dtype=float)
    force = np.zeros(dof, dtype=float)
    length_factor = _length_factor(scene.units)
    area = 1200e-6
    modulus = 200e9

    elements = []
    for member in scene.members:
        i, j = index[member.a], index[member.b]
        a, b = scene.nodes[i], scene.nodes[j]
        dx, dy = (b.x - a.x) * length_factor, (b.y - a.y) * length_factor
        length = float(np.hypot(dx, dy))
        if length <= 1e-9:
            raise ValueError(f"Member {member.a}-{member.b} has zero length.")
        c, s = dx / length, dy / length
        vector = np.array([c, s, -c, -s])
        local = modulus * area / length * np.outer(vector, vector)
        indices = [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
        for row, row_index in enumerate(indices):
            for col, col_index in enumerate(indices):
                stiffness[row_index, col_index] += local[row, col]
        elements.append((member, i, j, length, c, s))

    force_factor = _force_factor(scene.forceUnit)
    for load in scene.loads:
        i = index[load.node]
        force[2 * i] += load.fx * force_factor
        force[2 * i + 1] += load.fy * force_factor

    fixed: set[int] = set()
    for i, node in enumerate(scene.nodes):
        if node.support in {"pin", "fixed"}:
            fixed.update({2 * i, 2 * i + 1})
        elif node.support == "roller":
            fixed.add(2 * i + 1)

    free = [i for i in range(dof) if i not in fixed]
    if not fixed or not free:
        raise ValueError("Insufficient restraints or free degrees of freedom.")
    displacement = np.zeros(dof)
    displacement[free] = np.linalg.solve(stiffness[np.ix_(free, free)], force[free])
    reactions = stiffness @ displacement - force

    member_forces = []
    for member, i, j, length, c, s in elements:
        extension = c * (displacement[2 * j] - displacement[2 * i]) + s * (displacement[2 * j + 1] - displacement[2 * i + 1])
        axial = modulus * area / length * extension
        member_forces.append({"member": f"{member.a}-{member.b}", "forceN": float(axial), "state": "tension" if axial >= 0 else "compression"})

    return {
        "memberForces": member_forces,
        "reactions": [{"node": node.id, "rxN": float(reactions[2 * i]), "ryN": float(reactions[2 * i + 1])} for i, node in enumerate(scene.nodes) if node.support != "none"],
        "maxDisplacementMm": float(np.max(np.abs(displacement)) * 1000)
    }
