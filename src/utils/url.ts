
export function normalizePath(path: string): string {
    const normalized = path.replace(/\/+$/, "");
    return normalized || "/";
}
