#!/usr/bin/env python3
"""
Test integration between frontend and backend
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Web_scraping.llinkupscraper import LinkupScraper
from Web_scraping.schema import TeammateOutput

def test_integration():
    """Test the integrated scraper"""
    
    print("="*70)
    print("🧪 TESTING BACKEND INTEGRATION")
    print("="*70)
    
    try:
        # Initialize scraper
        print("\n1️⃣ Initializing Linkup Scraper...")
        scraper = LinkupScraper()
        print("✅ Scraper initialized successfully")
        
        # Create test data
        print("\n2️⃣ Creating test product data...")
        product_data = TeammateOutput(
            product="iPhone 15 Pro",
            short_description="Apple's flagship smartphone",
            target_audience="Tech enthusiasts",
            objective="Competitive analysis",
            primary_platforms=["Instagram"],
            budget="High",
            brand_voice="Premium",
            key_messages=["Best camera", "Fastest processor"],
            visual_direction="Sleek",
            constraints="Apple brand",
            success_metrics=["Sales"],
            price="$999",
            is_new_product=True,
            competitors=["Samsung Galaxy S24 Ultra"]
        )
        print("✅ Test data created")
        
        # Run scraper
        print("\n3️⃣ Running scraper...")
        result = scraper.scrape_for_ad(product_data)
        print("✅ Scraping complete!")
        
        # Display results
        print("\n" + "="*70)
        print("📊 RESULTS")
        print("="*70)
        print(f"Data Quality: {result.data_quality}")
        print(f"Competitors Analyzed: {len(result.competitor_analysis)}")
        print(f"Market Gaps Found: {len(result.market_gaps)}")
        print(f"Pricing Data: {'✅ Available' if result.pricing_comparison else '❌ None'}")
        
        print("\n" + "="*70)
        print("✅ INTEGRATION TEST PASSED!")
        print("="*70)
        print("\n📝 Next Steps:")
        print("1. Start backend: ./start_backend.sh")
        print("2. Start frontend: ./start_frontend.sh")
        print("3. Open: http://localhost:8501")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
