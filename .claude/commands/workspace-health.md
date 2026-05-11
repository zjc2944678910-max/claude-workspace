# workspace-health

Run the workspace health check and summarize the result.

## Steps

1. Run `bash tools/workspace-health.sh` from the workspace root.
2. Read the output sections: **CONFIRMED**, **DRIFT**, **MISSING**, **STALE REFERENCES**.
3. Summarize:
   - If all checks passed, say so briefly.
   - If issues are found, list each category with the specific items.
4. If drift or missing items exist, suggest what edits would fix them.
5. If stale references exist, identify which files need cleanup.
