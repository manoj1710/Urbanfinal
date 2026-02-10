import time
import json
import requests
import sys
import os

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

def wait_for_server(retries=10, delay=2):
    print(f"Waiting for server at {BASE_URL}...")
    for _ in range(retries):
        try:
            requests.get(f"{BASE_URL}/health")
            print("Server is UP!")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(delay)
    print("Server failed to start.")
    return False

def test_endpoint(name, url, method="POST", data=None):
    print(f"\n--- Testing {name} ---")
    print(f"URL: {url}")
    if data:
        print(f"Input: {json.dumps(data, indent=2)}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response (Text): {response.text}")
            
        if response.status_code == 200:
            print(">>> PASS")
        else:
            print(">>> FAIL")
            
    except Exception as e:
        print(f"Error: {e}")
        print(">>> FAIL")

def run_tests():
    if not wait_for_server():
        sys.exit(1)

    # 1. Health
    test_endpoint("Health Check", f"{BASE_URL}/health", method="GET")

    # 2. Freshness
    test_endpoint("Freshness Prediction", f"{BASE_URL}/ai/freshness", data={
        "produced_date": "2023-10-25",
        "expiry_date": "2023-11-05", # 11 days shelf life
        "storage_type": "Refrigerated",
        "quality_grade": "A"
    })

    # 3. Spoilage
    test_endpoint("Spoilage Risk", f"{BASE_URL}/ai/spoilage-risk", data={
        "freshness": 78,
        "delay_hours": 3,
        "temperature": 8,
        "congestion": "High"
    })

    # 4. Priority
    test_endpoint("Priority Score", f"{BASE_URL}/ai/priority-score", data={
        "spoilage_risk": "High",
        "customer_demand": 85,
        "distance_km": 45
    })

    # 5. Route
    test_endpoint("Route Analysis", f"{BASE_URL}/ai/route-analysis", data={})

if __name__ == "__main__":
    run_tests()
