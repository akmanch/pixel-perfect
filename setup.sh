#!/bin/bash

# Social Media Ad Generator - Setup Script
# This script sets up the development environment for the 3-hour sprint

echo "🚀 Setting up Social Media Ad Generator..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual API keys!"
else
    echo "✅ .env file already exists"
fi

# Create startup scripts
echo "📄 Creating startup scripts..."

# Backend startup script
cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting FastAPI backend..."
source venv/bin/activate
uvicorn src.main:app --reload --port 8000 --host 0.0.0.0
EOF

# Frontend startup script
cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "🎨 Starting Streamlit frontend..."
source venv/bin/activate
streamlit run src/app.py --server.port 8501
EOF

# Make scripts executable
chmod +x start_backend.sh start_frontend.sh

echo ""
echo "🎉 Setup complete!"
echo "=================="
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start the backend: ./start_backend.sh"
echo "3. Start the frontend: ./start_frontend.sh"
echo "4. Open http://localhost:8501 in your browser"
echo ""
echo "🔑 Required API Keys:"
echo "   - OpenAI API Key"
echo "   - Linkup API Key"
echo "   - Structify API Key"
echo "   - Imagepik API Key"
echo "   - DeepL API Key"
echo "   - Twitter API Keys"
echo ""
echo "⚡ Quick start:"
echo "   Backend:  uvicorn src.main:app --reload --port 8000"
echo "   Frontend: streamlit run src/app.py --server.port 8501"
echo ""
echo "🚀 Ready for your 3-hour sprint!"
