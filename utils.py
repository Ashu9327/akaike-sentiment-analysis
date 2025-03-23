import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import os
from typing import List, Dict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from concurrent.futures import ThreadPoolExecutor

def clean_url(url: str) -> str:
    """Clean and decode URL if needed."""
    try:
        return urllib.parse.unquote(url)
    except Exception:
        return url

def get_news_articles(company_name: str) -> List[Dict[str, str]]:
    """
    Fetch top 10 news articles about a company from Bing News RSS feed.
    
    Args:
        company_name (str): Name of the company to search for
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing article information
    """
    search_url = f"https://www.bing.com/news/search?q={urllib.parse.quote(company_name)}&format=rss"
    
    try:
        print(f"\nFetching news about {company_name}...")
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml-xml")
        articles = []
        items = soup.find_all('item')[:10]  # Fetch top 10 articles

        print(f"Found {len(items)} news items to process")

        for item in items:
            title = item.title.text if item.title else "No Title"
            url = clean_url(item.link.text if item.link else "")
            summary = item.description.text if item.description else "No Summary"
            publish_date = item.pubDate.text if item.pubDate else "No Date"

            article_data = {
                "title": title,
                "url": url,
                "summary": summary,
                "publish_date": publish_date
            }
            articles.append(article_data)
            print(f"✓ Processed: {title}")

        return articles
        
    except requests.RequestException as e:
        print(f"Error fetching news: {str(e)}")
        return []

def save_articles_to_json(all_articles: Dict[str, List[Dict[str, str]]]):
    """
    Save all company news articles into a single JSON file inside the data folder.
    
    Args:
        all_articles (Dict[str, List[Dict[str, str]]]): Dictionary containing all company news
    """
    folder_name = "data"
    os.makedirs(folder_name, exist_ok=True)  # Create data folder if it doesn't exist
    file_path = os.path.join(folder_name, "Company.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=4)
    
    print(f"\n✅ Successfully saved news for all companies in '{file_path}'")

def analyze_sentiment(text: str) -> str:
    """
    Perform sentiment analysis using VADER.
    
    Args:
        text (str): Article summary/content
    
    Returns:
        str: Sentiment category ('Positive', 'Negative', 'Neutral')
    """
    if not text:
        return "Neutral"  # Default if text is empty

    sia = SentimentIntensityAnalyzer()  # Move inside the function
    sentiment_score = sia.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def perform_sentiment_analysis(input_path: str, output_path: str):
    """
    Perform sentiment analysis on articles from Company.json and save results to SentimentAnalysis.json.
    
    Args:
        input_path (str): Path to Company.json file
        output_path (str): Path to save SentimentAnalysis.json
    """
    if not os.path.exists(input_path):
        print("❌ Error: Company.json not found!")
        return
    
    with open(input_path, "r", encoding="utf-8") as file:
        company_data = json.load(file)

    sentiment_results = {}

    for company, articles in company_data.items():
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        article_analysis = []

        for article in articles:
            title = article.get("title", "No Title")
            summary = article.get("summary", "No Summary")
            
            sentiment = analyze_sentiment(summary)
            sentiment_counts[sentiment] += 1

            article_analysis.append({
                "Title": title,
                "Summary": summary,
                "Sentiment": sentiment
            })

        final_sentiment = "Overall, the company's recent news coverage is mostly "
        if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
            final_sentiment += "positive, indicating a strong outlook."
        elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
            final_sentiment += "negative, signaling potential concerns."
        else:
            final_sentiment += "neutral, with mixed viewpoints."

        sentiment_results[company] = {
            "Company": company,
            "Articles": article_analysis,
            "Sentiment Distribution": sentiment_counts,
            "Final Sentiment Analysis": final_sentiment
        }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(sentiment_results, file, indent=4)
    
    print(f"\n✅ Sentiment analysis saved in '{output_path}'")

def process_company(company, data, output_folder, slow=False):
    """ Generate speech and save audio file for a single company with adjustable speed. """
    if "Final Sentiment Analysis" not in data or "Sentiment Distribution" not in data:
        print(f"⚠️ Skipping {company} (Missing data).")
        return

    speech_text = f"Company: {company}. {data['Final Sentiment Analysis']}. " \
                  + "Sentiment Distribution: " \
                  + " ".join(f"{sentiment}: {count}." for sentiment, count in data["Sentiment Distribution"].items())

    tts = gTTS(text=speech_text, lang="en", slow=slow)
    audio_file_path = os.path.join(output_folder, f"{company}_sentiment.mp3")
    tts.save(audio_file_path)

    print(f"✅ Audio saved for {company} (Slow={slow}): {audio_file_path}")

def generate_speech_from_analysis(input_path, output_folder, slow=False):
    """ Convert CompanyAnalysis.json into speech files concurrently with speed control. """
    if not os.path.exists(input_path):
        print("❌ Error: CompanyAnalysis.json not found!")
        return

    with open(input_path, "r", encoding="utf-8") as file:
        company_analysis = json.load(file)

    os.makedirs(output_folder, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for company, data in company_analysis.items():
            executor.submit(process_company, company, data, output_folder, slow)

# Wrapper Functions
def Scrapper():
    companies = ["Microsoft", "Tesla", "Apple", "Google", "Amazon"]
    all_articles = {company: get_news_articles(company) for company in companies}
    save_articles_to_json(all_articles)

def Sentiment():
    nltk.download('vader_lexicon')
    perform_sentiment_analysis("data/Company.json", "data/CompanyAnalysis.json")

def tts():
    generate_speech_from_analysis("data/CompanyAnalysis.json", "data/audio/")

Scrapper()
Sentiment()
tts()
