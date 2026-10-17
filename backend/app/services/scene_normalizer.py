from app.schemas.scene import SceneModel


def normalize_scene(scene: SceneModel) -> SceneModel:
    node_ids = {node.id for node in scene.nodes}
    scene.members = [
        member for member in scene.members
        if member.a in node_ids and member.b in node_ids and member.a != member.b
    ]
    scene.loads = [load for load in scene.loads if load.node in node_ids]

    if scene.units == "relative":
        scene.warnings.append("Coordinates are illustrative; confirm dimensions before calculating.")
    if scene.spatial:
        scene.warnings.append("3D rendering is educational; full 3D equilibrium is not implemented.")
    if scene.confidence < 0.7:
        scene.warnings.append("Haunted scan: Gemma is not confident in this reconstruction. Review every element before calculating.")
    if scene.questions:
        scene.warnings.append("Gemma has unanswered questions about the source image. Resolve them during review.")

    return scene
