---
title: Desk Generator
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.28.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# Desk Generator 📊

A Streamlit-based financial report generator that takes uploaded CSV data and builds smart summary output and downloadable reports.

## Features

- Upload finance data as CSV
- Generate insights and summary reports
- Download generated reports
- Includes helper utilities for calculation, report generation, and PDF export

## Quick Start

1. Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run Streamlit:

```bash
streamlit run app.py
```

4. Open the local URL from Streamlit output, typically `http://localhost:8501`.

## Project Structure

- `app.py` - Main Streamlit app UI and flow
- `utils/` - Utility modules:
  - `financial_calculator.py`
  - `llm_handler.py`
  - `pdf_exporter.py`
  - `report_generator.py`
- `data/` - Sample financial data
- `sample_uploads/` - Example input dataset templates

## Notes

- This project is tailored for Streamlit `1.28.0`.
- Use Python 3.11 as specified in app metadata.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Open a PR with your changes

Enjoy building smart desk reports! 🚀