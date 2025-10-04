class LinkupQueryBuilder:
    """
    Query builder that uses PROVIDED competitor names
    """
    
    def get_queries(
        self, 
        ad_type: str, 
        subject: str, 
        category: str,
        key_messages: list = None,
        our_price: str = None,
        competitors: list = None  # NEW: Competitor names from teammate
    ) -> dict:
        """Get type-specific queries"""
        
        if ad_type == "product":
            return self._product_queries(
                subject, category, key_messages, our_price, competitors
            )
        elif ad_type == "event":
            return self._event_queries(subject, category)
        elif ad_type == "job":
            return self._job_queries(subject, category)
        else:
            return self._generic_queries(subject)
    
    # ════════════════════════════════════════════════════════════
    # PRODUCT QUERIES: Using PROVIDED competitor names
    # ════════════════════════════════════════════════════════════
    
    def _product_queries(
        self, 
        subject: str, 
        category: str, 
        key_messages: list = None,
        our_price: str = None,
        competitors: list = None
    ) -> dict:
        """
        For PRODUCTS: Use provided competitor names for TARGETED scraping
        """
        
        queries = {}
        
        # If competitors provided, search each one specifically
        if competitors and len(competitors) > 0:
            
            # Query for each competitor's weaknesses
            for i, competitor_name in enumerate(competitors[:2], 1):  # Top 2
                queries[f"competitor_{i}_overview"] = f"What are the key features, price, and specifications of {competitor_name}?"
                
                queries[f"competitor_{i}_weaknesses"] = f"What are the main customer complaints and problems with {competitor_name}?"
                
                queries[f"competitor_{i}_vs_us"] = f"How does {competitor_name} compare to a product with {', '.join(key_messages[:2]) if key_messages else 'better features'}?"
        
        else:
            # Fallback: Search generically if no competitors provided
            queries["identify_competitors"] = f"Who are the top 2 competitors in the {category} market and their prices?"
            
            queries["market_pain_points"] = f"What are common customer complaints in the {category} market?"
        
        # Universal queries (always search these)
        
        queries["market_gaps"] = f"What unmet needs and gaps exist in the {category} market for {subject}?"
        
        # Price comparison (if we have our price)
        if our_price:
            if competitors:
                # Specific price comparison
                competitor_list = ", ".join(competitors[:2])
                queries["pricing_comparison"] = f"Compare the price of {subject} at {our_price} with {competitor_list}?"
            else:
                # Generic price comparison
                queries["pricing_landscape"] = f"What are typical prices in the {category} market compared to {our_price}?"
        
        # Validate our key messages
        if key_messages:
            queries["validate_claims"] = f"Do customers care about {', '.join(key_messages[:2])} in {category} products?"
        
        return queries
    
    # ════════════════════════════════════════════════════════════
    # EVENT & JOB QUERIES: Same as before
    # ════════════════════════════════════════════════════════════
    
    def _event_queries(self, subject: str, category: str) -> dict:
        """For EVENTS"""
        return {
            "event_success_history": f"What are the attendance numbers and success metrics for {subject}?",
            "attendee_testimonials": f"What do attendees say about their experience at {subject}?",
            "event_highlights": f"What are the notable achievements and highlights of {subject}?",
            "organizer_credibility": f"Who organizes {subject} and what is their reputation?",
            "networking_value": f"What networking and career opportunities does {subject} provide?"
        }
    
    def _job_queries(self, subject: str, category: str) -> dict:
        """For JOBS"""
        return {
            "company_culture": f"What is the company culture like at {subject}?",
            "work_life_balance": f"What is the work-life balance at {subject}?",
            "compensation_benefits": f"What are the salary and benefits at {subject}?",
            "career_growth": f"What career growth opportunities does {subject} offer?",
            "employee_satisfaction": f"What do employees say about working at {subject}?",
            "company_stability": f"What is the financial stability and outlook of {subject}?"
        }
    
    def _generic_queries(self, subject: str) -> dict:
        """Fallback"""
        return {
            "general_info": f"What are the key features and reviews of {subject}?"
        }
    
    def get_category_queries(self, category: str) -> dict:
        """Fallback when no data"""
        return {
            "category_overview": f"Who are the key players and trends in the {category} market?",
            "customer_needs": f"What features and needs do customers want in {category} products?"
        }