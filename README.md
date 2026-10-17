# Truss-Vision

Truss-Vision is an educational statics tool that turns a photo of a student's engineering problem into an interactive structural model.

Students can upload handwritten work or a printed diagram, use Gemma to identify the problem text and structural elements, review and correct the extracted model, and explore it in 2D or 3D.

## MVP features

- Upload a phone photo of a statics problem.
- Extract problem text, nodes, members, supports, and loads with Gemma.
- Review and correct the extracted model before using it.
- Edit nodes and members in an interactive 2D diagram.
- Visualize point loads, distributed loads, reactions, tension, and compression.
- Preview the same model in a simple rotatable 3D view.
- Calculate basic reactions and axial forces for supported 2D determinate trusses.
- Explain when a model is ambiguous or outside the supported calculation scope.

The visual theme is Halloween-inspired: an uncertain scan is a “trick,” while a successful reconstruction is a “treat.”

## Project status

This repository contains the product specification and initial React/FastAPI application structure for the Hacktoberfest Hack Day MVP. The teammate's Mark V implementation is preserved as a migration reference while its scene model, visual language, fixtures, and solver behavior are moved into the open-source simulator fork.

## Open-source foundation

The submission is intended to be an actual GitHub fork of [VictorKaraboychev/statics-simulator](https://github.com/VictorKaraboychev/statics-simulator), an MIT-licensed truss simulator with finite-element analysis and optimization. The upstream solver is the foundation; Truss-Vision adds image extraction, review controls, Gemma analysis, and the Trick-or-Treat experience. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution.

See the complete scope, model contract, schedule, acceptance criteria, and testing plan in [SPECIFICATION.md](SPECIFICATION.md).
See the framework decisions and file layout in [ARCHITECTURE.md](ARCHITECTURE.md).

## Development setup

Open `D:\hacktoberFest` or `trussvision.code-workspace` in VS Code. The repository currently contains the upstream simulator at the root and the Truss-Vision migration prototype under `frontend/`; the next implementation step is to move the Gemma upload/review flow into the root simulator while reusing its solver.

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
$env:GOOGLE_AI_API_KEY = "your-key"
uvicorn app.main:app --reload --port 8000
```

The frontend expects the API at `http://localhost:8000`. Prepared demo fixtures work without an AI key.

The original Mark V implementation is available under [frontend/legacy-mark-v](frontend/legacy-mark-v) while the migration is developed.

## Gemma configuration

The backend calls a hosted Gemma vision model through Google's Gemini API. The default is `gemma-4-26b-a4b-it`; set `GOOGLE_AI_API_KEY` in the backend environment, or use the fixture mode without a key. The key is never sent to the browser. The app treats Gemma output as a proposal that must be reviewed by a human.

For the MLH submission, disclose Gemma, the Gemini API, and any coding assistants used to build the project.

## AI and educational-use notes

Gemma is intended to interpret uploaded images and propose a structured model. The app must show the extracted result for human review rather than silently treating it as exact. Geometry normalization and supported statics calculations should remain deterministic.

Truss-Vision is an educational visualization prototype, not professional engineering software. Results should be checked against course materials and an instructor's guidance.

The public MVP accepts one image of one statics problem. Full exams and course PDFs are not committed or deployed; use private page exports from the local input collection for testing.

## Event context

Built for the 2026 WSU Hacktoberfest Hack Day and the Trick or Treat challenge. The project targets the Best Gemma AI Project and Best Open-Source AI Project tracks.
