import streamlit as st
import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv
import time
from datadog_integration import dd_logger

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
    start_time = time.time()
    try:
        # Increase timeout for media generation (can take 60-120 seconds)
        timeout = 180 if endpoint == "/generate-media" else 30
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=timeout)
        response.raise_for_status()
        
        # Track API call success
        duration_ms = (time.time() - start_time) * 1000
        dd_logger.track_api_usage(
            endpoint=endpoint,
            success=True,
            duration_ms=duration_ms,
            user_id=st.session_state.get('session_id'),
            additional_tags=[f"frontend:streamlit"]
        )
        
        # Increment session API calls counter
        if 'api_calls' in st.session_state:
            st.session_state.api_calls += 1
        
        return response.json()
    except requests.exceptions.RequestException as e:
        # Track API call failure
        duration_ms = (time.time() - start_time) * 1000
        dd_logger.track_api_usage(
            endpoint=endpoint,
            success=False,
            duration_ms=duration_ms,
            user_id=st.session_state.get('session_id'),
            additional_tags=[f"frontend:streamlit", f"error:{type(e).__name__}"]
        )
        
        st.error(f"API Error: {str(e)}")
        return {"success": False, "message": str(e)}

def validate_product_description(text: str) -> tuple[bool, str]:
    """Validate if product description is clear and specific"""
    text = text.strip().lower()
    
    # Check if too short or vague
    if len(text) < 10:
        return False, "Please provide more details about your product or service."
    
    # Check for vague terms that need clarification
    vague_terms = [
        "something", "thing", "stuff", "product", "service", "item", 
        "this", "that", "it", "good", "nice", "great", "amazing"
    ]
    
    vague_count = sum(1 for term in vague_terms if term in text)
    
    if vague_count > 2:
        return False, "Please be more specific about what you're selling. Instead of 'something good', tell me exactly what product or service you offer."
    
    # Check if it's too generic
    generic_phrases = [
        "create an ad", "make an ad", "advertisement", "marketing", 
        "promote", "sell", "business", "company"
    ]
    
    if any(phrase in text for phrase in generic_phrases) and len(text.split()) < 5:
        return False, "I need to know what specific product or service you want to advertise. Please tell me exactly what you're selling."
    
    return True, "Product description is clear!"

def export_to_json_format(ad_data: dict) -> dict:
    """Export ad data in the exact output.json format"""
    return {
        "success": True,
        "ad_data": ad_data,
        "message": "Ad generation completed successfully"
    }

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
        st.header("💬 Chatbot Assistant")
        
        # Initialize session state for chatbot
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_info" not in st.session_state:
            st.session_state.user_info = {}
        if "chat_step" not in st.session_state:
            st.session_state.chat_step = 0
        if "session_start_time" not in st.session_state:
            st.session_state.session_start_time = time.time()
        if "session_id" not in st.session_state:
            st.session_state.session_id = f"user_{int(time.time())}"
        if "ads_generated" not in st.session_state:
            st.session_state.ads_generated = 0
        if "api_calls" not in st.session_state:
            st.session_state.api_calls = 0
        
        # Chatbot steps
        steps = [
            {
                "question": "👋 Hi! I'm your AI assistant. What product or service would you like to create an ad for?\n\nPlease be specific and clear about what you're selling (e.g., 'iPhone 15 Pro', 'Organic Coffee Beans', 'Fitness App Subscription').",
                "key": "product_description",
                "input_type": "text_area",
                "placeholder": "Describe your product or service clearly and specifically...",
                "validation": "product_clear"
            },
            {
                "question": "🎯 Who is your target audience? (e.g., young professionals, eco-conscious consumers, tech enthusiasts)",
                "key": "target_audience",
                "input_type": "text_input",
                "placeholder": "Describe your ideal customer..."
            },
            {
                "question": "💰 What's your price range or value proposition?",
                "key": "price_range",
                "input_type": "text_input",
                "placeholder": "e.g., $20-50, premium quality, affordable luxury..."
            },
            {
                "question": "🏆 Do you have any competitors you'd like me to analyze? (Optional)",
                "key": "competitor_url",
                "input_type": "text_input",
                "placeholder": "https://competitor-website.com",
                "optional": True
            },
            {
                "question": "🎨 What style should the ad have? (modern, classic, playful, professional)",
                "key": "ad_style",
                "input_type": "text_input",
                "placeholder": "Describe the tone and style..."
            }
        ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Current step
        current_step = st.session_state.chat_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            # Display current question
            with st.chat_message("assistant"):
                st.markdown(step["question"])
            
            # Input field based on type
            if step["input_type"] == "text_area":
                user_input = st.text_area(
                    "Your response:",
                    placeholder=step["placeholder"],
                    height=100,
                    key=f"input_{current_step}"
                )
            else:
                user_input = st.text_input(
                    "Your response:",
                    placeholder=step["placeholder"],
                    key=f"input_{current_step}"
                )
            
            # Submit button
            if st.button("Send", key=f"send_{current_step}"):
                if user_input.strip() or step.get("optional", False):
                    # Validate product description if it's the first step
                    if step.get("validation") == "product_clear":
                        is_valid, validation_message = validate_product_description(user_input)
                        if not is_valid:
                            st.error(f"❌ {validation_message}")
                            return
                    
                    # Store user response
                    st.session_state.user_info[step["key"]] = user_input.strip()
                    
                    # Add user message to chat
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input
                    })
                    
                    # Move to next step
                    st.session_state.chat_step += 1
                    st.rerun()
                else:
                    st.error("Please provide a response.")
        
        # Summary and generate button
        elif current_step >= len(steps):
            with st.chat_message("assistant"):
                st.markdown("✅ Perfect! I have all the information I need. Here's what I'll create for you:")
                
                summary = f"""
                **Product:** {st.session_state.user_info.get('product_description', 'N/A')}
                **Target Audience:** {st.session_state.user_info.get('target_audience', 'N/A')}
                **Price Range:** {st.session_state.user_info.get('price_range', 'N/A')}
                **Competitor:** {st.session_state.user_info.get('competitor_url', 'None')}
                **Style:** {st.session_state.user_info.get('ad_style', 'N/A')}
                """
                st.markdown(summary)
            
            # Action buttons
            col_gen, col_reset = st.columns([2, 1])
            
            with col_gen:
                if st.button("🚀 Generate Complete Ad", type="primary", use_container_width=True):
                    # Get data from chatbot
                    product_description = st.session_state.user_info.get('product_description', '')
                    competitor_url = st.session_state.user_info.get('competitor_url', '')
                    custom_target_audience = st.session_state.user_info.get('target_audience', '')
                    price_range = st.session_state.user_info.get('price_range', '')
                    ad_style = st.session_state.user_info.get('ad_style', '')
                    
                    if not product_description:
                        st.error("Please complete the chatbot conversation first")
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
                    
                    # Enhanced copy generation with chatbot data
                    copy_data = make_api_request("/generate-copy", {
                        "product_description": product_description,
                        "competitor_insights": competitor_insights,
                        "target_audience": custom_target_audience or target_audience.lower(),
                        "price_range": price_range,
                        "ad_style": ad_style
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
                        "style": ad_style or "modern"
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
                    
                    # Track successful ad generation
                    st.session_state.ads_generated += 1
                    
                    # Log successful ad generation to Datadog
                    dd_logger.log_event(
                        title="Ad Generation Completed",
                        text=f"Successfully generated ad for {product_description[:50]}...",
                        tags=[
                            f"product:{product_description[:30]}",
                            f"target_audience:{custom_target_audience or target_audience}",
                            f"ad_style:{ad_style or 'default'}",
                            f"session_id:{st.session_state.session_id}"
                        ]
                    )
                    
                    # Store results in session state (matching output.json format)
                    st.session_state.ad_data = {
                        "product_description": product_description,
                        "target_audience": custom_target_audience or target_audience.lower(),
                        "price_range": price_range,
                        "ad_style": ad_style,
                        "competitor_insights": competitor_insights,
                        "generated_content": {
                            "ad_copy": ad_copy,
                            "translated_copy": translated_copy,
                            "media_url": media_url,
                            "tweet_url": "https://twitter.com/user/status/1234567890"  # Placeholder
                        },
                        "metadata": {
                            "generation_timestamp": "2024-01-15T12:30:00Z",
                            "api_version": "1.0.0",
                            "processing_time_ms": 2500,
                            "languages": ["en", translation_language],
                            "platforms": ["twitter"]
                        }
                    }
                    
                    # Legacy format for backward compatibility
                    st.session_state.ad_copy = ad_copy
                    st.session_state.translated_copy = translated_copy
                    st.session_state.media_url = media_url
                    st.session_state.competitor_insights = competitor_insights
            
            with col_reset:
                if st.button("🔄 New Conversation", use_container_width=True):
                    # Reset chatbot state
                    st.session_state.messages = []
                    st.session_state.user_info = {}
                    st.session_state.chat_step = 0
                    st.rerun()
    
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
            col_a, col_b, col_c, col_d = st.columns(4)
            
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
                if st.button("💾 Download JSON", use_container_width=True):
                    if hasattr(st.session_state, 'ad_data'):
                        json_data = export_to_json_format(st.session_state.ad_data)
                        json_str = json.dumps(json_data, indent=2)
                        st.download_button(
                            label="📥 Download output.json",
                            data=json_str,
                            file_name="ad_output.json",
                            mime="application/json"
                        )
                    else:
                        st.error("No data to download")
            
            with col_d:
                if st.button("🔄 New Ad", use_container_width=True):
                    # Reset chatbot state
                    st.session_state.messages = []
                    st.session_state.user_info = {}
                    st.session_state.chat_step = 0
                    st.rerun()
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
