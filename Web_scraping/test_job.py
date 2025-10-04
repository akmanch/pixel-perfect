#!/usr/bin/env python3
"""Test job opening scraping"""
from llinkupscraper import LinkupScraper
from schema import TeammateOutput

def test_job_opening():
    """Test scraping for a job opening"""
    
    scraper = LinkupScraper()
    
    # Job opening input
    job_input = TeammateOutput(
        product="Software Engineer at Google",
        short_description="Join Google as a Software Engineer - Full-time position in Mountain View",
        target_audience="Experienced developers",
        objective="Attract top talent to Google",
        primary_platforms=["LinkedIn", "Indeed"],
        budget="High",
        brand_voice="Innovative, collaborative",
        key_messages=[
            "Work on cutting-edge technology",
            "Competitive compensation and benefits",
            "Great work-life balance"
        ],
        visual_direction="Professional, modern",
        constraints="Must highlight Google culture",
        success_metrics=["Application rate", "Quality of applicants"],
        price=None,  # Not applicable for jobs
        is_new_product=False,
        competitors=None  # Not applicable for jobs
    )
    
    print("="*70)
    print("🧪 JOB OPENING TEST - Software Engineer at Google")
    print("="*70)
    print(f"Position: {job_input.product}")
    print(f"Target: {job_input.target_audience}")
    print(f"Key Messages: {job_input.key_messages}")
    print("="*70)
    
    try:
        result = scraper.scrape_for_ad(job_input)
        
        print("\n" + "="*70)
        print("📤 SCRAPED DATA FOR JOB AD:")
        print("="*70)
        
        print(f"\n📊 Data Quality: {result.data_quality}")
        
        # Company Culture
        if result.company_culture:
            print("\n🏢 COMPANY CULTURE:")
            culture = result.company_culture
            if culture.get('highlights'):
                print(f"  Highlights: {culture['highlights'][:200]}...")
            if culture.get('reviews'):
                print(f"  Reviews: {len(culture['reviews'])} found")
                if culture['reviews']:
                    print(f"    - {culture['reviews'][0][:100]}...")
        
        # Work-Life Balance
        if result.work_life_balance:
            print("\n⚖️  WORK-LIFE BALANCE:")
            balance = result.work_life_balance
            if balance.get('rating'):
                print(f"  Rating: {balance['rating'][:150]}...")
            if balance.get('feedback'):
                print(f"  Feedback: {len(balance['feedback'])} reviews found")
        
        # Benefits
        if result.benefits_info:
            print("\n💰 BENEFITS & COMPENSATION:")
            benefits = result.benefits_info
            if benefits.get('salary'):
                print(f"  Salary Info: {benefits['salary'][:150]}...")
            if benefits.get('perks'):
                print(f"  Perks: {len(benefits['perks'])} found")
                if benefits['perks']:
                    print(f"    - {benefits['perks'][0][:100]}...")
        
        print("\n" + "="*70)
        print("✅ JOB SCRAPING TEST SUCCESSFUL!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_opening()
