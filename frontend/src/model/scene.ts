export type SceneKind = "truss" | "beam" | "frame2d" | "vector3d" | "other2d" | "unknown";
export type SupportType = "none" | "pin" | "roller" | "fixed";

export interface Node {
  id: string;
  x: number;
  y: number;
  z: number;
  support: SupportType;
}

export interface Member {
  a: string;
  b: string;
}

export interface Load {
  node: string;
  fx: number;
  fy: number;
  fz: number;
  label: string;
}

export interface PointLoad {
  x: number;
  fy: number;
  label: string;
}

export interface DistributedLoad {
  from: number;
  to: number;
  w: number;
  wEnd: number;
  label: string;
}

export interface SceneModel {
  kind: SceneKind;
  spatial: boolean;
  title: string;
  summary: string;
  confidence: number;
  units: "m" | "ft" | "in" | "relative";
  forceUnit: "kN" | "N" | "lb" | "unknown";
  nodes: Node[];
  members: Member[];
  loads: Load[];
  pointLoads: PointLoad[];
  distributedLoads: DistributedLoad[];
  warnings: string[];
  questions: string[];
  explanation: string;
}

export const trussFixture: SceneModel = {
  kind: "truss",
  spatial: false,
  title: "Five-node teaching truss",
  summary: "A planar pin-jointed truss with one downward joint load.",
  confidence: 1,
  units: "m",
  forceUnit: "kN",
  nodes: [
    { id: "A", x: 0, y: 0, z: 0, support: "pin" },
    { id: "B", x: 4, y: 0, z: 0, support: "none" },
    { id: "C", x: 8, y: 0, z: 0, support: "roller" },
    { id: "D", x: 2, y: 3, z: 0, support: "none" },
    { id: "E", x: 6, y: 3, z: 0, support: "none" }
  ],
  members: [
    { a: "A", b: "B" }, { a: "B", b: "C" }, { a: "D", b: "E" },
    { a: "A", b: "D" }, { a: "D", b: "B" }, { a: "B", b: "E" }, { a: "E", b: "C" }
  ],
  loads: [{ node: "B", fx: 0, fy: -50, fz: 0, label: "50 kN down" }],
  pointLoads: [],
  distributedLoads: [],
  warnings: [],
  questions: [],
  explanation: "Fixture mode is available without an AI key. Confirm the model before relying on any result."
};
