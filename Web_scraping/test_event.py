#!/usr/bin/env python3
"""Test event scraping"""
from llinkupscraper import LinkupScraper
from schema import TeammateOutput

def test_event():
    """Test scraping for an event"""
    
    scraper = LinkupScraper()
    
    # Event input
    event_input = TeammateOutput(
        product="TechCrunch Disrupt 2024",
        short_description="Premier startup conference and hackathon with $100K prizes",
        target_audience="Startup founders, developers, investors",
        objective="Maximize attendance and participation",
        primary_platforms=["LinkedIn", "Twitter", "Instagram"],
        budget="High",
        brand_voice="Innovative, exciting, opportunity-driven",
        key_messages=[
            "Connect with top VCs and investors",
            "Compete for $100K in prizes",
            "Network with 10,000+ attendees",
            "Launch your startup on stage"
        ],
        visual_direction="Bold, energetic, tech-forward",
        constraints="Highlight past success stories",
        success_metrics=["Ticket sales", "Media coverage", "Social engagement"],
        price=None,
        is_new_product=False,
        competitors=None
    )
    
    print("="*70)
    print("🧪 EVENT TEST - TechCrunch Disrupt 2024")
    print("="*70)
    print(f"Event: {event_input.product}")
    print(f"Target: {event_input.target_audience}")
    print(f"Key Messages:")
    for msg in event_input.key_messages:
        print(f"  - {msg}")
    print("="*70)
    
    try:
        result = scraper.scrape_for_ad(event_input)
        
        print("\n" + "="*70)
        print("📤 SCRAPED DATA FOR EVENT AD:")
        print("="*70)
        
        print(f"\n📊 Data Quality: {result.data_quality}")
        
        # Event Success Metrics
        if result.event_success_metrics:
            print("\n📈 EVENT SUCCESS METRICS:")
            metrics = result.event_success_metrics
            if metrics.get('attendance'):
                print(f"  {metrics['attendance'][:250]}...")
            if metrics.get('sources'):
                print(f"  Sources: {len(metrics['sources'])} found")
        
        # Attendee Testimonials
        if result.attendee_testimonials:
            print(f"\n💬 ATTENDEE TESTIMONIALS ({len(result.attendee_testimonials)} found):")
            for i, testimonial in enumerate(result.attendee_testimonials[:3], 1):
                print(f"  {i}. {testimonial[:150]}...")
        
        print("\n" + "="*70)
        print("✅ EVENT SCRAPING TEST SUCCESSFUL!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_event()
