import streamlit as st
import requests
import json
import time

# Configure page
st.set_page_config(
    page_title="Linkup Ad Generator",
    page_icon="🚀",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Title
st.title("🚀 AI-Powered Ad Generator with Linkup")
st.markdown("### Generate data-driven ads with real-time competitor analysis")

# Check API Status
def check_api_status():
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

# Sidebar - API Status
with st.sidebar:
    st.header("⚙️ Configuration")
    api_status = check_api_status()
    if api_status:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Not Running")
        st.info("Start backend: `uvicorn src.main:app --reload --port 8000`")

# Main Form
st.header("📝 Ad Campaign Details")

with st.form("ad_generator_form"):
    
    # Product Information
    st.subheader("🎯 Product Information")
    col1, col2 = st.columns(2)
    
    with col1:
        product = st.text_input(
            "Product Name *",
            placeholder="e.g., iPhone 15 Pro, Tesla Model 3",
            help="Enter the name of your product or service"
        )
        
        short_description = st.text_area(
            "Short Description *",
            placeholder="e.g., Apple's flagship smartphone with A17 Pro chip and titanium design",
            help="Brief description of your product",
            height=100
        )
        
        price = st.text_input(
            "Price",
            placeholder="e.g., From $999, $29.99/month",
            help="Product pricing (optional)"
        )
    
    with col2:
        target_audience = st.text_input(
            "Target Audience *",
            placeholder="e.g., Tech professionals 25-45",
            help="Who is this ad for?"
        )
        
        objective = st.text_input(
            "Campaign Objective *",
            placeholder="e.g., Increase sales, Beat competition",
            help="What do you want to achieve?"
        )
        
        budget = st.selectbox(
            "Budget Level *",
            ["Low", "Medium", "High"],
            help="Campaign budget level"
        )
    
    # Competitors
    st.subheader("🏆 Competitor Analysis")
    st.markdown("*Add up to 2 competitors for analysis*")
    
    col1, col2 = st.columns(2)
    with col1:
        competitor1 = st.text_input(
            "Competitor 1",
            placeholder="e.g., Samsung Galaxy S24 Ultra",
            help="First competitor (optional)"
        )
    with col2:
        competitor2 = st.text_input(
            "Competitor 2",
            placeholder="e.g., Google Pixel 8 Pro",
            help="Second competitor (optional)"
        )
    
    # Messaging
    st.subheader("💬 Messaging & Branding")
    
    col1, col2 = st.columns(2)
    with col1:
        brand_voice = st.selectbox(
            "Brand Voice *",
            ["Professional", "Casual", "Premium", "Playful", "Innovative", "Trustworthy"],
            help="Tone of your ad"
        )
        
        visual_direction = st.selectbox(
            "Visual Style *",
            ["Modern", "Classic", "Sleek", "Bold", "Minimalist", "Colorful"],
            help="Visual aesthetic"
        )
    
    with col2:
        platforms = st.multiselect(
            "Platforms *",
            ["Instagram", "Facebook", "Twitter", "LinkedIn", "YouTube", "TikTok"],
            default=["Instagram", "Facebook"],
            help="Where will this ad run?"
        )
        
        is_new_product = st.checkbox(
            "Is this a new product launch?",
            value=True,
            help="Check if launching a new product"
        )
    
    # Key Messages
    st.subheader("✨ Key Messages")
    st.markdown("*Add 2-3 key points you want to highlight*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        message1 = st.text_input("Message 1", placeholder="e.g., Best camera system")
    with col2:
        message2 = st.text_input("Message 2", placeholder="e.g., Fastest processor")
    with col3:
        message3 = st.text_input("Message 3", placeholder="e.g., All-day battery")
    
    # Additional Details
    st.subheader("📊 Additional Details")
    
    col1, col2 = st.columns(2)
    with col1:
        constraints = st.text_area(
            "Constraints",
            placeholder="e.g., Must follow brand guidelines",
            help="Any restrictions or requirements",
            height=80
        )
    with col2:
        success_metrics = st.text_input(
            "Success Metrics",
            placeholder="e.g., Conversions, Engagement, Sales",
            help="How will you measure success?"
        )
    
    # Submit Button
    st.markdown("---")
    submitted = st.form_submit_button(
        "🚀 Generate Ad with Linkup Analysis",
        use_container_width=True,
        type="primary"
    )

# Process Form Submission
if submitted:
    if not product or not short_description or not target_audience or not objective:
        st.error("❌ Please fill in all required fields marked with *")
    elif not api_status:
        st.error("❌ Backend API is not running. Please start the server first.")
    else:
        # Prepare competitors list
        competitors = []
        if competitor1:
            competitors.append(competitor1)
        if competitor2:
            competitors.append(competitor2)
        
        # Prepare key messages list
        key_messages = []
        for msg in [message1, message2, message3]:
            if msg:
                key_messages.append(msg)
        
        # Build request payload
        payload = {
            "competitor_url": competitors[0] if competitors else "",
            "product_description": f"{product} - {short_description}"
        }
        
        # Store full data for later use
        full_data = {
            "product": product,
            "short_description": short_description,
            "target_audience": target_audience,
            "objective": objective,
            "primary_platforms": platforms,
            "budget": budget,
            "brand_voice": brand_voice,
            "key_messages": key_messages,
            "visual_direction": visual_direction,
            "constraints": constraints or "None",
            "success_metrics": success_metrics.split(",") if success_metrics else ["Engagement"],
            "price": price,
            "is_new_product": is_new_product,
            "competitors": competitors if competitors else None
        }
        
        # Show loading
        with st.spinner("🔍 Analyzing competitors with Linkup... This may take 15-30 seconds..."):
            try:
                # Call scrape-data endpoint
                response = requests.post(
                    f"{API_BASE_URL}/scrape-data",
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Display Results
                    st.header("📊 Linkup Analysis Results")
                    
                    # Generate Image Automatically in parallel
                    image_url = None
                    with st.spinner("🎨 Generating ad image with Freepik AI..."):
                        try:
                            image_response = requests.post(
                                f"{API_BASE_URL}/generate-media",
                                json={
                                    "product_description": f"{product} - {short_description}",
                                    "media_type": "image",
                                    "style": visual_direction.lower()
                                },
                                timeout=120
                            )
                            
                            if image_response.status_code == 200:
                                image_data = image_response.json()
                                if image_data.get("success"):
                                    image_url = image_data.get("media_url")
                                    st.success("✅ Image Generated!")
                        except Exception as e:
                            st.warning(f"⚠️ Image generation failed: {str(e)}")
                    
                    # Show image first if generated
                    if image_url:
                        st.subheader("🎨 Generated Ad Image")
                        st.image(image_url, caption=f"{product} - AI Generated Ad", use_column_width=True)
                        st.markdown(f"[🔗 View Full Resolution]({image_url})")
                        st.markdown("---")
                    
                    # Show input summary
                    with st.expander("📝 Campaign Summary", expanded=True):
                        st.markdown(f"""
                        **Product:** {product}  
                        **Target:** {target_audience}  
                        **Competitors:** {', '.join(competitors) if competitors else 'None'}  
                        **Budget:** {budget}  
                        **Platforms:** {', '.join(platforms)}  
                        **Key Messages:** {', '.join(key_messages) if key_messages else 'None'}
                        """)
                    
                    # Show scraped data
                    if data.get("success"):
                        scraped_data = data.get("data", {})
                        
                        # Data Quality
                        st.metric(
                            "Data Quality",
                            scraped_data.get("data_quality", "N/A"),
                            help="Quality of scraped data"
                        )
                        
                        # Competitor Analysis
                        st.subheader("🏆 Competitor Analysis")
                        competitor_analysis = scraped_data.get("competitor_analysis", {})
                        
                        if competitor_analysis:
                            for comp_key, comp_data in competitor_analysis.items():
                                with st.expander(f"📊 {comp_data.get('name', 'Competitor')}"):
                                    overview = comp_data.get('overview', {})
                                    st.markdown(f"**Description:** {overview.get('description', 'N/A')[:300]}...")
                                    
                                    st.markdown("**Weaknesses:**")
                                    for weakness in comp_data.get('weaknesses', [])[:3]:
                                        st.markdown(f"- {weakness[:150]}...")
                                    
                                    st.markdown("**How We Beat Them:**")
                                    for strategy in comp_data.get('how_we_beat_them', [])[:3]:
                                        st.markdown(f"- {strategy[:150]}...")
                        else:
                            st.info("No competitor data available")
                        
                        # Market Gaps
                        st.subheader("💡 Market Gaps to Exploit")
                        market_gaps = scraped_data.get("market_gaps", [])
                        if market_gaps:
                            for i, gap in enumerate(market_gaps[:5], 1):
                                st.markdown(f"{i}. {gap[:200]}...")
                        else:
                            st.info("No market gaps identified")
                        
                        # Pricing Comparison
                        st.subheader("💰 Pricing Analysis")
                        pricing = scraped_data.get("pricing_comparison", {})
                        if pricing:
                            st.markdown(f"**Your Price:** {pricing.get('our_price', 'N/A')}")
                            st.markdown(f"**Market Analysis:** {pricing.get('market_analysis', 'N/A')[:300]}...")
                        else:
                            st.info("No pricing data available")
                        
                        # Strategy
                        st.subheader("🎯 Winning Strategy")
                        strategy = scraped_data.get("how_to_beat_them", {})
                        if strategy:
                            st.json(strategy)
                        
                        # Download Results
                        st.download_button(
                            label="📥 Download Full Report",
                            data=json.dumps(scraped_data, indent=2),
                            file_name=f"linkup_analysis_{product.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.json(response.json())
                    
            except requests.Timeout:
                st.error("❌ Request timed out. The analysis is taking longer than expected.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Provide competitor names for deeper analysis")

