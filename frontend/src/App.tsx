import { useState } from "react";
import { analyzeImage, solveScene } from "./api/client";
import Diagram2D from "./components/Diagram2D";
import Preview3D from "./components/Preview3D";
import { trussFixture, type SceneModel } from "./model/scene";
import { validateScene } from "./model/sceneValidation";

export default function App() {
  const [scene, setScene] = useState<SceneModel>(trussFixture);
  const [message, setMessage] = useState("Fixture loaded. Upload one image of one problem to analyze it.");
  const [results, setResults] = useState<unknown>(null);
  const [show3d, setShow3d] = useState(false);

  async function onUpload(file?: File) {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setMessage("Please upload one PNG, JPG, or WebP image.");
      return;
    }
    try {
      const response = await analyzeImage(file);
      setScene(validateScene(response.scene));
      setMessage("AI extraction complete. Review the scene before solving.");
      setResults(null);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Analysis failed.");
    }
  }

  async function calculate() {
    try {
      setResults(await solveScene(scene));
      setMessage("Calculation complete. Check warnings before relying on results.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Calculation failed.");
    }
  }

  function deleteMember(index: number) {
    const member = scene.members[index];
    if (!member) return;
    setScene({ ...scene, members: scene.members.filter((_, memberIndex) => memberIndex !== index) });
    setResults(null);
    setMessage(`Removed member ${member.a}-${member.b}. Review the model before calculating.`);
  }

  return (
    <main className="app-shell">
      <header><p className="eyebrow">STRUCTURAL INTELLIGENCE // HACKTOBERFEST</p><h1>Truss-Vision</h1><p>Turn one statics problem image into a reviewable structural model.</p></header>
      <section className="controls panel">
        <label className="upload">Upload one problem image<input type="file" accept="image/png,image/jpeg,image/webp" onChange={(event) => onUpload(event.target.files?.[0])} /></label>
        <button onClick={() => { setScene(trussFixture); setResults(null); setMessage("Fixture restored."); }}>Load fixture</button>
        <button onClick={() => setShow3d((value) => !value)}>{show3d ? "Show 2D" : "Show 3D"}</button>
        <button onClick={calculate}>Calculate supported case</button>
      </section>
      <p className="status">{message}</p>
      <section className="workspace">
        <div className="panel diagram-panel"><h2>{show3d ? "3D preview" : "Review model"}</h2>{show3d ? <Preview3D scene={scene} /> : <><p className="hint">Click a member to delete it. This is a review step, so confirm the geometry before calculating.</p><Diagram2D scene={scene} onDeleteMember={deleteMember} /></>}</div>
        <aside className="panel details"><h2>{scene.title}</h2><p>{scene.summary}</p><dl><dt>Type</dt><dd>{scene.kind}</dd><dt>Nodes / members</dt><dd>{scene.nodes.length} / {scene.members.length}</dd><dt>Confidence</dt><dd>{Math.round(scene.confidence * 100)}%</dd></dl><h3>Warnings</h3>{scene.warnings.length ? <ul>{scene.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul> : <p>No warnings.</p>}<h3>Results</h3><pre>{results ? JSON.stringify(results, null, 2) : "Confirm the model, then calculate."}</pre></aside>
      </section>
    </main>
  );
}
