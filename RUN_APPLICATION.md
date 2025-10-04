# 🚀 How to Run the Complete Application

## Project Structure
```
pixel-perfect/
├── src/
│   ├── main.py              # FastAPI Backend (Port 8000)
│   ├── app.py               # Streamlit Frontend (Port 8501)
│   └── datadog_integration.py
├── Web_scraping/
│   ├── llinkupscraper.py    # Linkup Web Scraper
│   ├── schema.py            # Data schemas
│   ├── query_builder.py     # Query optimization
│   └── test_*.py            # Test files
├── start_backend.sh         # Backend startup script
├── start_frontend.sh        # Frontend startup script
└── requirements.txt         # All dependencies
```

---

## 🎯 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# OR use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment
Make sure you have your API keys in `.env` file:
```env
LINKUP_API_KEY=your_linkup_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Run the Application

**Option A: Use Scripts (Recommended)**
```bash
# Terminal 1 - Start Backend
./start_backend.sh

# Terminal 2 - Start Frontend  
./start_frontend.sh
```

**Option B: Manual Start**
```bash
# Terminal 1 - Backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Terminal 2 - Frontend
source venv/bin/activate
streamlit run src/app.py --server.port 8501
```

---

## 🌐 Access the Application

Once both services are running:

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

---

## 🧪 Test Before Running

Test the Linkup integration:
```bash
python3 test_integration.py
```

Test individual components:
```bash
# Test product scraping
python3 Web_scraping/test_quick.py

# Test job scraping
python3 Web_scraping/test_job.py

# Test event scraping
python3 Web_scraping/test_event.py
```

---

## 🔧 How It Works

### Architecture Flow:
```
User (Browser)
    ↓
Streamlit Frontend (Port 8501)
    ↓ HTTP Request
FastAPI Backend (Port 8000)
    ↓ Calls
Linkup Scraper (Web_scraping/)
    ↓ API Call
Linkup API (External)
    ↓ Returns Data
Backend → Frontend → User
```

### Key Endpoints:

1. **`POST /scrape-data`** - Scrape competitor data
   - Input: Product description, competitor URL
   - Output: Market gaps, competitor analysis, pricing

2. **`POST /generate-copy`** - Generate ad copy
   - Input: Product details, scraped insights
   - Output: AI-generated ad copy

3. **`GET /health`** - Health check
   - Returns: Service status

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is available
lsof -ti:8000 | xargs kill -9

# Restart backend
./start_backend.sh
```

### Frontend won't start
```bash
# Check if port 8501 is available
lsof -ti:8501 | xargs kill -9

# Restart frontend
./start_frontend.sh
```

### Import errors
```bash
# Make sure you're in the right directory
cd /Users/saikaushikbhima/Documents/pixel-perfect

# Reinstall dependencies
pip install -r requirements.txt
```

### Linkup API errors
```bash
# Check your .env file has LINKUP_API_KEY
cat .env | grep LINKUP_API_KEY

# Test Linkup directly
python3 Web_scraping/test_quick.py
```

---

## 📊 What Each Component Does

### 1. **Backend (src/main.py)**
- FastAPI server
- Handles API requests
- Integrates Linkup scraper
- Manages data flow

### 2. **Frontend (src/app.py)**
- Streamlit UI
- User interface
- Displays results
- Sends requests to backend

### 3. **Linkup Scraper (Web_scraping/)**
- Scrapes competitor data
- Analyzes market gaps
- Finds pricing information
- Optimized queries for speed

---

## 🎯 Usage Example

1. **Start both services** (backend + frontend)
2. **Open** http://localhost:8501
3. **Enter product details**:
   - Product: "iPhone 15 Pro"
   - Competitor: "Samsung Galaxy S24 Ultra"
4. **Click "Analyze"**
5. **View results**:
   - Competitor weaknesses
   - Market gaps
   - Pricing comparison
   - Suggested strategies

---

## 📝 Development Mode

### Watch logs:
```bash
# Backend logs
tail -f backend.log

# Frontend logs  
tail -f frontend.log
```

### Auto-reload:
- Backend: `--reload` flag enables auto-reload on code changes
- Frontend: Streamlit auto-reloads on file save

---

## 🚀 Ready to Launch!

Your application is integrated and ready to run. The backend now uses your optimized Linkup scraper with fast, focused queries.

**Start the application:**
```bash
./start_backend.sh   # Terminal 1
./start_frontend.sh  # Terminal 2
```

Then open http://localhost:8501 and start generating ads! 🎉

