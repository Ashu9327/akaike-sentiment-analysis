# Company Sentiment Analysis

## Overview

This project provides a **Company Sentiment Analysis** tool with a **Streamlit frontend** and a **FastAPI backend**. It fetches sentiment analysis and news data for companies and provides an **audio summary** of the sentiment analysis.

## Features

- **Streamlit Frontend**: User-friendly UI for selecting companies and viewing sentiment analysis.
- **FastAPI Backend**: Provides APIs to fetch sentiment data, news, and audio summaries.
- **Clipboard Copy**: Easily copy sentiment data.
- **Audio Summary**: Play sentiment analysis audio.

## Project Structure

```
├── app.py            # Streamlit frontend
├── api.py            # FastAPI backend
├── utils.py          # Utility functions
├── requirements.txt  # Dependencies
├── README.md         # Setup and usage instructions
```

## Installation

### 1️⃣ Clone the Repository
```sh
git clone <repository_url>
cd <repository_name>
```

### 2️⃣ Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## Running the Application

### 1️⃣ Start the FastAPI Backend
```sh
python api.py
```
The backend will run at **http://127.0.0.1:8001/api/**

### 2️⃣ Start the Streamlit Frontend
Open a new terminal (keeping FastAPI running) and run:
```sh
streamlit run app.py
```
The frontend will be available at **http://127.0.0.1:8501/**

## Usage

1. Open **http://127.0.0.1:8501/** in your browser.
2. Select a company from the dropdown.
3. View sentiment analysis data.
4. Click the **Copy** button to copy data to the clipboard.
5. Listen to the **sentiment audio summary**.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/get_sentiment/{company}` | GET | Fetch sentiment analysis for a company |
| `/api/get_news/{company}` | GET | Retrieve the latest news for a company |
| `/api/get_audio/{company}` | GET | Get sentiment audio summary |
