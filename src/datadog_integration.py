"""
Datadog Integration Module for Social Media Ad Generator
Handles logging, metrics, and usage tracking
"""

import os
import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from datadog import initialize, api, statsd
from datadog.api.exceptions import ApiError
import json

class DatadogLogger:
    """Datadog logging and metrics handler"""
    
    def __init__(self):
        self.api_key = os.getenv('DD_API_KEY')
        self.app_key = os.getenv('DD_APP_KEY')
        self.site = os.getenv('DD_SITE', 'datadoghq.com')
        self.service = os.getenv('DD_SERVICE', 'social-media-ad-generator')
        self.env = os.getenv('DD_ENV', 'development')
        self.version = os.getenv('DD_VERSION', '1.0.0')
        self.org_name = os.getenv('DD_ORG_NAME', 'oct-04-hackathon-sfcoases-LMS')
        self.org_id = os.getenv('DD_ORG_ID', '09105ad2-9ae9-11f0-8c7b-bea17a92d134')
        
        self.initialized = False
        self._initialize_datadog()
    
    def _initialize_datadog(self):
        """Initialize Datadog connection"""
        if not self.api_key or not self.app_key:
            logging.warning("Datadog API keys not found. Logging will be disabled.")
            return
        
        try:
            initialize(
                api_key=self.api_key,
                app_key=self.app_key,
                api_host=f'https://api.{self.site}'
            )
            self.initialized = True
            logging.info("Datadog initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Datadog: {e}")
            self.initialized = False
    
    def log_event(self, title: str, text: str, tags: Optional[list] = None, alert_type: str = "info"):
        """Log an event to Datadog"""
        if not self.initialized:
            return
        
        try:
            default_tags = [
                f"service:{self.service}",
                f"env:{self.env}",
                f"version:{self.version}",
                f"org:{self.org_name}",
                f"org_id:{self.org_id}"
            ]
            
            if tags:
                default_tags.extend(tags)
            
            api.Event.create(
                title=title,
                text=text,
                tags=default_tags,
                alert_type=alert_type
            )
        except ApiError as e:
            logging.error(f"Failed to log event to Datadog: {e}")
    
    def increment_counter(self, metric_name: str, value: int = 1, tags: Optional[list] = None):
        """Increment a counter metric"""
        if not self.initialized:
            return
        
        try:
            default_tags = [
                f"service:{self.service}",
                f"env:{self.env}"
            ]
            
            if tags:
                default_tags.extend(tags)
            
            statsd.increment(metric_name, value, tags=default_tags)
        except Exception as e:
            logging.error(f"Failed to increment counter: {e}")
    
    def record_timing(self, metric_name: str, duration_ms: float, tags: Optional[list] = None):
        """Record a timing metric"""
        if not self.initialized:
            return
        
        try:
            default_tags = [
                f"service:{self.service}",
                f"env:{self.env}"
            ]
            
            if tags:
                default_tags.extend(tags)
            
            statsd.timing(metric_name, duration_ms, tags=default_tags)
        except Exception as e:
            logging.error(f"Failed to record timing: {e}")
    
    def record_gauge(self, metric_name: str, value: float, tags: Optional[list] = None):
        """Record a gauge metric"""
        if not self.initialized:
            return
        
        try:
            default_tags = [
                f"service:{self.service}",
                f"env:{self.env}"
            ]
            
            if tags:
                default_tags.extend(tags)
            
            statsd.gauge(metric_name, value, tags=default_tags)
        except Exception as e:
            logging.error(f"Failed to record gauge: {e}")
    
    def track_api_usage(self, endpoint: str, success: bool, duration_ms: float, 
                       user_id: Optional[str] = None, additional_tags: Optional[list] = None):
        """Track API usage metrics"""
        tags = [
            f"endpoint:{endpoint}",
            f"success:{success}",
            f"service:{self.service}"
        ]
        
        if user_id:
            tags.append(f"user_id:{user_id}")
        
        if additional_tags:
            tags.extend(additional_tags)
        
        # Increment API call counter
        self.increment_counter("api.calls.total", tags=tags)
        
        # Record timing
        self.record_timing("api.response_time", duration_ms, tags=tags)
        
        # Log success/failure
        if success:
            self.increment_counter("api.calls.success", tags=tags)
        else:
            self.increment_counter("api.calls.error", tags=tags)
    
    def track_ad_generation(self, product_type: str, target_audience: str, 
                           success: bool, duration_ms: float, user_id: Optional[str] = None):
        """Track ad generation metrics"""
        tags = [
            f"product_type:{product_type}",
            f"target_audience:{target_audience}",
            f"success:{success}",
            f"service:{self.service}"
        ]
        
        if user_id:
            tags.append(f"user_id:{user_id}")
        
        # Track ad generation
        self.increment_counter("ad.generation.total", tags=tags)
        self.record_timing("ad.generation.time", duration_ms, tags=tags)
        
        if success:
            self.increment_counter("ad.generation.success", tags=tags)
        else:
            self.increment_counter("ad.generation.error", tags=tags)
    
    def track_user_session(self, user_id: str, session_duration_ms: float, 
                          ads_generated: int, api_calls: int):
        """Track user session metrics"""
        tags = [
            f"user_id:{user_id}",
            f"service:{self.service}"
        ]
        
        # Session metrics
        self.record_gauge("user.session.duration", session_duration_ms, tags=tags)
        self.record_gauge("user.session.ads_generated", ads_generated, tags=tags)
        self.record_gauge("user.session.api_calls", api_calls, tags=tags)
        
        # Log session event
        self.log_event(
            title="User Session Completed",
            text=f"User {user_id} completed session with {ads_generated} ads generated",
            tags=tags
        )

# Global Datadog instance
dd_logger = DatadogLogger()

def track_api_call(endpoint: str, user_id: Optional[str] = None):
    """Decorator to track API calls"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                dd_logger.log_event(
                    title=f"API Error: {endpoint}",
                    text=f"Error in {endpoint}: {str(e)}",
                    tags=[f"endpoint:{endpoint}", f"error:{type(e).__name__}"],
                    alert_type="error"
                )
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                dd_logger.track_api_usage(endpoint, success, duration_ms, user_id)
        
        return wrapper
    return decorator

def track_ad_generation(product_type: str, target_audience: str, user_id: Optional[str] = None):
    """Decorator to track ad generation"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                dd_logger.log_event(
                    title="Ad Generation Error",
                    text=f"Failed to generate ad for {product_type}: {str(e)}",
                    tags=[f"product_type:{product_type}", f"error:{type(e).__name__}"],
                    alert_type="error"
                )
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                dd_logger.track_ad_generation(product_type, target_audience, success, duration_ms, user_id)
        
        return wrapper
    return decorator
