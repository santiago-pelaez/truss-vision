from app.schemas.scene import SceneModel
from app.services.scene_normalizer import normalize_scene


def test_normalizer_removes_orphaned_edges_and_warns_on_relative_units():
    scene = SceneModel.model_validate({
        "kind": "truss",
        "nodes": [{"id": "A", "x": 0, "y": 0}],
        "members": [{"a": "A", "b": "MISSING"}],
        "units": "relative"
    })
    normalized = normalize_scene(scene)
    assert normalized.members == []
    assert any("relative" in warning for warning in normalized.warnings)


def test_normalizer_marks_low_confidence_scene_as_haunted_review():
    scene = SceneModel.model_validate({"confidence": 0.4, "questions": ["Is the right support a roller?"]})
    normalized = normalize_scene(scene)
    assert any("Haunted scan" in warning for warning in normalized.warnings)
    assert any("unanswered questions" in warning for warning in normalized.warnings)
