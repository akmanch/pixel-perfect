# Social Media Ad Generator - 3-Hour Sprint MVP

A rapid prototype that demonstrates AI-powered social media ad generation using Python, FastAPI, and Streamlit. Built in 3 hours by a team of 4 developers.

## 🚀 Project Overview

**MVP Features (3-Hour Sprint):**
- Generate ad copy using OpenAI Prompting
- Scrape competitor data using Linkup scraping
- Structure scraped data with Structify
- Generate images/videos using Imagepik
- Translate content using DeepL
- Simple web interface for ad creation
- Basic preview and download functionality
- Single social media platform integration (Twitter/X)

## 👥 Team Structure (4 Developers - 3 Hours)

### **Developer 1: Backend API & Data Processing (45 minutes)**
**Responsibilities:**
- Set up FastAPI server
- Create basic API endpoints
- Integrate Linkup scraping for competitor data
- Integrate Structify for data structuring
- Basic error handling

**Key Deliverables:**
- `/scrape-data` endpoint
- `/structure-data` endpoint
- Basic FastAPI server setup

### **Developer 2: Frontend UI (45 minutes)**
**Responsibilities:**
- Create Streamlit web application
- Build ad creation form with Streamlit components
- Add preview functionality
- Implement download buttons
- Basic responsive design with Streamlit

**Key Deliverables:**
- Streamlit single-page application
- Form for ad input using Streamlit widgets
- Preview area for generated content
- Download functionality

### **Developer 3: AI & Content Generation (45 minutes)**
**Responsibilities:**
- Integrate OpenAI Prompting for ad copy generation
- Integrate Imagepik for image/video generation
- Integrate DeepL for content translation
- Create prompt templates
- Handle API responses and error handling

**Key Deliverables:**
- OpenAI Prompting service integration
- Imagepik API integration
- DeepL translation service
- Prompt templates and response processing

### **Developer 4: Twitter Integration & Polish (45 minutes)**
**Responsibilities:**
- Integrate Twitter API for posting
- Add basic styling and UX improvements
- Handle file uploads/downloads
- Test and debug integration
- Final polish and presentation prep

**Key Deliverables:**
- Twitter API integration
- Post to Twitter functionality
- Final UI polish
- Demo-ready application

## 🛠 Technical Architecture (MVP)

### **Tech Stack (3-Hour Sprint):**
- **Backend:** Python with FastAPI
- **Frontend:** Streamlit
- **APIs:** OpenAI Prompting, Linkup scraping, Structify, Imagepik, DeepL, Twitter API
- **No Database:** In-memory storage for demo
- **Deployment:** Local development server

### **API Integration Structure:**
```python
# FastAPI endpoints
@app.post("/scrape-data")
async def scrape_competitor_data():
    pass

@app.post("/structure-data")
async def structure_scraped_data():
    pass

@app.post("/generate-copy")
async def generate_ad_copy():
    pass

@app.post("/generate-media")
async def generate_image_video():
    pass

@app.post("/translate")
async def translate_content():
    pass

@app.post("/post-twitter")
async def post_to_twitter():
    pass
```

## ⏰ 3-Hour Sprint Timeline

### **Hour 1: Foundation & Setup (0-60 minutes)**
- **Minutes 0-15:** Project setup, Python environment configuration
- **Minutes 15-30:** Basic FastAPI server setup
- **Minutes 30-45:** Streamlit frontend structure
- **Minutes 45-60:** API key configuration and basic routing

### **Hour 2: Core Features (60-120 minutes)**
- **Minutes 60-75:** Linkup scraping and Structify integration
- **Minutes 75-90:** OpenAI Prompting and Imagepik integration
- **Minutes 90-105:** Streamlit form and preview components
- **Minutes 105-120:** Basic styling and layout with Streamlit

### **Hour 3: Integration & Polish (120-180 minutes)**
- **Minutes 120-135:** DeepL translation and Twitter API integration
- **Minutes 135-150:** Testing and debugging
- **Minutes 150-165:** UI polish and improvements
- **Minutes 165-180:** Final testing and demo preparation

## 📊 Success Metrics (3-Hour MVP)

### **MVP Goals:**
- ✅ Scrape competitor data using Linkup scraping
- ✅ Structure scraped data with Structify
- ✅ Generate ad copy using OpenAI Prompting
- ✅ Generate images/videos using Imagepik
- ✅ Translate content using DeepL
- ✅ Display preview of generated content
- ✅ Post to Twitter/X successfully
- ✅ Basic working demo in 3 hours

### **Demo Success Criteria:**
- User can input a product/service description
- System scrapes competitor data and structures it
- System generates compelling ad copy using AI
- System generates relevant images/videos
- System can translate content to multiple languages
- User can preview the complete ad
- User can post directly to Twitter/X
- Application runs without critical errors

## ⚠️ Risk Mitigation (3-Hour Sprint)

### **Critical Risks & Quick Fixes:**
- **API Keys:** Have backup API keys ready, use environment variables
- **API Failures:** Implement basic error handling with fallback messages
- **Time Constraints:** Focus on core functionality, skip advanced features
- **Integration Issues:** Use simple, well-documented APIs
- **UI Polish:** Use CSS frameworks (Bootstrap/Tailwind) for quick styling

### **Backup Plans:**
- If Linkup scraping fails → Use predefined competitor data
- If Structify fails → Use basic JSON parsing
- If Imagepik API fails → Use placeholder images
- If DeepL API fails → Skip translation feature
- If Twitter API fails → Show "Copy to clipboard" functionality
- If OpenAI API fails → Use predefined ad templates
- If deployment fails → Run locally for demo

## 🚀 Quick Start (3-Hour Sprint)

### Prerequisites
- Python 3.9+
- API Keys: OpenAI, Linkup, Structify, Imagepik, DeepL, Twitter/X
- Code editor (VS Code recommended)

### Rapid Setup (5 minutes)
```bash
# Clone and setup
git clone <repository-url>
cd pixel-perfect
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn streamlit requests python-dotenv

# Create basic structure
mkdir src
touch src/main.py src/app.py requirements.txt
touch .env
```

### Environment Variables (.env)
```env
OPENAI_API_KEY=your_openai_key
LINKUP_API_KEY=your_linkup_key
STRUCTIFY_API_KEY=your_structify_key
IMAGEPIK_API_KEY=your_imagepik_key
DEEPL_API_KEY=your_deepl_key
TWITTER_API_KEY=your_twitter_key
TWITTER_API_SECRET=your_twitter_secret
```

### Start Development
```bash
# Terminal 1 - Start FastAPI backend
uvicorn src.main:app --reload --port 8000

# Terminal 2 - Start Streamlit frontend
streamlit run src/app.py --server.port 8501
# Open http://localhost:8501
```

## 📁 Project Structure (MVP)
```
pixel-perfect/
├── src/
│   ├── main.py            # FastAPI backend
│   └── app.py             # Streamlit frontend
├── venv/                  # Python virtual environment
├── requirements.txt       # Python dependencies
├── .env                   # API keys
└── README.md             # This file
```

## 🎯 Demo Script (3-Hour Sprint)

### **5-Minute Demo Flow:**
1. **Open application** → Show clean, simple interface
2. **Input product description** → "New eco-friendly water bottle"
3. **Scrape competitor data** → Show Linkup scraping competitor ads
4. **Structure data** → Display Structify-processed competitor insights
5. **Generate ad copy** → Show AI-generated compelling text
6. **Generate media** → Display relevant product image/video
7. **Translate content** → Show DeepL translation to Spanish/French
8. **Preview complete ad** → Show final multilingual ad layout
9. **Post to Twitter** → Demonstrate live posting
10. **Show success** → Confirm post published

### **Key Talking Points:**
- "Built in just 3 hours by 4 developers"
- "AI-powered content generation with competitor analysis"
- "Automated data scraping and structuring"
- "Multilingual content generation"
- "One-click social media posting"
- "Extensible API framework for future platforms"

## 🔮 Post-Sprint Enhancements

- [ ] Add more social platforms (Instagram, LinkedIn)
- [ ] Implement user accounts and campaign management
- [ ] Add A/B testing for ad variations
- [ ] Include analytics and performance tracking
- [ ] Add video ad generation capabilities
- [ ] Implement scheduling and automation

---

**🚀 Built in 3 hours by the Pixel Perfect Sprint Team**
