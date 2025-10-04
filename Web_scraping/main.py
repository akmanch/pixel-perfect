from fastapi import FastAPI, HTTPException
from linkup_scraper import LinkupScraper
from schema import TeamInputData, ScrapedData
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Linkup Web Scraper API",
    description="Receives classified data, returns scraped web data",
    version="1.0.0"
)

# Initialize scraper (Linkup only, no OpenAI)
try:
    scraper = LinkupScraper(linkup_api_key=os.getenv("LINKUP_API_KEY"))
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    scraper = None

@app.get("/")
async def root():
    return {
        "service": "Linkup Web Scraper",
        "status": "running",
        "role": "Receives classified data from teammate, scrapes web",
        "endpoints": {
            "scrape": "POST /scrape",
            "health": "GET /health"
        }
    }

@app.post("/scrape", response_model=ScrapedData)
async def scrape_web_data(team_input: TeamInputData):
    """
    Receives classified data from teammate's OpenAI processing,
    scrapes web with Linkup, returns factual data
    
    Example input from teammate:
    {
      "ad_type": "event",
      "subject": "Google Hackathon",
      "category": "tech",
      "target_audience": "developers",
      "extracted_features": ["AI", "$10K prize"]
    }
    """
    
    if not scraper:
        raise HTTPException(
            status_code=500,
            detail="Scraper not initialized. Check LINKUP_API_KEY in .env"
        )
    
    try:
        scraped_data = scraper.scrape_data(team_input)
        return scraped_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scraping error: {str(e)}"
        )

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "linkup_configured": bool(os.getenv("LINKUP_API_KEY"))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)