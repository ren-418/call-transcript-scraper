# AI Sales Call Evaluator

This project automates the extraction and evaluation of sales call transcripts from Fathom.video using Selenium and FastAPI. It is designed for integration with Make.com (Integromat) and can be used as a standalone API or as a background batch processor.

## Features
- Receives webhook requests (e.g., from Make.com) and scrapes call transcripts from Fathom.video.
- Returns transcript and call metadata as JSON (with transcript text base64-encoded).
- Supports both instant API and batch/background job processing.

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download ChromeDriver (Required)
**ChromeDriver is NOT included in this repository.**
You must download the version of ChromeDriver that matches your installed version of Google Chrome:

- Check your Chrome version: Open Chrome and go to `chrome://settings/help`.
- Download the matching ChromeDriver from: https://googlechromelabs.github.io/chrome-for-testing/
- Extract the `chromedriver.exe` (Windows) or binary to the `chromedriver-win64/` directory in this project.

> **If the versions do not match, Selenium will fail to launch Chrome.**

### 3. (Optional) Install Playwright (if needed)
If you use Playwright elsewhere, you can install it with:
```bash
playwright install
```

## Running the Project

### Run the FastAPI Server (for instant API)
```bash
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000/webhook`.

### Run Both API and Batch Worker
```bash
python server.py
```
- This will start both the FastAPI server and the Selenium worker for batch jobs.

## Make.com Integration
- Use the `/webhook` endpoint as a webhook in Make.com.
- The response will include `closer_name`, `closer_email`, `transcript_text` (base64), and `date_of_call`.
- Map only these fields in your Make.com HTTP module to avoid 422 errors.

## Troubleshooting
- **ChromeDriver/Chrome version mismatch:** Ensure your ChromeDriver matches your installed Chrome version.
- **Browser does not open or closes immediately:** This is usually a version mismatch or missing ChromeDriver.
- **422 Unprocessable Entity from downstream server:** Only send the expected fields (`closer_name`, `closer_email`, `transcript_text`, `date_of_call`). Do not include extra fields like `error`.
- **Network/proxy errors:** If you see `net::ERR_TUNNEL_CONNECTION_FAILED`, check your network, proxy, or VPN settings.

## FAQ
- **Where do I put ChromeDriver?**
  - Place the binary in the `chromedriver-win64/` directory in this project.
- **Can I use this without Make.com?**
  - Yes, you can POST directly to the `/webhook` endpoint.
- **Is the transcript text encoded?**
  - Yes, it is base64-encoded in the API response.

---

For further help, please open an issue or contact the maintainer.