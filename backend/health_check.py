#!/usr/bin/env python3
"""
Simple health check script for monitoring.
Can be used with external monitoring services (UptimeRobot, Pingdom, etc.)
"""

import sys
import requests
from urllib.parse import urljoin

def check_health(base_url: str) -> bool:
    """Check if the API is healthy"""
    try:
        health_url = urljoin(base_url, "/health")
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print(f"✅ API is healthy: {base_url}")
                print(f"   Service: {data.get('service', 'unknown')}")
                print(f"   Version: {data.get('version', 'unknown')}")
                print(f"   Environment: {data.get('environment', 'unknown')}")
                return True
        
        print(f"❌ API returned unhealthy status: {response.status_code}")
        return False
        
    except requests.exceptions.Timeout:
        print(f"❌ API health check timed out: {base_url}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API: {base_url}")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python health_check.py <api_url>")
        print("Example: python health_check.py https://medvision-ai-backend.onrender.com")
        sys.exit(1)
    
    api_url = sys.argv[1]
    
    print(f"🔍 Checking API health: {api_url}")
    print("-" * 60)
    
    is_healthy = check_health(api_url)
    
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()
