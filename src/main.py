from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
import logging
import time
from src.datadog_integration import dd_logger, track_api_call, track_ad_generation
import asyncio

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
        logger.info(f"Generating {request.media_type} for: {request.product_description}")

        freepik_api_key = os.getenv("FREEPIK_API_KEY")
        if not freepik_api_key:
            logger.error("FREEPIK_API_KEY not found in environment variables")
            raise HTTPException(status_code=500, detail="Freepik API key not configured")

        headers = {
            "x-freepik-api-key": freepik_api_key,
            "Content-Type": "application/json"
        }

        if request.media_type == "image":
            # Text-to-Image using Imagen3
            url = "https://api.freepik.com/v1/ai/text-to-image/imagen3"

            # Map style to aspect ratio
            aspect_ratio_map = {
                "modern": "widescreen_16_9",
                "square": "square_1_1",
                "story": "social_story_9_16",
                "traditional": "traditional_3_4"
            }

            payload = {
                "prompt": request.product_description,
                "num_images": 1,
                "aspect_ratio": aspect_ratio_map.get(request.style, "widescreen_16_9"),
                "styling": {
                    "style": "photo",
                    "effects": {
                        "color": "vibrant",
                        "lightning": "studio",
                        "framing": "close-up"
                    }
                },
                "person_generation": "allow_all",
                "safety_settings": "block_none"
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

                result = response.json()
                logger.info(f"Image API response: {result}")

                # Check if task is completed or get task ID
                if result.get("data"):
                    data = result["data"]

                    # Check if images are already available (immediate completion)
                    if isinstance(data, list) and len(data) > 0 and data[0].get("url"):
                        media_url = data[0]["url"]
                    elif data.get("url"):
                        media_url = data["url"]
                    elif data.get("images") and len(data["images"]) > 0:
                        media_url = data["images"][0]["url"]
                    else:
                        # Task is still processing, get task ID
                        task_id = data.get("task_id") or data.get("id") or result.get("id")

                        if not task_id:
                            logger.error(f"No task ID found in response: {result}")
                            raise HTTPException(status_code=500, detail="Failed to get task ID from Freepik API")

                        logger.info(f"Image generation task created: {task_id}")

                        # Poll for completion
                        max_attempts = 20
                        for attempt in range(max_attempts):
                            await asyncio.sleep(5)

                            # Use the correct endpoint for checking task status
                            status_url = f"https://api.freepik.com/v1/ai/text-to-image/imagen3/{task_id}"
                            status_response = await client.get(status_url, headers=headers)

                            # Handle 404 - task might still be initializing
                            if status_response.status_code == 404:
                                logger.info(f"Task not ready yet (404), retrying... (attempt {attempt + 1})")
                                continue

                            status_response.raise_for_status()
                            status_result = status_response.json()

                            logger.info(f"Task status (attempt {attempt + 1}): {status_result}")

                            if status_result.get("data"):
                                task_data = status_result["data"]
                                status = task_data.get("status")

                                if status == "COMPLETED":
                                    # Try different response structures
                                    if task_data.get("generated") and len(task_data["generated"]) > 0:
                                        # Handle both array of URLs and array of objects
                                        generated = task_data["generated"][0]
                                        if isinstance(generated, str):
                                            media_url = generated
                                        elif isinstance(generated, dict):
                                            media_url = generated.get("url")
                                        break
                                    elif task_data.get("images") and len(task_data["images"]) > 0:
                                        media_url = task_data["images"][0]["url"]
                                        break
                                    elif isinstance(task_data.get("result"), list) and len(task_data["result"]) > 0:
                                        media_url = task_data["result"][0]["url"]
                                        break
                                    elif task_data.get("url"):
                                        media_url = task_data["url"]
                                        break
                                    else:
                                        logger.error(f"Completed but no URL found in: {task_data}")
                                        raise HTTPException(status_code=500, detail="Image URL not found in completed task")
                                elif status == "FAILED":
                                    raise HTTPException(status_code=500, detail="Image generation failed")
                        else:
                            raise HTTPException(status_code=500, detail="Image generation timeout")
                else:
                    raise HTTPException(status_code=500, detail="Invalid response from Freepik API")

            return GenerateMediaResponse(
                success=True,
                media_url=media_url,
                message="Image generated successfully"
            )

        elif request.media_type == "video":
            # For video, we first need to generate an image, then convert to video
            # Step 1: Generate image first
            image_url = "https://api.freepik.com/v1/ai/text-to-image/imagen3"

            image_payload = {
                "prompt": request.product_description,
                "num_images": 1,
                "aspect_ratio": "widescreen_16_9",
                "styling": {
                    "style": "photo",
                    "effects": {
                        "color": "vibrant",
                        "lightning": "studio",
                        "framing": "close-up"
                    }
                }
            }

            async with httpx.AsyncClient(timeout=180.0) as client:
                # Generate base image
                image_response = await client.post(image_url, json=image_payload, headers=headers)
                image_response.raise_for_status()
                image_result = image_response.json()

                logger.info(f"Video base image API response: {image_result}")

                # Get image URL (wait for completion if needed)
                data = image_result.get("data")
                if data:
                    # Check if images are already available
                    if isinstance(data, list) and len(data) > 0 and data[0].get("url"):
                        base_image_url = data[0]["url"]
                    elif data.get("url"):
                        base_image_url = data["url"]
                    elif data.get("generated") and len(data["generated"]) > 0:
                        generated = data["generated"][0]
                        base_image_url = generated if isinstance(generated, str) else generated.get("url")
                    else:
                        # Get task ID and poll
                        task_id = data.get("task_id") or data.get("id")

                        if not task_id:
                            logger.error(f"No task ID found for video base image: {image_result}")
                            raise HTTPException(status_code=500, detail="Failed to get task ID for base image")

                        logger.info(f"Video base image task created: {task_id}")

                        # Wait for image generation
                        for attempt in range(15):
                            await asyncio.sleep(5)
                            status_url = f"https://api.freepik.com/v1/ai/text-to-image/imagen3/{task_id}"
                            status_response = await client.get(status_url, headers=headers)

                            if status_response.status_code == 404:
                                logger.info(f"Base image task not ready yet (404), retrying...")
                                continue

                            status_response.raise_for_status()
                            status_result = status_response.json()

                            logger.info(f"Base image task status (attempt {attempt + 1}): {status_result}")

                            if status_result.get("data"):
                                task_data = status_result["data"]
                                if task_data.get("status") == "COMPLETED":
                                    if task_data.get("generated") and len(task_data["generated"]) > 0:
                                        generated = task_data["generated"][0]
                                        base_image_url = generated if isinstance(generated, str) else generated.get("url")
                                        break
                        else:
                            raise HTTPException(status_code=500, detail="Base image generation timeout")
                else:
                    raise HTTPException(status_code=500, detail="Invalid response for base image generation")

                # Step 2: Convert image to video
                logger.info(f"Generating video from base image: {base_image_url}")
                video_url = "https://api.freepik.com/v1/ai/image-to-video/seedance-pro-1080p"
                video_payload = {
                    "image": base_image_url,
                    "prompt": request.product_description,
                    "duration": "5",
                    "aspect_ratio": "widescreen_16_9",
                    "frames_per_second": 24
                }

                video_response = await client.post(video_url, json=video_payload, headers=headers)
                video_response.raise_for_status()
                video_result = video_response.json()

                logger.info(f"Video generation API response: {video_result}")

                # Wait for video generation
                video_data = video_result.get("data")
                if not video_data:
                    raise HTTPException(status_code=500, detail="Invalid video generation response")

                video_task_id = video_data.get("task_id") or video_data.get("id")

                if not video_task_id:
                    logger.error(f"No video task ID found: {video_result}")
                    raise HTTPException(status_code=500, detail="Failed to get video task ID")

                logger.info(f"Video generation task created: {video_task_id}")

                for attempt in range(30):  # Videos take longer - up to 150 seconds
                    await asyncio.sleep(5)

                    status_url = f"https://api.freepik.com/v1/ai/image-to-video/seedance-pro-1080p/{video_task_id}"
                    status_response = await client.get(status_url, headers=headers)

                    if status_response.status_code == 404:
                        logger.info(f"Video task not ready yet (404), retrying... (attempt {attempt + 1}/30)")
                        continue

                    status_response.raise_for_status()
                    status_result = status_response.json()

                    logger.info(f"Video task status (attempt {attempt + 1}): {status_result}")

                    if status_result.get("data"):
                        task_data = status_result["data"]
                        status = task_data.get("status")

                        if status == "COMPLETED":
                            # Try different response structures for video
                            if task_data.get("generated") and len(task_data["generated"]) > 0:
                                generated = task_data["generated"][0]
                                media_url = generated if isinstance(generated, str) else generated.get("url")
                                break
                            elif task_data.get("video") and task_data["video"].get("url"):
                                media_url = task_data["video"]["url"]
                                break
                            elif task_data.get("url"):
                                media_url = task_data["url"]
                                break
                            else:
                                logger.error(f"Video completed but no URL found: {task_data}")
                                raise HTTPException(status_code=500, detail="Video URL not found in completed task")
                        elif status == "FAILED":
                            raise HTTPException(status_code=500, detail="Video generation failed")
                else:
                    raise HTTPException(status_code=500, detail="Video generation timeout (150 seconds)")

            return GenerateMediaResponse(
                success=True,
                media_url=media_url,
                message="Video generated successfully"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid media_type. Must be 'image' or 'video'")

    except httpx.HTTPStatusError as e:
        logger.error(f"Freepik API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Freepik API error: {e.response.text}")
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
