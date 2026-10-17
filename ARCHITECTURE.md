# Truss-Vision Architecture

## Decision summary

Truss-Vision uses a React + Vite + TypeScript frontend and a Python FastAPI backend during the migration into the upstream simulator fork.

The frontend accepts one picture of one statics problem at a time. The backend sends the image to a hosted Gemma vision model, validates the returned scene, and runs only supported educational calculations.

The canonical submission repository is the GitHub fork of `VictorKaraboychev/statics-simulator`. Its truss solver remains the open-source foundation. The teammate's Mark V application is the behavior and visual reference: its scene format, demo fixtures, extraction prompt, sanitization logic, Canvas interactions, and solver behavior are being migrated into the fork.

## Frameworks

### Frontend

- React
- Vite
- TypeScript
- Canvas or SVG for editable 2D diagrams
- Three.js for the rotatable 3D preview
- No UI framework, Redux store, database, authentication, or routing library for the MVP

### Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- NumPy
- Pytest

The API key stays on the backend in `GOOGLE_AI_API_KEY`. `GEMMA_MODEL` defaults to `gemma-4-26b-a4b-it`, so the demo uses Gemma rather than a Gemini-only model.

## Repository structure

```text
trussvision/
├── README.md
├── SPECIFICATION.md
├── ARCHITECTURE.md
├── LICENSE
├── .gitignore
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/client.ts
│       ├── model/scene.ts
│       ├── model/sceneValidation.ts
│       ├── fixtures/truss.ts
│       ├── components/
│       └── styles/
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── solvers/
│   └── tests/
├── frontend/legacy-mark-v/
│   └── Mark V source retained during migration
└── scripts/
    └── start-dev.ps1
```

## Data flow

```text
Image upload -> client compression -> POST /api/analyze -> Gemma
-> Pydantic validation -> review/correction -> POST /api/solve
-> supported solver -> 2D Canvas / Three.js / results panel
```

## API contracts

### `GET /api/health`

```json
{ "status": "ok" }
```

### `POST /api/analyze`

Multipart form upload containing one PNG, JPG, or WebP image. Returns a validated scene, warnings, source, and confidence.

### `POST /api/solve`

Accepts a confirmed scene. Returns calculated results for supported trusses, simple beams, and spatial resultants. Unsupported cases return `visualization_only` with an explanation.

## Input policy

The public MVP accepts one picture of one problem. The provided PDFs are private test material; export an individual page to an image before uploading. Full exams and problem-set PDFs are intentionally outside the public upload contract.

## Migration order

1. Preserve Mark V fixtures and visual language.
2. Define shared TypeScript and Pydantic scene models.
3. Port scene validation and the 2D renderer.
4. Port truss and beam solvers to tested Python modules.
5. Add the Gemma adapter and review gate.
6. Replace custom 3D projection with a minimal Three.js preview.
7. Remove the legacy copy only after feature parity is verified.
