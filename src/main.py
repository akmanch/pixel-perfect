from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
import logging
import time
import asyncio
from src.datadog_integration import dd_logger, track_api_call, track_ad_generation

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
        # TODO: Implement Linkup API integration
        logger.info(f"Scraping data for: {request.competitor_url}")
        
        # Log to Datadog
        dd_logger.log_event(
            title="Competitor Data Scraping",
            text=f"Scraping competitor data from {request.competitor_url}",
            tags=[f"competitor_url:{request.competitor_url}", f"product:{request.product_description[:50]}"]
        )
        
        # Placeholder response
        mock_data = {
            "competitor": request.competitor_url,
            "ads_found": 5,
            "common_themes": ["eco-friendly", "premium quality", "affordable"],
            "target_audience": "environmentally conscious consumers"
        }
        
        # Track successful scraping
        dd_logger.increment_counter("scraping.success", tags=[f"competitor:{request.competitor_url}"])
        
        return ScrapeResponse(
            success=True,
            data=mock_data,
            message="Competitor data scraped successfully"
        )
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}")
        dd_logger.log_event(
            title="Scraping Error",
            text=f"Failed to scrape data from {request.competitor_url}: {str(e)}",
            tags=[f"competitor_url:{request.competitor_url}", f"error:{type(e).__name__}"],
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
    """Generate images/videos using Freepik API"""
    try:
        freepik_api_key = os.getenv("FREEPIK_API_KEY")
        if not freepik_api_key:
            raise HTTPException(status_code=500, detail="FREEPIK_API_KEY not configured")

        logger.info(f"Generating {request.media_type} for: {request.product_description}")

        headers = {
            "x-freepik-api-key": freepik_api_key,
            "Content-Type": "application/json"
        }

        # Prepare the request payload for Freepik Imagen3
        payload = {
            "prompt": request.product_description,
            "styling": {
                "color": "vibrant",
                "framing": "close-up",
                "lightning": "studio"
            },
            "num_images": 1
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Submit the image generation task
            response = await client.post(
                "https://api.freepik.com/v1/ai/text-to-image/imagen3",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            # Extract task_id
            task_id = data.get("task_id") or data.get("id")
            if not task_id:
                raise ValueError(f"No task_id found in response: {data}")

            logger.info(f"Freepik task created: {task_id}")

            # Poll for results
            max_attempts = 30
            poll_interval = 2

            for attempt in range(max_attempts):
                await asyncio.sleep(poll_interval)

                poll_response = await client.get(
                    f"https://api.freepik.com/v1/ai/text-to-image/imagen3/{task_id}",
                    headers=headers
                )
                poll_response.raise_for_status()
                result = poll_response.json()

                status = result.get("status")
                logger.info(f"Poll attempt {attempt + 1}: status={status}")

                if status == "completed":
                    generated = result.get("generated", [])
                    if generated:
                        # Handle both string and dict responses
                        media_url = generated[0] if isinstance(generated[0], str) else generated[0].get("url")
                        if media_url:
                            return GenerateMediaResponse(
                                success=True,
                                media_url=media_url,
                                message=f"{request.media_type.title()} generated successfully"
                            )
                    raise ValueError(f"No generated images in completed response: {result}")

                elif status in ["failed", "error"]:
                    error_msg = result.get("error", "Unknown error")
                    raise ValueError(f"Freepik task failed: {error_msg}")

            raise TimeoutError(f"Image generation timed out after {max_attempts * poll_interval} seconds")

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
