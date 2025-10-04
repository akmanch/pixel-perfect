from pydantic import BaseModel
from typing import List, Optional

class TeammateOutput(BaseModel):
    """
    What YOUR TEAMMATE gives YOU (OpenAI output)
    """
    product: str
    short_description: str
    target_audience: str
    objective: str
    primary_platforms: List[str]
    budget: str
    brand_voice: str
    key_messages: List[str]
    visual_direction: str
    constraints: str
    success_metrics: List[str]
    
    # Product-specific fields:
    price: Optional[str] = None                    # "From $999" or "$10.99/month"
    is_new_product: bool = True                    # True if launching
    competitors: Optional[List[str]] = None        # ["Samsung Galaxy S24", "Google Pixel 8 Pro"]
    
class ScrapedData(BaseModel):
    """
    What YOU return to YOUR TEAMMATE
    """
    # Core info
    company_info: dict = {}
    product_details: dict = {}
    
    # Competitor intelligence (KEY!)
    competitor_analysis: dict = {}        # Detailed breakdown per competitor
    how_to_beat_them: dict = {}          # Action plan
    pricing_comparison: dict = {}        # Price vs each competitor
    
    # Event-specific
    event_success_metrics: dict = {}
    attendee_testimonials: List[str] = []
    
    # Job-specific  
    company_culture: dict = {}
    work_life_balance: dict = {}
    benefits_info: dict = {}
    
    # Supporting data
    market_gaps: List[str] = []
    recent_news: List[str] = []
    category_insights: dict = {}
    
    # Metadata
    data_quality: str = ""
    sources_scraped: List[str] = []
    scraping_timestamp: str = ""