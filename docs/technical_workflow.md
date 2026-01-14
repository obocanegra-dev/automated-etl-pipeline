# Technical Workflow Documentation

## 1. Pipeline Overview
This ETL pipeline automates the migration of legacy medical/veterinary files. It acts as a middleware between local legacy dumps and modern cloud storage.

## 2. Architecture Components

### Extraction (`src/extractor.py`)
- Monitors the `data/source` directory.
- Detects new files dropped by the simulation script.

### Validation (`src/validator.py`)
- **Regex Rule**: `^(\d+)_([A-Z]+)_(\d{8})\.(.+)$`
- **Logic**: 
  - Extracts ID, TYPE, and DATE.
  - Checks for valid extensions (.pdf, .jpg, .png, .docx, .txt).
- **Failure Handling**: Moves invalid files to `data/error`.

### Load (`src/cloud_connector.py`, `src/sftp_connector.py`)
- **AWS S3**: Uploads using `boto3`.
- **Azure Blob**: Uploads using `azure-storage-blob`.
- **SFTP**: Uploads using `paramiko`.
- **Mock Mode**: If valid credentials are missing in `config.yaml`, the system logs the "upload" without making network calls.

## 3. Directory Lifecycle
1. **Source**: Files arrive here.
2. **Stage**: Valid files are moved here temporarily.
3. **Archive**: Successfully uploaded files are moved here.
4. **Error**: Invalid files are quarantined here.

## 4. How to Run
1. **Simulate Data**: 
   ```powershell
   .\scripts\simulate_extraction.ps1
   ```
2. **Run Pipeline**:
   ```bash
   python main.py
   ```
3. **Check Results**:
   - `data/archive` should contain valid files (e.g., `1001_LAB_20231025.pdf`).
   - `data/error` should contain invalid files (e.g., `unknown_file.txt`).
   - `pipeline.log` will show upload details.
