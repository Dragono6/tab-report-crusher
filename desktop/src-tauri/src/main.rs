#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use std::process::{Command, Stdio};
use std::io::{BufReader, BufRead};

#[derive(Clone, serde::Serialize)]
struct Payload {
  message: String,
}

#[tauri::command]
fn run_review(file_path: String, api_key: String, model_name: String) -> Result<String, String> {
    // TODO: For production, this path needs to be resolved to the bundled PyInstaller executable.
    let python_executable = "python"; // Assuming python is in the PATH within the dev environment
    let script_path = "../worker/review.py"; // Path relative to src-tauri

    let mut cmd = Command::new(python_executable)
        .arg(script_path)
        .arg(file_path)
        .arg(api_key)
        .arg(model_name)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;

    // Capture stderr for debugging purposes in the main app logs
    if let Some(stderr) = cmd.stderr.take() {
        let reader = BufReader::new(stderr);
        for line in reader.lines() {
            eprintln!("Worker stderr: {}", line.unwrap_or_default());
        }
    }

    let output = cmd.wait_with_output().map_err(|e| e.to_string())?;
    
    if output.status.success() {
        let result_json = String::from_utf8(output.stdout).map_err(|e| e.to_string())?;
        Ok(result_json)
    } else {
        let error_message = String::from_utf8(output.stderr).unwrap_or_else(|_| "Unknown worker error".to_string());
        Err(format!("Worker script failed: {}", error_message))
    }
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_store::Builder::default().build())
        .invoke_handler(tauri::generate_handler![run_review])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
} 