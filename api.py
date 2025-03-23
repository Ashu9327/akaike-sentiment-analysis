from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Paths for JSON files and audio folder
ANALYSIS_FILE = "data/CompanyAnalysis.json"
NEWS_FILE = "data/Company.json"
AUDIO_FOLDER = "data/audio"

# Ensure audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.get("/get_sentiment/{company_name}")
def get_sentiment_analysis(company_name: str):
    """Fetch sentiment analysis for a specific company."""
    try:
        with open(ANALYSIS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise HTTPException(status_code=500, detail="Invalid JSON format")

        company_analysis = data.get(company_name)
        if not company_analysis:
            raise HTTPException(status_code=404, detail="Company not found")

        return company_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_news/{company_name}")
def get_company_news(company_name: str):
    """Fetch news articles for a specific company."""
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as file:
            news_data = json.load(file)

        if not isinstance(news_data, dict):
            raise HTTPException(status_code=500, detail="Invalid JSON format")

        company_news = news_data.get(company_name)
        if not company_news:
            raise HTTPException(status_code=404, detail="No news found for the company")

        return company_news
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_audio/{company_name}")
def get_audio(company_name: str):
    """Retrieve pre-generated sentiment analysis audio for the company."""
    try:
        audio_file_name = f"{company_name}_sentiment.mp3"
        audio_file_path = os.path.join(AUDIO_FOLDER, audio_file_name)

        if not os.path.exists(audio_file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")

        return FileResponse(audio_file_path, media_type="audio/mpeg", filename=audio_file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)