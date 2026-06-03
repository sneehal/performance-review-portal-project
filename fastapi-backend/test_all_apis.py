# test_all_apis.py
# Tests all APIs in correct order
# Run: python test_all_apis.py

import requests
import json

BASE = "http://localhost:8000"

def print_result(name, response):
    status = "✅" if response.status_code < 400 else "❌"
    print(f"{status} {name}")
    print(f"   Status : {response.status_code}")
    try:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
    except Exception:
        print(f"   Response: {response.text[:200]}")
    print()

print("=" * 60)
print("Testing All Performance Review Portal APIs")
print("=" * 60 + "\n")

# ── AUTH ──────────────────────────────────────────────────────
print("AUTH APIs")

# Login HR Admin
r = requests.post(f"{BASE}/auth/login",
    json={"email": "sarah.hr@company.com", "password": "Test@1234"})
print_result("POST /auth/login (HR Admin)", r)
sarah_token = r.json()["data"]["access_token"]
sarah_headers = {"Authorization": f"Bearer {sarah_token}"}

# Login Manager
r = requests.post(f"{BASE}/auth/login",
    json={"email": "mike.manager@company.com", "password": "Test@1234"})
print_result("POST /auth/login (Manager)", r)
mike_token = r.json()["data"]["access_token"]
mike_headers = {"Authorization": f"Bearer {mike_token}"}

# Login Employee
r = requests.post(f"{BASE}/auth/login",
    json={"email": "alice.emp@company.com", "password": "Test@1234"})
print_result("POST /auth/login (Employee)", r)
alice_token = r.json()["data"]["access_token"]
alice_headers = {"Authorization": f"Bearer {alice_token}"}

# Login Bob
r = requests.post(f"{BASE}/auth/login",
    json={"email": "bob.emp@company.com", "password": "Test@1234"})
bob_token = r.json()["data"]["access_token"]
bob_headers = {"Authorization": f"Bearer {bob_token}"}

# Get profile
r = requests.get(f"{BASE}/auth/me", headers=alice_headers)
print_result("GET /auth/me", r)

# ── REVIEW CYCLES ─────────────────────────────────────────────
print("REVIEW CYCLE APIs")

r = requests.get(f"{BASE}/review-cycles", headers=sarah_headers)
print_result("GET /review-cycles", r)

r = requests.post(f"{BASE}/review-cycles", headers=sarah_headers,
    json={
        "name": "Q3 2025 Appraisal",
        "start_date": "2025-07-01",
        "end_date": "2025-09-30",
        "self_due_date": "2025-09-15",
        "manager_due_date": "2025-09-25"
    })
print_result("POST /review-cycles", r)

r = requests.get(f"{BASE}/review-cycles/2/progress", headers=sarah_headers)
print_result("GET /review-cycles/2/progress", r)

# ── GOALS ─────────────────────────────────────────────────────
print("GOAL APIs")

r = requests.get(f"{BASE}/goals/my?cycle_id=2", headers=alice_headers)
print_result("GET /goals/my?cycle_id=2 (Alice)", r)

r = requests.put(f"{BASE}/goals/3/achievement", headers=alice_headers,
    json={"achievement": "Updated achievement text via API test"})
print_result("PUT /goals/3/achievement", r)

# ── REVIEWS ───────────────────────────────────────────────────
print("REVIEW APIs")

r = requests.get(f"{BASE}/reviews/my/2", headers=alice_headers)
print_result("GET /reviews/my/2 (Alice)", r)

# ── MANAGER ───────────────────────────────────────────────────
print("MANAGER APIs")

r = requests.get(f"{BASE}/manager/pending-reviews", headers=mike_headers)
print_result("GET /manager/pending-reviews", r)

r = requests.get(f"{BASE}/manager/team-summary", headers=mike_headers)
print_result("GET /manager/team-summary", r)

r = requests.get(f"{BASE}/manager/compare/1", headers=mike_headers)
print_result("GET /manager/compare/1", r)

# ── COMPETENCIES ──────────────────────────────────────────────
print("COMPETENCY APIs")

r = requests.get(f"{BASE}/competencies", headers=alice_headers)
print_result("GET /competencies", r)

r = requests.get(f"{BASE}/competencies/ratings/1", headers=alice_headers)
print_result("GET /competencies/ratings/1", r)

# ── ADMIN REPORTS ─────────────────────────────────────────────
print("ADMIN REPORT APIs")

r = requests.get(f"{BASE}/admin/reports/ratings-summary", headers=sarah_headers)
print_result("GET /admin/reports/ratings-summary", r)

r = requests.get(f"{BASE}/admin/reports/completion", headers=sarah_headers)
print_result("GET /admin/reports/completion", r)

r = requests.get(f"{BASE}/admin/reports/export", headers=sarah_headers)
print(f"GET /admin/reports/export")
print(f"   Status: {r.status_code}")
print(f"   Content-Type: {r.headers.get('content-type')}")
print(f"   CSV Preview: {r.text[:300]}")
print()

print("=" * 60)
print("All API tests complete!")
print("=" * 60)
