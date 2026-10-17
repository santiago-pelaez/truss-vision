import type { SceneModel } from "../model/scene";

export default function Preview3D({ scene }: { scene: SceneModel }) {
  return (
    <div className="preview3d">
      <div className="axis axis-x">X</div>
      <div className="axis axis-y">Y</div>
      <div className="axis axis-z">Z</div>
      <p>Three.js preview boundary ready for {scene.nodes.length} nodes and {scene.members.length} members.</p>
    </div>
  );
}
