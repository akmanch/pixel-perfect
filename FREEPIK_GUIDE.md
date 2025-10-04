# Freepik API Integration Guide

## 🎨 Overview

This project now includes full integration with **Freepik API** for generating high-quality images and videos for your ad campaigns.

## 🔑 Setup

Your Freepik API key is already configured in `.env`:
```
FREEPIK_API_KEY=FPSX67788b00ff9d4527a86515810961c957
```

## 🚀 Quick Start

### Method 1: Command Line Script (Fastest)

```bash
# Generate an image ad
python generate_ad.py "iPhone 15 Pro with titanium design"

# Generate a video ad
python generate_ad.py "Eco-friendly water bottle" --type video

# Generate with custom aspect ratio
python generate_ad.py "Luxury sports car" --aspect square
```

**Available aspect ratios:**
- `widescreen` (16:9) - Default, best for YouTube, presentations
- `square` (1:1) - Instagram, Facebook posts
- `story` (9:16) - Instagram Stories, TikTok
- `traditional` (3:4) - Print, traditional media

### Method 2: Web Interface (Streamlit)

1. **Start the backend:**
   ```bash
   ./start_backend.sh
   # Or manually: uvicorn src.main:app --reload --port 8000
   ```

2. **Start the frontend:**
   ```bash
   ./start_frontend.sh
   # Or manually: streamlit run src/app.py --server.port 8501
   ```

3. **Open your browser:**
   ```
   http://localhost:8501
   ```

4. **Generate your ad:**
   - Enter product description
   - Select media type (image or video)
   - Click "Generate Complete Ad"
   - Preview and download!

### Method 3: API Endpoints (Direct)

**Generate Image:**
```bash
curl -X POST http://localhost:8000/generate-media \
  -H "Content-Type: application/json" \
  -d '{
    "product_description": "iPhone 15 Pro with titanium design",
    "media_type": "image",
    "style": "modern"
  }'
```

**Generate Video:**
```bash
curl -X POST http://localhost:8000/generate-media \
  -H "Content-Type: application/json" \
  -d '{
    "product_description": "Eco-friendly water bottle",
    "media_type": "video",
    "style": "modern"
  }'
```

## 📊 How It Works

### Image Generation Flow

1. **Request** → Send product description to Freepik Imagen3 API
2. **Processing** → AI generates high-quality image (5-15 seconds)
3. **Polling** → Automatically checks task status every 3 seconds
4. **Result** → Returns URL to generated image

### Video Generation Flow

1. **Step 1: Image** → Generate base image using Imagen3
2. **Step 2: Animation** → Convert image to video using Seedance Pro 1080p
3. **Processing** → AI creates 5-second video (30-90 seconds)
4. **Polling** → Checks status every 5 seconds
5. **Result** → Returns URL to generated video

## 🎯 Example Prompts

### Product Images
```
"Modern smartphone with sleek titanium design on white background"
"Eco-friendly reusable water bottle with bamboo cap"
"Luxury sports car in metallic blue, studio lighting"
"Organic skincare product with natural ingredients"
```

### Video Ads
```
"Premium headphones with active noise cancellation, rotating view"
"Smart watch displaying fitness metrics, close-up"
"Coffee maker brewing fresh espresso, steam rising"
"Running shoes on athletic track, dynamic motion"
```

## 📋 API Response Format

### Successful Image Generation
```json
{
  "success": true,
  "media_url": "https://cdn.freepik.com/...",
  "message": "Image generated successfully"
}
```

### Successful Video Generation
```json
{
  "success": true,
  "media_url": "https://cdn.freepik.com/.../video.mp4",
  "message": "Video generated successfully"
}
```

## ⚙️ Configuration Options

### Image Styling (in main.py)
```python
payload = {
    "prompt": "Your product description",
    "num_images": 1,
    "aspect_ratio": "widescreen_16_9",
    "styling": {
        "style": "photo",  # Options: photo, digital-art, anime
        "effects": {
            "color": "vibrant",     # vibrant, pastel, monochrome
            "lightning": "studio",  # studio, warm, natural
            "framing": "closeup"    # closeup, wide, portrait
        }
    },
    "person_generation": "allow_all",
    "safety_settings": "block_none"
}
```

### Video Options
```python
video_payload = {
    "image": "base_image_url",
    "prompt": "Your animation description",
    "duration": "5",  # 5 or 10 seconds
    "aspect_ratio": "widescreen_16_9",
    "frames_per_second": 24
}
```

## 🔧 Troubleshooting

### "FREEPIK_API_KEY not configured"
- Check that `.env` file exists and contains your API key
- Restart the FastAPI server after adding the key

### Image/Video Generation Timeout
- Freepik API may be experiencing high load
- Images typically take 5-15 seconds
- Videos can take 30-90 seconds
- Script automatically retries with polling

### API Rate Limits
- Free tier: 5 USD in credits
- Monitor your usage at https://www.freepik.com/profile/api
- Consider upgrading if you need more generations

## 📚 Resources

- **Freepik API Docs:** https://docs.freepik.com/
- **Get API Key:** https://www.freepik.com/api
- **Imagen3 Endpoint:** https://docs.freepik.com/api-reference/text-to-image/imagen3/post-imagen3
- **Video Endpoint:** https://docs.freepik.com/api-reference/image-to-video/seedance-pro-1080p/post-seedance-pro-1080p

## 🎉 Examples

### Complete Ad Campaign
```bash
# 1. Generate product image
python generate_ad.py "Premium wireless headphones with noise cancellation" --type image --aspect widescreen

# 2. Generate video version
python generate_ad.py "Premium wireless headphones with noise cancellation" --type video

# 3. Generate square version for Instagram
python generate_ad.py "Premium wireless headphones with noise cancellation" --aspect square
```

### Using the Web Interface
1. Open http://localhost:8501
2. Enter: "Premium wireless headphones with noise cancellation"
3. Select "Media Type": image or video
4. Click "Generate Complete Ad"
5. Preview generated media
6. Download or post to social media

## 💡 Tips

1. **Be Specific:** More detailed prompts = better results
2. **Include Context:** Mention background, lighting, angle
3. **Use Keywords:** "professional", "studio lighting", "high quality"
4. **Test Variations:** Try different aspect ratios for different platforms
5. **Video Length:** Keep videos to 5 seconds for faster generation

## 🚀 Next Steps

- Generate ads for your products using the command line tool
- Integrate into your workflow via the web interface
- Use the FastAPI endpoints in your own applications
- Experiment with different styling options
- Create multi-platform ad campaigns (Instagram, YouTube, TikTok)
