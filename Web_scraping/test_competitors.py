from llinkupscraper import LinkupScraper
from schema import TeammateOutput

def test_with_competitors_list():
    """Test with PROVIDED competitor names"""
    
    scraper = LinkupScraper()
    
    # Input with COMPETITORS LIST
    product_input = TeammateOutput(
        product="iPhone 15 Pro",
        short_description="Apple's flagship with A17 Pro and titanium design",
        target_audience="Tech professionals 25-45",
        objective="Beat Samsung and Google",
        primary_platforms=["Instagram", "YouTube"],
        budget="High",
        brand_voice="Premium, innovative",
        key_messages=[
            "Faster than any Android",
            "Best camera system",
            "Titanium is stronger and lighter"
        ],
        visual_direction="Sleek, futuristic",
        constraints="Maintain Apple aesthetic",
        success_metrics=["Market share"],
        
        # KEY INPUTS:
        price="From $999",
        is_new_product=True,
        competitors=[                    # PROVIDED BY TEAMMATE!
            "Samsung Galaxy S24 Ultra",
            "Google Pixel 8 Pro"
        ]
    )
    
    print("="*70)
    print("📥 INPUT FROM TEAMMATE:")
    print("="*70)
    print(f"Product: {product_input.product}")
    print(f"Price: {product_input.price}")
    print(f"Competitors: {product_input.competitors}")
    print(f"Key Messages: {product_input.key_messages}")
    
    result = scraper.scrape_for_ad(product_input)
    
    print("\n" + "="*70)
    print("📤 WHAT YOU RETURN TO TEAMMATE:")
    print("="*70)
    
    print("\n🎯 COMPETITOR BREAKDOWN:")
    for comp_key, comp_data in result.competitor_analysis.items():
        print(f"\n{comp_key.upper()}:")
        print(f"  Name: {comp_data.get('name', 'N/A')}")
        print(f"  Weaknesses: {comp_data.get('weaknesses', [])[:2]}")
        print(f"  How We Beat Them: {comp_data.get('how_we_beat_them', [])[:2]}")
    
    print("\n💡 HOW TO BEAT THEM:")
    print(result.how_to_beat_them)
    
    print("\n🎯 MARKET GAPS TO EXPLOIT:")
    print(result.market_gaps[:3])
    
    print("\n💰 PRICE COMPARISON:")
    print(result.pricing_comparison)

if __name__ == "__main__":
    test_with_competitors_list()
