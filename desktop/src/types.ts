export interface Model {
    id: string;
    name: string;
    // other properties like context window size could be added here
}

export const supportedModels: Model[] = [
    { id: "gpt-4o", name: "GPT-4o" },
    { id: "gpt-4", name: "GPT-4" },
    { id: "gpt-3.5-turbo", name: "GPT-3.5 Turbo" },
    { id: "claude-3-opus-20240229", name: "Claude 3 Opus" },
    { id: "claude-3-sonnet-20240229", name: "Claude 3 Sonnet" },
    { id: "gemini-1.5-pro-latest", name: "Gemini 1.5 Pro" },
    { id: "grok-1", name: "Grok" },
];

export interface Tolerance {
    type: "percent" | "absolute";
    value: number;
    unit?: string;
}

export interface ToleranceProfile {
    name: string;
    tolerances: Record<string, Tolerance>;
}

export interface DroppedFile extends File {
    path: string;
} 