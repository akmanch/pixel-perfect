# Social Media Ad Generator - Quick Start Guide

## 🚀 One-Command Setup

```bash
./setup.sh
```

## 📋 Manual Setup (if needed)

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp env.example .env
# Edit .env with your API keys
```

### 4. Start Services

**Terminal 1 - Backend:**
```bash
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run src/app.py --server.port 8501
```

### 5. Access Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔑 Required API Keys

Edit `.env` file with your actual keys:

```env
OPENAI_API_KEY=sk-your-openai-key
LINKUP_API_KEY=your-linkup-key
STRUCTIFY_API_KEY=your-structify-key
IMAGEPIK_API_KEY=your-imagepik-key
DEEPL_API_KEY=your-deepl-key
TWITTER_API_KEY=your-twitter-key
TWITTER_API_SECRET=your-twitter-secret
```

## 🧪 Testing the Setup

1. Start both services
2. Open http://localhost:8501
3. Enter a product description
4. Click "Generate Complete Ad"
5. Check the preview

## 🐛 Troubleshooting

- **API Connection Failed**: Make sure FastAPI backend is running on port 8000
- **Import Errors**: Make sure virtual environment is activated
- **Permission Denied**: Run `chmod +x setup.sh` first

## 📁 Project Structure

```
pixel-perfect/
├── src/
│   ├── main.py          # FastAPI backend
│   └── app.py           # Streamlit frontend
├── venv/                # Python virtual environment
├── requirements.txt     # Dependencies
├── env.example         # Environment template
├── setup.sh            # Setup script
└── README.md           # Project documentation
```
