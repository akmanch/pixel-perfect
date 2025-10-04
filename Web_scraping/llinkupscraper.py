from linkup import LinkupClient
from .schema import TeammateOutput, ScrapedData
from .query_builder import LinkupQueryBuilder
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class LinkupScraper:
    
    def __init__(self, linkup_api_key: str = None):
        self.linkup_api_key = linkup_api_key or os.getenv("LINKUP_API_KEY")
        if not self.linkup_api_key:
            raise ValueError("Linkup API key required!")
        
        self.linkup_client = LinkupClient(api_key=self.linkup_api_key)
        self.query_builder = LinkupQueryBuilder()
        print("✅ Linkup Scraper initialized")
    
    def scrape_for_ad(self, teammate_output: TeammateOutput) -> ScrapedData:
        """Main scraping method"""
        
        print("\n" + "="*60)
        print("🌐 STARTING COMPETITOR-FOCUSED SCRAPING")
        print("="*60)
        print(f"Product: {teammate_output.product}")
        print(f"Price: {teammate_output.price or 'Not specified'}")
        print(f"Competitors: {teammate_output.competitors or 'Will search generically'}")
        print("="*60 + "\n")
        
        # Extract info
        subject = teammate_output.product
        category = self._infer_category(teammate_output.short_description)
        ad_type = self._infer_ad_type(teammate_output)
        
        print(f"🎯 Ad Type: {ad_type.upper()}")
        print(f"📊 Category: {category}")
        
        # Show targeting
        if ad_type == "product" and teammate_output.competitors:
            print(f"🎯 Targeting Competitors:")
            for i, comp in enumerate(teammate_output.competitors[:2], 1):
                print(f"   {i}. {comp}")
        print()
        
        # Build queries with competitors list
        print(f"📋 Building targeted queries...")
        queries = self.query_builder.get_queries(
            ad_type=ad_type,
            subject=subject,
            category=category,
            key_messages=teammate_output.key_messages,
            our_price=teammate_output.price,
            competitors=teammate_output.competitors  # PASS COMPETITORS!
        )
        print(f"✅ Built {len(queries)} targeted queries\n")
        
        # Execute
        print(f"🔍 Scraping web...")
        search_results = self._execute_searches(queries)
        
        # Quality check
        data_quality = self._assess_quality(search_results)
        print(f"\n📊 Data Quality: {data_quality}")
        
        # Fallback
        category_data = {}
        if data_quality in ["PARTIAL", "MINIMAL"]:
            print(f"\n⚠️ Limited data. Category research...")
            category_queries = self.query_builder.get_category_queries(category)
            category_results = self._execute_searches(category_queries)
            category_data = self._process_results(category_results)
        
        # Structure output
        scraped_data = self._structure_by_type(
            ad_type=ad_type,
            search_results=search_results,
            category_data=category_data,
            data_quality=data_quality,
            subject=subject,
            our_price=teammate_output.price,
            competitors=teammate_output.competitors  # PASS COMPETITORS!
        )
        
        print("\n✅ Scraping complete!\n")
        return scraped_data
    
    def _infer_category(self, description: str) -> str:
        """Infer category"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["smartphone", "phone"]):
            return "smartphones"
        elif any(word in desc_lower for word in ["laptop", "computer"]):
            return "laptops"
        elif any(word in desc_lower for word in ["software", "app"]):
            return "software"
        elif any(word in desc_lower for word in ["hackathon", "conference"]):
            return "tech events"
        
        return "technology"
    
    def _infer_ad_type(self, teammate_data: TeammateOutput) -> str:
        """Infer ad type"""
        desc = teammate_data.short_description.lower()
        
        if any(word in desc for word in ["hiring", "position", "role"]):
            return "job"
        if any(word in desc for word in ["hackathon", "conference", "event"]):
            return "event"
        
        return "product"
    
    def _execute_searches(self, queries: dict) -> dict:
        """Execute searches"""
        results = {}
        
        for query_name, query_text in queries.items():
            print(f"   → {query_name}...")
            
            try:
                response = self.linkup_client.search(
                    query=query_text,
                    depth="standard",
                    output_type="sourcedAnswer"
                )
                results[query_name] = response
                print(f"   ✅ {query_name}")
                
            except Exception as e:
                print(f"   ⚠️ {query_name} failed: {e}")
                results[query_name] = None
        
        return results
    
    def _assess_quality(self, results: dict) -> str:
        """Assess quality"""
        if not results:
            return "MINIMAL"
        
        successful = sum(1 for r in results.values() if r is not None)
        total = len(results)
        
        rate = successful / total if total > 0 else 0
        
        if rate >= 0.7:
            return "SUFFICIENT"
        elif rate >= 0.3:
            return "PARTIAL"
        else:
            return "MINIMAL"
    
    def _process_results(self, results: dict) -> dict:
        """Process results"""
        return {k: v for k, v in results.items() if v}
    
    def _structure_by_type(
        self,
        ad_type: str,
        search_results: dict,
        category_data: dict,
        data_quality: str,
        subject: str,
        our_price: str = None,
        competitors: list = None
    ) -> ScrapedData:
        """Structure by type"""
        
        if ad_type == "product":
            return self._structure_product_data(
                search_results, category_data, data_quality, 
                subject, our_price, competitors
            )
        elif ad_type == "event":
            return self._structure_event_data(
                search_results, category_data, data_quality, subject
            )
        elif ad_type == "job":
            return self._structure_job_data(
                search_results, category_data, data_quality, subject
            )
    
    def _structure_product_data(
        self,
        search_results: dict,
        category_data: dict,
        data_quality: str,
        subject: str,
        our_price: str = None,
        competitors: list = None
    ) -> ScrapedData:
        """
        PRODUCT: Build competitor breakdown
        """
        
        competitor_breakdown = {}
        market_gaps = []
        price_comparison = {}
        how_to_beat = {}
        
        # Process each competitor
        if competitors:
            for i, comp_name in enumerate(competitors[:2], 1):
                
                overview_key = f"competitor_{i}_overview"
                weakness_key = f"competitor_{i}_weaknesses"
                vs_key = f"competitor_{i}_vs_us"
                
                comp_data = {
                    "name": comp_name,
                    "overview": {},
                    "weaknesses": [],
                    "how_we_beat_them": []
                }
                
                # Extract overview
                if overview_key in search_results and search_results[overview_key]:
                    result = search_results[overview_key]
                    answer = getattr(result, 'answer', '')
                    sources = getattr(result, 'sources', [])
                    comp_data["overview"] = {
                        "description": answer,
                        "features": [getattr(s, 'name', '') for s in sources[:3]],
                        "sources": [getattr(s, 'url', '') for s in sources[:3]]
                    }
                
                # Extract weaknesses
                if weakness_key in search_results and search_results[weakness_key]:
                    result = search_results[weakness_key]
                    answer = getattr(result, 'answer', '')
                    # Split answer into bullet points
                    weaknesses = [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10]
                    comp_data["weaknesses"] = weaknesses[:5]
                
                # Extract comparison
                if vs_key in search_results and search_results[vs_key]:
                    result = search_results[vs_key]
                    answer = getattr(result, 'answer', '')
                    # Split answer into bullet points
                    comparisons = [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10]
                    comp_data["how_we_beat_them"] = comparisons[:3]
                
                competitor_breakdown[f"competitor_{i}"] = comp_data
        
        # Extract market gaps
        for query_name, result in search_results.items():
            if "market_gaps" in query_name and result:
                answer = getattr(result, 'answer', '')
                gaps = [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10]
                market_gaps = gaps[:5]
        
        # Extract pricing
        for query_name, result in search_results.items():
            if "pricing" in query_name and result:
                answer = getattr(result, 'answer', '')
                sources = getattr(result, 'sources', [])
                price_comparison = {
                    "our_price": our_price or "Not specified",
                    "market_analysis": answer,
                    "sources": [getattr(s, 'url', '') for s in sources[:3]]
                }
        
        # Build strategy
        all_weaknesses = []
        for comp_data in competitor_breakdown.values():
            all_weaknesses.extend(comp_data["weaknesses"])
        
        how_to_beat = {
            "exploit_competitor_weaknesses": all_weaknesses[:5],
            "fill_market_gaps": market_gaps[:3],
            "competitive_advantages": [
                f"Address {all_weaknesses[0] if all_weaknesses else 'competitor weakness'}",
                f"Fill gap: {market_gaps[0] if market_gaps else 'unmet need'}"
            ]
        }
        
        return ScrapedData(
            company_info={"product_name": subject},
            product_details={
                "positioning": "NEW product with competitive advantages"
            },
            competitor_analysis=competitor_breakdown,
            how_to_beat_them=how_to_beat,
            market_gaps=market_gaps,
            pricing_comparison=price_comparison,
            category_insights=category_data,
            data_quality=data_quality,
            scraping_timestamp=datetime.now().isoformat()
        )
    
    def _structure_event_data(self, search_results, category_data, data_quality, subject):
        """EVENT data"""
        success_metrics = {}
        testimonials = []
        
        for query_name, result in search_results.items():
            if not result:
                continue
            
            if "success" in query_name:
                answer = getattr(result, 'answer', '')
                success_metrics = {
                    "attendance": answer,
                    "sources": [getattr(s, 'url', '') for s in getattr(result, 'sources', [])[:3]]
                }
            
            if "testimonial" in query_name:
                answer = getattr(result, 'answer', '')
                testimonials = [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10][:5]
        
        return ScrapedData(
            company_info={"event_name": subject},
            event_success_metrics=success_metrics,
            attendee_testimonials=testimonials,
            category_insights=category_data,
            data_quality=data_quality,
            scraping_timestamp=datetime.now().isoformat()
        )
    
    def _structure_job_data(self, search_results, category_data, data_quality, subject):
        """JOB data"""
        culture = {}
        balance = {}
        benefits = {}
        
        for query_name, result in search_results.items():
            if not result:
                continue
            
            if "culture" in query_name:
                answer = getattr(result, 'answer', '')
                culture = {
                    "highlights": answer,
                    "reviews": [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10][:3]
                }
            
            if "balance" in query_name:
                answer = getattr(result, 'answer', '')
                balance = {
                    "rating": answer,
                    "feedback": [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10][:3]
                }
            
            if "benefit" in query_name or "compensation" in query_name:
                answer = getattr(result, 'answer', '')
                benefits = {
                    "salary": answer[:200] + "..." if len(answer) > 200 else answer,
                    "perks": [line.strip('- •').strip() for line in answer.split('\n') if line.strip() and len(line.strip()) > 10][:5]
                }
        
        return ScrapedData(
            company_info={"company_name": subject},
            company_culture=culture,
            work_life_balance=balance,
            benefits_info=benefits,
            category_insights=category_data,
            data_quality=data_quality,
            scraping_timestamp=datetime.now().isoformat()
        )