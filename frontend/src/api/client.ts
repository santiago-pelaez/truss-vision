import type { SceneModel } from "../model/scene";

const jsonRequest = async <T>(url: string, body: unknown): Promise<T> => {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail ?? data.error ?? "Request failed.");
  return data as T;
};

export async function analyzeImage(file: File) {
  const form = new FormData();
  form.append("image", file);
  const response = await fetch("/api/analyze", { method: "POST", body: form });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail ?? data.error ?? "Analysis failed.");
  return data as { scene: SceneModel; warnings: string[]; source: string; confidence: number };
}

export function solveScene(scene: SceneModel) {
  return jsonRequest<{ status: string; solver: string; results: unknown; warnings: string[] }>("/api/solve", scene);
}
