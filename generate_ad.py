#!/usr/bin/env python3
"""
Quick Ad Generator using Freepik API
Usage: python generate_ad.py "Your product description here" [--type image|video]
"""

import os
import sys
import asyncio
import argparse
import httpx
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")

async def generate_image(prompt: str, aspect_ratio: str = "widescreen_16_9"):
    """Generate an image using Freepik API"""
    if not FREEPIK_API_KEY:
        print("❌ Error: FREEPIK_API_KEY not found in environment variables")
        print("Please add your API key to the .env file")
        return None

    url = "https://api.freepik.com/v1/ai/text-to-image/imagen3"

    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "num_images": 1,
        "aspect_ratio": aspect_ratio,
        "styling": {
            "style": "photo",
            "effects": {
                "color": "vibrant",
                "lightning": "studio",
                "framing": "closeup"
            }
        },
        "person_generation": "allow_all",
        "safety_settings": "block_none"
    }

    print(f"🎨 Generating image for: {prompt}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

            # Check if task is completed or get task ID
            if result.get("data") and result["data"].get("images"):
                image_url = result["data"]["images"][0]["url"]
                print(f"✅ Image generated successfully!")
                print(f"📸 URL: {image_url}")
                return image_url
            else:
                # Task may still be processing
                task_id = result.get("data", {}).get("id")
                print(f"⏳ Image generation task created: {task_id}")
                print(f"⏳ Waiting for completion...")

                # Poll for completion
                max_attempts = 15
                for attempt in range(max_attempts):
                    await asyncio.sleep(3)

                    status_url = f"https://api.freepik.com/v1/ai/tasks/{task_id}"
                    status_response = await client.get(status_url, headers=headers)
                    status_result = status_response.json()

                    status = status_result.get("data", {}).get("status")
                    print(f"   Status: {status} (attempt {attempt + 1}/{max_attempts})")

                    if status == "COMPLETED":
                        image_url = status_result["data"]["images"][0]["url"]
                        print(f"✅ Image generated successfully!")
                        print(f"📸 URL: {image_url}")
                        return image_url
                    elif status == "FAILED":
                        print(f"❌ Image generation failed")
                        return None

                print(f"❌ Image generation timeout")
                return None

        except httpx.HTTPStatusError as e:
            print(f"❌ Freepik API error: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

async def generate_video(prompt: str):
    """Generate a video using Freepik API (image-to-video)"""
    if not FREEPIK_API_KEY:
        print("❌ Error: FREEPIK_API_KEY not found in environment variables")
        return None

    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }

    # Step 1: Generate base image first
    print("📸 Step 1: Generating base image...")
    base_image_url = await generate_image(prompt, aspect_ratio="widescreen_16_9")

    if not base_image_url:
        print("❌ Failed to generate base image for video")
        return None

    # Step 2: Convert image to video
    print("\n🎬 Step 2: Converting image to video...")
    video_url_endpoint = "https://api.freepik.com/v1/ai/image-to-video/seedance-pro-1080p"

    video_payload = {
        "image": base_image_url,
        "prompt": prompt,
        "duration": "5",
        "aspect_ratio": "widescreen_16_9",
        "frames_per_second": 24
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            video_response = await client.post(video_url_endpoint, json=video_payload, headers=headers)
            video_response.raise_for_status()
            video_result = video_response.json()

            # Wait for video generation
            video_task_id = video_result.get("data", {}).get("id")
            print(f"⏳ Video generation task created: {video_task_id}")
            print(f"⏳ Waiting for completion (this may take 1-2 minutes)...")

            max_attempts = 30
            for attempt in range(max_attempts):
                await asyncio.sleep(5)

                status_url = f"https://api.freepik.com/v1/ai/tasks/{video_task_id}"
                status_response = await client.get(status_url, headers=headers)
                status_result = status_response.json()

                status = status_result.get("data", {}).get("status")
                print(f"   Status: {status} (attempt {attempt + 1}/{max_attempts})")

                if status == "COMPLETED":
                    video_url = status_result["data"]["video"]["url"]
                    print(f"✅ Video generated successfully!")
                    print(f"🎬 URL: {video_url}")
                    return video_url
                elif status == "FAILED":
                    print(f"❌ Video generation failed")
                    return None

            print(f"❌ Video generation timeout")
            return None

        except httpx.HTTPStatusError as e:
            print(f"❌ Freepik API error: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

async def main():
    parser = argparse.ArgumentParser(
        description="Generate ad images or videos using Freepik API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_ad.py "iPhone 15 Pro with titanium design"
  python generate_ad.py "Eco-friendly water bottle" --type video
  python generate_ad.py "Luxury sports car" --type image --aspect square
        """
    )

    parser.add_argument("prompt", help="Description of the product/ad to generate")
    parser.add_argument(
        "--type",
        choices=["image", "video"],
        default="image",
        help="Type of media to generate (default: image)"
    )
    parser.add_argument(
        "--aspect",
        choices=["widescreen", "square", "story", "traditional"],
        default="widescreen",
        help="Aspect ratio for image generation (default: widescreen)"
    )

    args = parser.parse_args()

    # Map aspect ratio names to API values
    aspect_ratio_map = {
        "widescreen": "widescreen_16_9",
        "square": "square_1_1",
        "story": "social_story_9_16",
        "traditional": "traditional_3_4"
    }

    print("=" * 60)
    print("🚀 Freepik Ad Generator")
    print("=" * 60)
    print(f"Prompt: {args.prompt}")
    print(f"Type: {args.type}")

    if args.type == "image":
        print(f"Aspect Ratio: {args.aspect}")
        print("=" * 60)
        result = await generate_image(args.prompt, aspect_ratio_map[args.aspect])
    else:
        print("=" * 60)
        result = await generate_video(args.prompt)

    print("=" * 60)

    if result:
        print("\n✅ Generation complete!")
        print(f"📎 Result URL: {result}")

        # Save to file
        output_file = "generated_ad.json"
        output_data = {
            "prompt": args.prompt,
            "type": args.type,
            "url": result
        }

        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"💾 Saved to {output_file}")
    else:
        print("\n❌ Generation failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
