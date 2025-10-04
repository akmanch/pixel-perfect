from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
import logging
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.datadog_integration import dd_logger, track_api_call, track_ad_generation
from Web_scraping.llinkupscraper import LinkupScraper
from Web_scraping.schema import TeammateOutput

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Social Media Ad Generator API",
    description="AI-powered social media ad generation with competitor analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Linkup Scraper
try:
    linkup_scraper = LinkupScraper()
    logger.info("✅ Linkup Scraper initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Linkup Scraper: {e}")
    linkup_scraper = None

# Pydantic models for request/response
class ScrapeRequest(BaseModel):
    competitor_url: str
    product_description: str

class ScrapeResponse(BaseModel):
    success: bool
    data: dict
    message: str

class GenerateCopyRequest(BaseModel):
    product_description: str
    competitor_insights: dict = None
    target_audience: str = "general"
    price_range: str = None
    ad_style: str = None

class GenerateCopyResponse(BaseModel):
    success: bool
    ad_copy: str
    message: str

class GenerateMediaRequest(BaseModel):
    product_description: str
    media_type: str = "image"  # "image" or "video"
    style: str = "modern"

class GenerateMediaResponse(BaseModel):
    success: bool
    media_url: str
    message: str

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "es"  # Spanish by default

class TranslateResponse(BaseModel):
    success: bool
    translated_text: str
    message: str

class TwitterPostRequest(BaseModel):
    text: str
    media_url: str = None

class TwitterPostResponse(BaseModel):
    success: bool
    tweet_url: str
    message: str

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Social Media Ad Generator API is running!"}

@app.post("/scrape-data", response_model=ScrapeResponse)
@track_api_call("scrape-data")
async def scrape_competitor_data(request: ScrapeRequest):
    """Scrape competitor data using Linkup"""
    try:
        if not linkup_scraper:
            raise HTTPException(status_code=500, detail="Linkup Scraper not initialized")
        
        logger.info(f"Scraping data for: {request.product_description}")
        
        # Log to Datadog
        dd_logger.log_event(
            title="Competitor Data Scraping",
            text=f"Scraping competitor data for {request.product_description}",
            tags=[f"product:{request.product_description[:50]}"]
        )
        
        # Parse competitor from URL or use description
        competitor_name = request.competitor_url.split('/')[-1].replace('-', ' ').title() if request.competitor_url else None
        
        # Create TeammateOutput for Linkup scraper
        teammate_data = TeammateOutput(
            product=request.product_description,
            short_description=request.product_description,
            target_audience="general audience",
            objective="competitive analysis",
            primary_platforms=["Instagram", "Facebook"],
            budget="Medium",
            brand_voice="Professional",
            key_messages=["Quality", "Innovation"],
            visual_direction="Modern",
            constraints="None",
            success_metrics=["Engagement"],
            competitors=[competitor_name] if competitor_name else None
        )
        
        # Scrape using Linkup
        scraped_data = linkup_scraper.scrape_for_ad(teammate_data)
        
        # Format response
        response_data = {
            "data_quality": scraped_data.data_quality,
            "competitor_analysis": scraped_data.competitor_analysis,
            "market_gaps": scraped_data.market_gaps,
            "pricing_comparison": scraped_data.pricing_comparison,
            "how_to_beat_them": scraped_data.how_to_beat_them
        }
        
        # Track successful scraping
        dd_logger.increment_counter("scraping.success", tags=[f"product:{request.product_description[:50]}"])
        
        return ScrapeResponse(
            success=True,
            data=response_data,
            message="Competitor data scraped successfully"
        )
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}")
        dd_logger.log_event(
            title="Scraping Error",
            text=f"Failed to scrape data: {str(e)}",
            tags=[f"product:{request.product_description[:50]}", f"error:{type(e).__name__}"],
            alert_type="error"
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/structure-data", response_model=ScrapeResponse)
async def structure_scraped_data(request: ScrapeRequest):
    """Structure scraped data using Structify"""
    try:
        # TODO: Implement Structify API integration
        logger.info("Structuring scraped data")
        
        # Placeholder response
        structured_data = {
            "insights": {
                "top_performing_ads": ["Ad 1", "Ad 2", "Ad 3"],
                "common_cta": "Shop Now",
                "price_range": "$20-50",
                "key_benefits": ["Eco-friendly", "Durable", "Affordable"]
            },
            "recommendations": [
                "Focus on sustainability messaging",
                "Highlight affordability",
                "Use emotional appeal"
            ]
        }
        
        return ScrapeResponse(
            success=True,
            data=structured_data,
            message="Data structured successfully"
        )
    except Exception as e:
        logger.error(f"Error structuring data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-copy", response_model=GenerateCopyResponse)
@track_api_call("generate-copy")
async def generate_ad_copy(request: GenerateCopyRequest):
    """Generate ad copy using OpenAI"""
    try:
        # TODO: Implement OpenAI API integration
        logger.info(f"Generating ad copy for: {request.product_description}")
        
        # Extract product type for tracking
        product_type = request.product_description.split()[0] if request.product_description else "unknown"
        
        # Log to Datadog
        dd_logger.log_event(
            title="Ad Copy Generation",
            text=f"Generating ad copy for {request.product_description[:50]}...",
            tags=[
                f"product_type:{product_type}",
                f"target_audience:{request.target_audience}",
                f"ad_style:{request.ad_style or 'default'}"
            ]
        )
        
        # Enhanced placeholder response using chatbot data
        product_name = request.product_description.title()
        target_audience = request.target_audience.title()
        price_info = f"Starting at {request.price_range}" if request.price_range else "Affordable pricing"
        style_tone = request.ad_style.title() if request.ad_style else "Modern"
        
        # Build competitor insights section
        competitor_section = ""
        if request.competitor_insights:
            insights = request.competitor_insights.get("insights", {})
            if insights:
                competitor_section = f"""
                📊 Market Insights:
                • Top performing ads focus on: {', '.join(insights.get('key_benefits', ['quality', 'value']))}
                • Common CTA: {insights.get('common_cta', 'Shop Now')}
                • Price range: {insights.get('price_range', 'Competitive')}
                """
        
        ad_copy = f"""
        🚀 {product_name}
        
        Perfect for {target_audience}! 
        {price_info} - {style_tone} style that delivers results.
        
        ✨ Why Choose Us:
        • Premium quality that lasts
        • {style_tone} design that stands out
        • {price_info}
        {competitor_section}
        🛒 Get yours today and see the difference!
        #{product_name.replace(' ', '')} #{target_audience.replace(' ', '')} #{style_tone}
        """
        
        # Track successful ad generation
        dd_logger.increment_counter("ad.generation.success", tags=[
            f"product_type:{product_type}",
            f"target_audience:{request.target_audience}",
            f"ad_style:{request.ad_style or 'default'}"
        ])
        
        return GenerateCopyResponse(
            success=True,
            ad_copy=ad_copy.strip(),
            message="Ad copy generated successfully"
        )
    except Exception as e:
        logger.error(f"Error generating copy: {str(e)}")
        dd_logger.log_event(
            title="Ad Generation Error",
            text=f"Failed to generate ad copy: {str(e)}",
            tags=[f"product:{request.product_description[:50]}", f"error:{type(e).__name__}"],
            alert_type="error"
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-media", response_model=GenerateMediaResponse)
async def generate_image_video(request: GenerateMediaRequest):
    """Generate images/videos using Imagepik"""
    try:
        # TODO: Implement Imagepik API integration
        logger.info(f"Generating {request.media_type} for: {request.product_description}")
        
        # Placeholder response
        media_url = f"https://via.placeholder.com/800x600/4CAF50/FFFFFF?text={request.product_description.replace(' ', '+')}"
        
        return GenerateMediaResponse(
            success=True,
            media_url=media_url,
            message=f"{request.media_type.title()} generated successfully"
        )
    except Exception as e:
        logger.error(f"Error generating media: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate", response_model=TranslateResponse)
async def translate_content(request: TranslateRequest):
    """Translate content using DeepL"""
    try:
        # TODO: Implement DeepL API integration
        logger.info(f"Translating text to {request.target_language}")
        
        # Placeholder response
        translated_text = f"[{request.target_language.upper()}] {request.text}"
        
        return TranslateResponse(
            success=True,
            translated_text=translated_text,
            message="Content translated successfully"
        )
    except Exception as e:
        logger.error(f"Error translating content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/post-twitter", response_model=TwitterPostResponse)
async def post_to_twitter(request: TwitterPostRequest):
    """Post to Twitter/X"""
    try:
        # TODO: Implement Twitter API integration
        logger.info("Posting to Twitter")
        
        # Placeholder response
        tweet_url = "https://twitter.com/user/status/1234567890"
        
        return TwitterPostResponse(
            success=True,
            tweet_url=tweet_url,
            message="Posted to Twitter successfully"
        )
    except Exception as e:
        logger.error(f"Error posting to Twitter: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
