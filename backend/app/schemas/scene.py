from typing import Literal

from pydantic import BaseModel, Field


class Node(BaseModel):
    id: str
    x: float
    y: float
    z: float = 0.0
    support: Literal["none", "pin", "roller", "fixed"] = "none"


class Member(BaseModel):
    a: str
    b: str


class Load(BaseModel):
    node: str
    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0
    label: str = ""


class PointLoad(BaseModel):
    x: float
    fy: float
    label: str = ""


class DistributedLoad(BaseModel):
    from_: float = Field(0.0, alias="from")
    to: float = 0.0
    w: float = 0.0
    w_end: float = Field(0.0, alias="wEnd")
    label: str = ""

    model_config = {"populate_by_name": True}


class SceneModel(BaseModel):
    kind: Literal["truss", "beam", "frame2d", "vector3d", "other2d", "unknown"] = "unknown"
    spatial: bool = False
    title: str = "Untitled problem"
    summary: str = ""
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    units: Literal["m", "ft", "in", "relative"] = "relative"
    forceUnit: Literal["kN", "N", "lb", "unknown"] = "unknown"
    nodes: list[Node] = Field(default_factory=list)
    members: list[Member] = Field(default_factory=list)
    loads: list[Load] = Field(default_factory=list)
    pointLoads: list[PointLoad] = Field(default_factory=list)
    distributedLoads: list[DistributedLoad] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    explanation: str = ""


class AnalysisResponse(BaseModel):
    scene: SceneModel
    warnings: list[str] = Field(default_factory=list)
    source: str
    confidence: float


class SolveResponse(BaseModel):
    status: Literal["calculated", "visualization_only"]
    solver: str
    results: dict
    warnings: list[str] = Field(default_factory=list)
