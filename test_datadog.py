#!/usr/bin/env python3
"""
Test script for Datadog integration
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add src directory to path
sys.path.append('src')

# Load environment variables
load_dotenv()

def test_datadog_integration():
    """Test Datadog integration with provided credentials"""
    print("🐕 Testing Datadog Integration...")
    print("=" * 50)
    
    try:
        from datadog_integration import dd_logger
        
        print(f"✅ Datadog Logger initialized: {dd_logger.initialized}")
        print(f"📊 Service: {dd_logger.service}")
        print(f"🏢 Organization: {dd_logger.org_name}")
        print(f"🔑 API Key: {dd_logger.api_key[:10]}..." if dd_logger.api_key else "❌ No API Key")
        print(f"🔑 App Key: {dd_logger.app_key[:10]}..." if dd_logger.app_key else "❌ No App Key")
        print()
        
        if not dd_logger.initialized:
            print("❌ Datadog not initialized. Check your API keys.")
            return False
        
        # Test 1: Log an event
        print("📝 Testing event logging...")
        dd_logger.log_event(
            title="Social Media Ad Generator - Test Event",
            text="Testing Datadog integration with provided credentials",
            tags=["test:integration", "hackathon:oct-04-sfcoases"]
        )
        print("✅ Event logged successfully")
        
        # Test 2: Increment counter
        print("📊 Testing counter metrics...")
        dd_logger.increment_counter(
            "test.integration.counter",
            value=1,
            tags=["test:counter", "hackathon:oct-04-sfcoases"]
        )
        print("✅ Counter incremented successfully")
        
        # Test 3: Record timing
        print("⏱️ Testing timing metrics...")
        dd_logger.record_timing(
            "test.integration.timing",
            duration_ms=150.5,
            tags=["test:timing", "hackathon:oct-04-sfcoases"]
        )
        print("✅ Timing recorded successfully")
        
        # Test 4: Record gauge
        print("📈 Testing gauge metrics...")
        dd_logger.record_gauge(
            "test.integration.gauge",
            value=42.0,
            tags=["test:gauge", "hackathon:oct-04-sfcoases"]
        )
        print("✅ Gauge recorded successfully")
        
        # Test 5: Track API usage
        print("🔌 Testing API usage tracking...")
        dd_logger.track_api_usage(
            endpoint="test-endpoint",
            success=True,
            duration_ms=250.0,
            user_id="test-user-123",
            additional_tags=["test:api", "hackathon:oct-04-sfcoases"]
        )
        print("✅ API usage tracked successfully")
        
        # Test 6: Track ad generation
        print("🎨 Testing ad generation tracking...")
        dd_logger.track_ad_generation(
            product_type="test-product",
            target_audience="test-audience",
            success=True,
            duration_ms=500.0,
            user_id="test-user-123"
        )
        print("✅ Ad generation tracked successfully")
        
        print()
        print("🎉 All Datadog integration tests passed!")
        print("📊 Check your Datadog dashboard at: https://app.datadoghq.com/")
        print(f"🏢 Organization: {dd_logger.org_name}")
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import Datadog integration: {e}")
        print("💡 Make sure you've installed the datadog package: pip install datadog")
        return False
    except Exception as e:
        print(f"❌ Datadog integration test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints with Datadog tracking"""
    print("\n🔌 Testing API endpoints with Datadog...")
    print("=" * 50)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ API health check passed")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False
    
    # Test generate-copy endpoint
    try:
        test_data = {
            "product_description": "Test Product for Datadog Integration",
            "target_audience": "test audience",
            "price_range": "$10-20",
            "ad_style": "modern"
        }
        
        response = requests.post(f"{base_url}/generate-copy", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Generate copy endpoint test passed")
            print("📊 This should have generated Datadog metrics!")
        else:
            print(f"❌ Generate copy endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Generate copy endpoint test failed: {e}")
        return False
    
    print("🎉 API endpoint tests completed!")
    print("📊 Check Datadog for API metrics and events")
    return True

if __name__ == "__main__":
    print("🚀 Social Media Ad Generator - Datadog Integration Test")
    print("=" * 60)
    
    # Test Datadog integration
    integration_success = test_datadog_integration()
    
    if integration_success:
        # Test API endpoints
        api_success = test_api_endpoints()
        
        if api_success:
            print("\n🎉 All tests passed! Datadog integration is working correctly.")
            print("\n📊 Next steps:")
            print("1. Check your Datadog dashboard for metrics and events")
            print("2. Set up alerts for error rates and performance")
            print("3. Create custom dashboards for your application")
        else:
            print("\n❌ API endpoint tests failed. Check your FastAPI server.")
    else:
        print("\n❌ Datadog integration tests failed. Check your configuration.")
    
    print("\n" + "=" * 60)
