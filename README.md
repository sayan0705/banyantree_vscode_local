# BanyanTree Agentic Finance - Local VS Code Project

This folder is a local runnable version of `banyanTreev3_agentic.py` for VS Code.
The original BanyanTree design is preserved: one user query enters the sentiment/router layer, then routes to RAG, AMFI NAV, planner tools, or the agentic equity market workflow.

## Folder Structure

```text
banyantree_vscode_local/
  src/
    banyanTreev3_agentic.py      # Main local entrypoint
    finsage_mcp_server.py        # Generated automatically at runtime
  config/
    tool_permission_policy.json  # Human-in-the-loop tool permission classes
  data/
    kg/                          # Local KG/vector persistence
    memory/                      # Agent memory JSON
    hf_cache/                    # Hugging Face model cache
  logs/                          # Runtime logs
  scripts/
    setup.ps1                    # Create venv and install dependencies
    run.ps1                      # Run the main script
  .vscode/
    launch.json                  # VS Code debug/run config
    settings.json                # Local Python env settings
```

## Setup

From this folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

If `faiss-cpu` fails on native Windows, use WSL or install FAISS through Conda:

```powershell
conda install -c conda-forge faiss-cpu
```

## Run

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run.ps1
```

Or open the folder in VS Code and run the `BanyanTree Agentic Local` debug configuration.

## GPU Mode

This project is configured to run `Qwen/Qwen2.5-7B-Instruct` locally. Use a CUDA-enabled NVIDIA GPU machine for the full agent run.

## Financial KG Docs

Seed financial documents live outside code:

```text
data/financial_kg/raw_docs/seed/personal_finance_seed.json
```

PageIndex-style structure JSON files can be staged here:

```text
data/financial_kg/pageindex/structures/
```

Optional PageIndex ingestion dependencies are separate from the normal app:

```powershell
git clone https://github.com/VectifyAI/PageIndex.git external/PageIndex
python -m pip install -r external/PageIndex/requirements.txt
```

On Kaggle, if PageIndex dependency pins conflict, use:

```bash
bash scripts/setup_pageindex_kaggle.sh
```

PageIndex indexing is an offline step. It should be run only when source PDFs/Markdown/text files change:

```powershell
python .\scripts\run_pageindex_indexing.py
```

Flatten PageIndex structures into LightRAG-ready docs:

```powershell
python .\scripts\import_pageindex_docs.py
```

The flattened output is written to:

```text
data/financial_kg/raw_docs/pageindex/pageindex_flattened_docs.json
```

Detailed workflow:

```text
docs/financial_kg_pageindex_workflow.md
```

If you see `ModuleNotFoundError: No module named 'torch'`, do not run with `C:\Users\SChowdhury\AppData\Local\Python\bin\python.exe`. That is your global Python 3.14 interpreter. Run `scripts\setup.ps1`, then select `.venv\Scripts\python.exe` from VS Code's `Python: Select Interpreter`.

This project requires Python 3.10, 3.11, or 3.12 for the pinned PyTorch stack. If setup says Python 3.14 is unsupported, install Python 3.11 and rerun setup.

To verify the active environment:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_env.ps1
```

## Runtime Notes

- The script expects a CUDA GPU for `Qwen/Qwen2.5-7B-Instruct` 4-bit inference.
- Model/cache paths are local under `data/` by default.
- The MCP server is generated from the canonical in-script server code and started on `http://localhost:8000`.
- Human approval policy is loaded from `config/tool_permission_policy.json`.

Key environment variables are documented in `.env.example`.
