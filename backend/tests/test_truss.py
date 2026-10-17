from app.schemas.scene import SceneModel
from app.solvers.truss import solve_truss


def test_simple_truss_returns_member_forces():
    scene = SceneModel.model_validate({
        "kind": "truss",
        "units": "m",
        "forceUnit": "kN",
        "nodes": [
            {"id": "A", "x": 0, "y": 0, "support": "pin"},
            {"id": "B", "x": 4, "y": 0, "support": "roller"},
            {"id": "C", "x": 2, "y": 3}
        ],
        "members": [{"a": "A", "b": "B"}, {"a": "A", "b": "C"}, {"a": "C", "b": "B"}],
        "loads": [{"node": "C", "fy": -10}]
    })
    result = solve_truss(scene)
    assert len(result["memberForces"]) == 3
    assert len(result["reactions"]) == 2
