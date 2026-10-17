from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import GEMMA_MODEL, MAX_IMAGE_BYTES
from app.schemas.scene import AnalysisResponse, SceneModel, SolveResponse
from app.services.gemma_provider import analyze_image
from app.services.scene_normalizer import normalize_scene
from app.solvers.truss import solve_truss


app = FastAPI(title="Truss-Vision API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": GEMMA_MODEL}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(image: UploadFile = File(...)) -> AnalysisResponse:
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=415, detail="Upload one PNG, JPG, or WebP image.")
    contents = await image.read()
    if len(contents) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image is too large. Crop to one problem and try again.")
    try:
        scene = normalize_scene(await analyze_image(contents, image.content_type))
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    return AnalysisResponse(scene=scene, warnings=scene.warnings, source="gemma", confidence=scene.confidence)


@app.post("/api/solve", response_model=SolveResponse)
def solve(scene: SceneModel) -> SolveResponse:
    if scene.kind == "truss":
        try:
            return SolveResponse(status="calculated", solver="planar_truss_stiffness", results=solve_truss(scene), warnings=scene.warnings)
        except ValueError as error:
            return SolveResponse(status="visualization_only", solver="planar_truss_stiffness", results={}, warnings=[*scene.warnings, str(error)])
    return SolveResponse(status="visualization_only", solver="none", results={}, warnings=[*scene.warnings, "This problem type is not numerically solved by the MVP."])
