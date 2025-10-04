import streamlit as st
import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Social Media Ad Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .preview-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
    """Make API request to FastAPI backend"""
    try:
        # Increase timeout for media generation (can take 60-120 seconds)
        timeout = 180 if endpoint == "/generate-media" else 30
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"success": False, "message": str(e)}

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Social Media Ad Generator</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status Check
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Connection Failed")
        except:
            st.error("❌ API Not Running")
            st.info("Please start the FastAPI server: `uvicorn src.main:app --reload --port 8000`")
        
        st.markdown("---")
        
        # Target Audience Selection
        target_audience = st.selectbox(
            "🎯 Target Audience",
            ["General", "Environmentally Conscious", "Tech Enthusiasts", "Fashion Forward", "Health Focused"]
        )
        
        # Media Type Selection
        media_type = st.selectbox(
            "📸 Media Type",
            ["image", "video"]
        )
        
        # Translation Language
        translation_language = st.selectbox(
            "🌍 Translation Language",
            ["es", "fr", "de", "it", "pt"]
        )

    # Main Content Area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Product Description Input
        product_description = st.text_area(
            "Product/Service Description",
            placeholder="Describe your product or service...",
            height=100,
            help="Enter a detailed description of what you're advertising"
        )
        
        # Competitor URL Input
        competitor_url = st.text_input(
            "Competitor URL (Optional)",
            placeholder="https://competitor-website.com",
            help="Enter a competitor's website URL for analysis"
        )
        
        # Generate Button
        if st.button("🚀 Generate Complete Ad", type="primary", use_container_width=True):
            if not product_description:
                st.error("Please enter a product description")
                return
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Scrape competitor data
            if competitor_url:
                status_text.text("🔍 Scraping competitor data...")
                progress_bar.progress(20)
                
                scrape_data = make_api_request("/scrape-data", {
                    "competitor_url": competitor_url,
                    "product_description": product_description
                })
                
                if scrape_data.get("success"):
                    st.success("✅ Competitor data scraped")
                    
                    # Step 2: Structure data
                    status_text.text("📊 Structuring data...")
                    progress_bar.progress(40)
                    
                    structure_data = make_api_request("/structure-data", {
                        "competitor_url": competitor_url,
                        "product_description": product_description
                    })
                    
                    if structure_data.get("success"):
                        st.success("✅ Data structured")
                        competitor_insights = structure_data.get("data", {})
                    else:
                        competitor_insights = {}
                else:
                    competitor_insights = {}
            else:
                competitor_insights = {}
            
            # Step 3: Generate ad copy
            status_text.text("✍️ Generating ad copy...")
            progress_bar.progress(60)
            
            copy_data = make_api_request("/generate-copy", {
                "product_description": product_description,
                "competitor_insights": competitor_insights,
                "target_audience": target_audience.lower()
            })
            
            if copy_data.get("success"):
                st.success("✅ Ad copy generated")
                ad_copy = copy_data.get("ad_copy", "")
            else:
                ad_copy = "Failed to generate ad copy"
            
            # Step 4: Generate media
            status_text.text("🎨 Generating media...")
            progress_bar.progress(80)
            
            media_data = make_api_request("/generate-media", {
                "product_description": product_description,
                "media_type": media_type,
                "style": "modern"
            })
            
            if media_data.get("success"):
                st.success("✅ Media generated")
                media_url = media_data.get("media_url", "")
            else:
                media_url = ""
            
            # Step 5: Translate content
            status_text.text("🌍 Translating content...")
            progress_bar.progress(90)
            
            translate_data = make_api_request("/translate", {
                "text": ad_copy,
                "target_language": translation_language
            })
            
            if translate_data.get("success"):
                st.success("✅ Content translated")
                translated_copy = translate_data.get("translated_text", "")
            else:
                translated_copy = ad_copy
            
            # Complete
            status_text.text("✅ Complete!")
            progress_bar.progress(100)
            
            # Store results in session state
            st.session_state.ad_copy = ad_copy
            st.session_state.translated_copy = translated_copy
            st.session_state.media_url = media_url
            st.session_state.media_type = media_type
            st.session_state.competitor_insights = competitor_insights
    
    with col2:
        st.header("👀 Preview")
        
        if hasattr(st.session_state, 'ad_copy'):
            # Original Ad Copy
            st.subheader("📝 Original Ad Copy")
            st.markdown(f'<div class="preview-box">{st.session_state.ad_copy}</div>', unsafe_allow_html=True)
            
            # Translated Ad Copy
            if hasattr(st.session_state, 'translated_copy'):
                st.subheader(f"🌍 Translated ({translation_language.upper()})")
                st.markdown(f'<div class="preview-box">{st.session_state.translated_copy}</div>', unsafe_allow_html=True)
            
            # Media Preview
            if hasattr(st.session_state, 'media_url') and st.session_state.media_url:
                st.subheader("🎨 Generated Media")
                # Check if it's a video or image based on URL or media type
                if hasattr(st.session_state, 'media_type') and st.session_state.media_type == 'video':
                    st.video(st.session_state.media_url)
                else:
                    st.image(st.session_state.media_url, caption="Generated Media", use_column_width=True)
            
            # Competitor Insights
            if hasattr(st.session_state, 'competitor_insights') and st.session_state.competitor_insights:
                st.subheader("📊 Competitor Insights")
                insights = st.session_state.competitor_insights
                if isinstance(insights, dict):
                    for key, value in insights.items():
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            
            # Action Buttons
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 Copy Text", use_container_width=True):
                    st.write("Text copied to clipboard!")
            
            with col_b:
                if st.button("📱 Post to Twitter", use_container_width=True):
                    # Post to Twitter
                    twitter_data = make_api_request("/post-twitter", {
                        "text": st.session_state.ad_copy,
                        "media_url": st.session_state.media_url
                    })
                    
                    if twitter_data.get("success"):
                        st.success("✅ Posted to Twitter!")
                        st.write(f"Tweet URL: {twitter_data.get('tweet_url', 'N/A')}")
                    else:
                        st.error("❌ Failed to post to Twitter")
            
            with col_c:
                if st.button("💾 Download", use_container_width=True):
                    st.write("Download functionality coming soon!")
        else:
            st.info("👆 Generate an ad to see the preview here")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            🚀 Built in 3 hours by the Pixel Perfect Sprint Team | 
            Powered by OpenAI, Linkup, Structify, Imagepik, DeepL & Twitter APIs
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
