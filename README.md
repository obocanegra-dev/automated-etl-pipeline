# Automated ETL Pipeline for File Migration (Simulated PIMS Workflow)

## Overview
This project simulates an end-to-end ELT solution for migrating medical/veterinary data files from a legacy system to modern cloud storage (AWS S3, Azure Blob) and SFTP servers. It includes file validation, normalization, and secure transfer simulations.

## Key Features (CV Highlights)

- **Scripting & Automation**: 
  - Python-based `FileExtractor` for real-time directory monitoring.
  - PowerShell (`simulate_extraction.ps1`) to simulate legacy system data dumps.
  
- **Data Validation & Integrity**: 
  - Implements **100% integrity checks** using Regex logic (`validator.py`).
  - Enforces naming conventions (`ID_TYPE_DATE`) and file type adjustments before the load phase.

- **Cloud Integration**: 
  - Modular connectors for **Amazon S3** (`boto3`) and **Azure Blob Storage**.
  - Includes a "Mock Mode" feature to allow local testing and demonstration without active cloud credentials.

- **Secure Transfer**: 
  - Automated **SFTP** client using `paramiko` for secure file delivery.
  - Verifies successful staging before archiving.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `config/config.yaml`. Default is "mock" mode.

## Usage
(Instructions to be added as scripts are developed)
