# TAB Report — Master Build Plan 


0 · VISION
--------------------------------------------------------------------
Desktop .exe (Tauri + React shell, Python worker) that:
• Reviews Excel-origin TAB reports locally (no OCR).  
• Syncs tolerances & rules via a tiny FastAPI cloud service.  
• Marks errors with **yellow highlights** and **red comments/arrows**.  
• Compares re-tests, shows fixed items.  
• Supports GPT-4o, o3, o4, Claude 3, Gemini 2.5 Pro, Grok 4 with token-smart batching.

--------------------------------------------------------------------
1 · ARCHITECTURE
--------------------------------------------------------------------
Desktop EXE (Tauri)
│
├─ UI  – React + Tailwind (shadcn/ui)  
│   ├─ Model Hub (model pick + API key vault)  
│   └─ Tolerance Control Center  
│
├─ Local SQLite  
│
└─ Python Worker  
      • File parser (openpyxl, PyMuPDF, pdfplumber)  
      • Rule engine (YAML)  
      • Token-smart AI gateway  
      • PDF annotator (PyMuPDF)  
      • Fix-Delta comparator
      ▲
      │  WebSocket / REST  (settings sync + version)
      ▼
Cloud Sync Service (FastAPI + Postgres/Supabase)

--------------------------------------------------------------------
2 · KEY MODULES
--------------------------------------------------------------------
1 File Ingestor ................. PDF or Excel, preserve cell addresses  
2 Data-Sheet Library ............ Stores sheet meta & common issues  
3 Tolerance Control Center ...... Flow-type limits; Import TAB Spec (PDF)→profile  
4 Model Hub ..................... GPT-4o / o3 / o4 / Claude 3 / Gemini 2.5 / Grok 4  
5 Token-Smart Chunker ........... size = context * 0.85  
6 Dual-Pass AI Review ........... broad scan → precision pass  
7 Red-Pen Annotator ............. Yellow highlight, red notes/arrows  
8 Fix-Delta Report .............. Visual diff re-test vs original  
9 Teach-the-Tool ................ One-click save missed issue → YAML rule  
10 Cloud Sync ................... /auth /profiles /rules /deltas /versions (Manager role only)

--------------------------------------------------------------------
3 · DEFAULT TOLERANCES
--------------------------------------------------------------------
Supply ±10 %   Return ±10 %   Exhaust ±15 %   OA ±5 %   Coil ΔT ±2 °F

--------------------------------------------------------------------
4 · LOCAL SQLITE SCHEMA
--------------------------------------------------------------------
profiles(id,name,json,version)  
rules(id,profile_id,yaml,version)  
runs(id,profile_id,file_hash,result_json,created_at)  
pending_updates(id,payload_json)

--------------------------------------------------------------------
5 · BUILD & CI STEPS
--------------------------------------------------------------------
1 Scaffold Tauri + React shell   • pnpm create tauri-app  
2 Scaffold Python worker         • poetry init  
3 Parser + annotator unit tests  
4 AI gateway & token chunker  
5 FastAPI sync API (+ docker-compose Postgres)  
6 WebSocket client + offline queue  
7 Hook tolerance UI & profile import  
8 Fix-Delta diff logic  
9 Bundle with PyInstaller → Tauri bundler  
10 GitHub Actions: build MSI, push Docker image (API)  
   (auto-updater URL TODO → https://example.com/tab-crusher-releases)

--------------------------------------------------------------------
6 · OPEN TODOS (provide later)
--------------------------------------------------------------------
• Default profile name (if not “Manager Default”).  
• PDF keyword/page rule to locate tolerance table.  
• Sample anonymized PDF & Excel in /samples/.  
• Real updater bucket URL.  
• EULA / privacy text.

--------------------------------------------------------------------
7 · MVP EXIT CRITERIA
--------------------------------------------------------------------
✓ Annotated PDF ≤ 2 min on 200-page file (modern laptop)  
✓ Tolerance edit syncs to peers ≤ 60 s  
✓ Re-test diff shows corrected items clearly

--------------------------------------------------------------------
8 · CURSOR SUPER-PROMPT
--------------------------------------------------------------------
SYSTEM  
You are an expert full-stack engineer (Tauri, React, Python, FastAPI, DevOps).

GOAL  
Implement the attached “TAB Report Crusher — Master Build Plan (v2)”.

TASKS  
1  Project scaffold: monorepo with  desktop/  (Tauri + Python)  and  cloud/  (FastAPI).  
2  Desktop app  
   • Configure Tauri (Windows) + React (shadcn/ui, Tailwind).  
   • Worker  desktop/worker/review.py  with parser, rule engine, token chunker, AI gateway.  
   • PyMuPDF annotator: yellow highlights, red notes/arrows (unit tests).  
   • SQLite schema + migration script (see §4).  
   • Model Hub & Tolerance Control Center components.  
   • WebSocket sync client with offline queue.  
3  Cloud Sync API  
   • FastAPI  cloud/app.py  with /auth /profiles /rules /deltas /versions.  
   • JWT via python-jose, single “Manager” role.  
   • Dockerfile + docker-compose (Postgres).  
4  CI / CD  
   • GitHub Actions: build Tauri MSI, upload artifact; build & push Docker image.  
   • Configure auto-updater for  https://example.com/tab-crusher-releases   // TODO.  
5  Tests  
   • Jest test for React login.  
   • Pytest E2E loads sample_report.pdf (placeholder) → asserts JSON findings.  
6  Docs  
   • README.md (setup, run, add profiles) and CONTRIBUTING.md.  
7  Mark missing inputs with  // TODO:.

OUTPUT FORMAT  
• One Markdown code-fence per created file (header = file path).  
• Use  // TODO:  comments for unfinished parts.  
• Finish with a plain-text checklist of next dev steps.

CONSTRAINTS  
• Follow the Plan unless conflict—mark <!-- deviation -->.  
• Never hard-code API keys; always send vendor privacy flags.  
• Keep line length ≤ 120 chars.

BEGIN
---------------------------------------------------
