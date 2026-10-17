import type { SceneModel } from "./scene";

export function validateScene(scene: SceneModel): SceneModel {
  if (!scene || !Array.isArray(scene.nodes) || !Array.isArray(scene.members)) {
    throw new Error("The extracted scene is missing nodes or members.");
  }

  const ids = new Set<string>();
  for (const node of scene.nodes) {
    if (!node.id || ids.has(node.id)) throw new Error("Node IDs must be unique.");
    ids.add(node.id);
  }

  for (const member of scene.members) {
    if (!ids.has(member.a) || !ids.has(member.b) || member.a === member.b) {
      throw new Error("Every member must connect two different existing nodes.");
    }
  }

  return scene;
}
