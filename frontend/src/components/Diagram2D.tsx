import type { SceneModel } from "../model/scene";

export default function Diagram2D({ scene, onDeleteMember }: { scene: SceneModel; onDeleteMember?: (index: number) => void }) {
  const xs = scene.nodes.map((node) => node.x);
  const ys = scene.nodes.map((node) => node.y);
  const minX = Math.min(...xs, 0);
  const maxX = Math.max(...xs, 1);
  const minY = Math.min(...ys, 0);
  const maxY = Math.max(...ys, 1);
  const project = (x: number, y: number) => ({
    x: 40 + ((x - minX) / Math.max(maxX - minX, 1)) * 520,
    y: 300 - ((y - minY) / Math.max(maxY - minY, 1)) * 240
  });

  return (
    <svg className="diagram" viewBox="0 0 600 340" role="img" aria-label="2D structural diagram">
      {scene.members.map((member, index) => {
        const a = scene.nodes.find((node) => node.id === member.a)!;
        const b = scene.nodes.find((node) => node.id === member.b)!;
        const pa = project(a.x, a.y);
        const pb = project(b.x, b.y);
        return <line key={`${member.a}-${member.b}-${index}`} x1={pa.x} y1={pa.y} x2={pb.x} y2={pb.y} className="member" onClick={() => onDeleteMember?.(index)} role={onDeleteMember ? "button" : undefined} aria-label={onDeleteMember ? `Delete member ${member.a}-${member.b}` : undefined} />;
      })}
      {scene.nodes.map((node) => {
        const point = project(node.x, node.y);
        return <g key={node.id}><circle cx={point.x} cy={point.y} r="7" className="node" /><text x={point.x + 10} y={point.y - 10}>{node.id}</text></g>;
      })}
    </svg>
  );
}
