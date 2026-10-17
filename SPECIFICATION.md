# Truss-Vision Product Specification

## Summary

Truss-Vision is a browser-based learning tool that turns a photographed statics problem into an interactive structural visualization.

The core demo is:

1. A student uploads a phone photo of handwritten work, a printed diagram, or both.
2. Gemma reads the problem and proposes a structured model.
3. The student reviews and manually fixes nodes, members, supports, and loads.
4. The app renders the result in 2D.
5. The same model can be viewed as a simpler rotatable 3D scene.
6. Supported 2D cases show visual forces and basic statics calculations.

Gemma 3 and later support image input, OCR, object detection, and coordinate-style outputs, making Gemma suitable for proposing diagram structure. Exact topology must still be validated by deterministic code and reviewed by the student. See the [Gemma image understanding documentation](https://ai.google.dev/gemma/docs/capabilities/vision/image).

## Product scope

### Guaranteed MVP

- Browser application using React and TypeScript.
- Python API for Gemma integration, model normalization, and calculations.
- Upload of PNG and JPG images.
- Reading of problem text, node labels, dimensions, supports, point loads, distributed loads, and 2D/3D intent.
- Gemma-generated extraction shown as an editable review model.
- Interactive 2D diagram with:
  - Nodes and members.
  - Pin and roller supports.
  - Point-load arrows.
  - Distributed-load arrows.
  - Labels and dimensions.
  - Node movement.
  - Member creation and deletion.
- Basic statics calculations for 2D planar, statically determinate trusses with pin/roller supports and point loads.
- Simple rotatable 3D preview derived from the same model.
- Warnings for ambiguous scans and unsupported calculations.
- Halloween styling only: dark background, orange/purple accents, “trick” warnings, and “treat” success states.

### Out of scope

- Reliable arbitrary-image understanding for every structure.
- Full finite-element analysis.
- 3D structural calculations.
- Material deformation or stress analysis.
- Complex bridges, machines, frames, or mechanisms beyond demo fixtures.
- Automatic claims that a reconstructed model is exact.
- Authentication, accounts, persistence, and production deployment polish.

## Technical design

### Frontend

The React/TypeScript frontend should contain:

- Upload screen.
- Scan and extraction progress state.
- Review-and-correct model editor.
- 2D visualization panel.
- 3D visualization panel.
- Results and warnings panel.

Use SVG or Canvas for the editable 2D diagram and Three.js for the rotatable 3D preview. Both views must consume the same `ProblemModel` state.

### Backend

Use a small FastAPI service with three isolated components:

- `GemmaVisionAdapter`: sends the image and extraction prompt to the hosted Gemma endpoint and requests structured JSON.
- `ModelNormalizer`: validates JSON, converts image coordinates, snaps nearby endpoints into shared nodes, infers member connectivity, and preserves uncertainty warnings.
- `StaticsSolver`: solves only the supported 2D determinate subset and returns reactions, axial member forces, and warnings.

The Gemma adapter must be replaceable so the project can switch between hosted inference, local inference, and deterministic fixtures without changing the UI.

## Shared model contract

Use one JSON structure across Gemma, the editor, the solver, and both visualizations:

```json
{
  "dimension": "2d",
  "problem_text": "Find the reaction forces and member forces...",
  "nodes": [
    { "id": "A", "x": 0, "y": 0, "z": 0, "confidence": 0.96 }
  ],
  "members": [
    { "id": "AB", "start": "A", "end": "B", "confidence": 0.91 }
  ],
  "supports": [
    { "node": "A", "type": "pin" },
    { "node": "B", "type": "roller", "direction": "x" }
  ],
  "loads": [
    {
      "type": "point",
      "node": "C",
      "magnitude": 10,
      "direction": "down",
      "unit": "kN"
    }
  ],
  "distributed_loads": [],
  "warnings": [],
  "confidence": 0.84
}
```

The frontend must allow this structure to be edited before visualization or solving.

## AI behavior

Prompt Gemma to return only the model schema, including:

- Detected text.
- Candidate nodes and coordinates.
- Candidate member segments.
- Support types.
- Loads and directions.
- Whether the problem appears 2D or 3D.
- Confidence values.
- Uncertainty warnings.

The app must not silently trust the output. The review screen should distinguish:

- Detected from image.
- Needs confirmation.
- Unsupported for calculations.

If Gemma is unavailable, the demo must fall back to two prepared fixtures: one 2D truss and one simple 3D structure.

## User experience flow

### Upload

Display:

> Upload a photo of your statics problem. Truss-Vision will identify the text, nodes, members, supports, and loads.

Include file upload, example image buttons, and an “Analyze with Gemma” action.

### Review

Show the original image beside the extracted model. Allow the user to:

- Edit problem text.
- Add, delete, and move nodes.
- Add and delete members.
- Change support types.
- Add and edit point loads.
- Add and edit distributed loads.
- Toggle 2D/3D interpretation.
- Visualize the model.

### Visualization

Provide tabs for `2D Diagram`, `3D Preview`, and `Forces & Results`.

Recommended visual language:

- Green members: tension.
- Red members: compression.
- Orange arrows: applied loads.
- Purple arrows: reactions.
- Dashed orange regions: distributed loads.
- Warning badges: uncertain or unsupported elements.

## Statics scope

The solver supports only:

- Planar trusses.
- Two-dimensional coordinates.
- Pin and roller supports.
- Point loads applied at nodes.
- Linear equilibrium equations.
- Determinate systems with a solvable number of equations.

Distributed loads should be visualized, but marked as “visualized only” unless the team has time to convert them into equivalent nodal loads.

For unsupported cases, show an explanation such as:

> This model can be visualized, but basic force calculations are unavailable because it contains a 3D connection or an indeterminate structure.

## Demo story

1. Explain that students often understand the equations but struggle to see the structure.
2. Upload a photographed handwritten statics problem.
3. Show Gemma extracting the text and diagram.
4. Show one imperfect detection.
5. Correct a node or support in the review panel.
6. Generate the 2D model.
7. Show calculated reactions and member forces.
8. Switch to the 3D preview.
9. Delete a member and show the model update.
10. Explain that AI interprets the image while deterministic code handles validation and supported calculations.

The “trick” is ambiguity in handwritten engineering diagrams. The “treat” is turning that ambiguity into an interactive model students can understand and correct.

## Hackathon schedule

Assuming a 12:22 p.m. start and a 6:00 p.m. submission deadline:

- 12:22–12:40 — Freeze scope, choose one 2D fixture and one 3D fixture, assign roles.
- 12:40–1:20 — Create the React shell, upload screen, shared model types, and navigation.
- 1:20–2:10 — Build the 2D renderer with nodes, members, supports, and loads.
- 2:10–2:50 — Build the review editor.
- 2:50–3:30 — Implement the Gemma adapter, extraction prompt, JSON validation, and fixture fallback.
- 3:30–4:10 — Implement the basic 2D statics solver.
- 4:10–4:40 — Add the Three.js 3D preview.
- 4:40–5:00 — Add Halloween styling, warnings, loading states, and failure handling.
- 5:00–5:20 — Rehearse the full demo using the real example image and fallback fixture.
- 5:20–5:30 — Fix only blocking bugs.
- 5:30–5:50 — Freeze features, record screenshots or demo video, write the submission description, and verify the GitHub link.
- 5:50–6:00 — Submit. No new features after 5:30.

Suggested team division:

- Person 1: frontend and editor.
- Person 2: 2D/3D visualization.
- Person 3: Gemma/API/model extraction.
- Person 4: statics solver, testing, and submission materials.

## Acceptance criteria

The MVP is ready when:

- A user can upload an image.
- The app calls Gemma or loads a clearly labeled fallback fixture.
- The result appears as editable structured data.
- The user can correct at least one node or member/support.
- The edited structure renders in 2D.
- A simple 3D preview opens and can be rotated.
- A supported 2D truss displays basic reactions and member forces.
- An unsupported model produces a warning instead of a false calculation.
- The complete demo can be finished in under three minutes.
- The app still works if the Gemma endpoint fails.
- The repository includes setup instructions, screenshots, AI disclosure, and the demo path.

## Testing plan

Before the 5:30 feature freeze, test:

1. A clean 2D truss fixture produces the expected nodes and members.
2. Handwritten or low-confidence input produces warnings and opens the review editor.
3. Deleting a member updates the visualization.
4. Moving a node updates connected member geometry.
5. A point load appears in the correct direction.
6. A distributed load renders even when excluded from calculations.
7. A supported determinate truss produces results.
8. An unsupported 3D or indeterminate model is visualized but not falsely solved.
9. Gemma failure activates the prepared fixture fallback.
10. The 3D preview opens from the same model used by the 2D view.

## Assumptions

- This repository is the team’s fork and can be rebuilt into the project.
- The team can access a hosted endpoint running a Gemma vision-capable model.
- Gemma interprets images and provides educational explanation; geometry validation and statics calculations remain deterministic.
- The representative example image has not yet been provided. The initial fixtures should be a clean 2D truss and a simple 3D structure, then adjusted to match the team’s real example.
- Truss-Vision is an educational visualization prototype, not professional engineering software.

## Actual input profile

The expected inputs are scanned or photographed pages from statics coursework, including handwritten notebook work, printed beam diagrams with annotations, frames, centroid and area-moment problems, and 3D vector problems.

The public MVP accepts one picture of one problem at a time. The supplied PDF collection is private test material; individual pages may be exported to images for local testing, but full exams and problem sets must not be committed or publicly deployed.

## Framework and architecture decisions

- Frontend: React, Vite, and TypeScript.
- 2D visualization: Canvas or SVG with direct editing.
- 3D visualization: Three.js preview.
- Backend: Python FastAPI with Pydantic schemas, HTTPX, NumPy, and Pytest.
- AI key: server-side `GOOGLE_AI_API_KEY` environment variable.
- Input contract: one PNG, JPG, or WebP image per analysis request.
- Full PDF parsing, authentication, databases, and general-purpose statics solving remain out of scope for the hackathon MVP.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the repository layout, API boundaries, and migration order.

## Event context

Built for the 2026 WSU Hacktoberfest Hack Day and the Trick or Treat challenge. The project targets the Best Gemma AI Project and Best Open-Source AI Project tracks.
