#!/usr/bin/env python3
"""Quick test with limited queries"""
from llinkupscraper import LinkupScraper
from schema import TeammateOutput
import json

def test_quick():
    """Test with one competitor only"""
    
    scraper = LinkupScraper()
    
    # Simplified input
    product_input = TeammateOutput(
        product="iPhone 15 Pro",
        short_description="Apple's flagship smartphone",
        target_audience="Tech professionals",
        objective="Beat Samsung",
        primary_platforms=["Instagram"],
        budget="High",
        brand_voice="Premium",
        key_messages=["Best camera system"],
        visual_direction="Sleek",
        constraints="Apple aesthetic",
        success_metrics=["Market share"],
        price="From $999",
        is_new_product=True,
        competitors=["Samsung Galaxy S24 Ultra"]  # Just 1 competitor
    )
    
    print("🧪 QUICK TEST - iPhone 15 Pro vs Samsung Galaxy S24 Ultra")
    print("="*70)
    
    try:
        result = scraper.scrape_for_ad(product_input)
        
        print("\n✅ SCRAPING COMPLETED!")
        print("="*70)
        
        print(f"\n📊 Data Quality: {result.data_quality}")
        
        print("\n🎯 COMPETITOR ANALYSIS:")
        for comp_key, comp_data in result.competitor_analysis.items():
            print(f"\n  {comp_data.get('name', 'Unknown')}:")
            print(f"    Overview: {comp_data.get('overview', {}).get('description', 'N/A')[:200]}...")
            print(f"    Weaknesses Found: {len(comp_data.get('weaknesses', []))}")
            if comp_data.get('weaknesses'):
                print(f"      - {comp_data['weaknesses'][0][:100]}...")
        
        print(f"\n💡 Market Gaps Found: {len(result.market_gaps)}")
        if result.market_gaps:
            print(f"  - {result.market_gaps[0][:100]}...")
        
        print(f"\n💰 Pricing Info:")
        print(f"  Our Price: {result.pricing_comparison.get('our_price', 'N/A')}")
        if result.pricing_comparison.get('market_analysis'):
            print(f"  Analysis: {result.pricing_comparison['market_analysis'][:150]}...")
        
        print("\n" + "="*70)
        print("✅ TEST SUCCESSFUL!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quick()
