# TAB Report Crusher

Desktop tool to review and annotate TAB reports with AI assistance.

## Overview

This project is a Tauri-based desktop application with a React frontend and a Python backend. It allows for local analysis of TAB (Testing, Adjusting, and Balancing) reports in PDF or Excel format.

- **Local First**: All report data stays on your machine. No cloud uploads.
- **AI-Powered Review**: Uses large language models to flag issues in reports.
- **Syncs Settings**: Tolerances and rules are synced from a central cloud service.
- **Annotates PDFs**: Automatically adds highlights and comments to the report.

## Setup and Running

<!-- deviation: Using pnpm as it was specified in the scaffolding command -->
### Prerequisites
- [Node.js](https://nodejs.org/)
- [pnpm](https://pnpm.io/)
- [Python 3.9+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Rust](https://www.rust-lang.org/)

### Desktop App (Tauri + React)

1.  **Navigate to the desktop directory:**
    ```bash
    cd desktop
    ```

2.  **Install dependencies:**
    ```bash
    pnpm install
    ```

3.  **Run in development mode:**
    ```bash
    pnpm tauri dev
    ```

### Python Worker

1.  **Navigate to the worker directory:**
    ```bash
    cd desktop/worker
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```
    
### Cloud Sync Service (FastAPI)

1.  **Navigate to the cloud directory:**
    ```bash
    cd cloud
    ```

2.  **Start the services using Docker:**
    ```bash
    docker-compose up --build
    ```

## Adding Profiles

// TODO: Add instructions on how to add and manage tolerance profiles. 