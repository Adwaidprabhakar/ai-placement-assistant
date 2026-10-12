import urllib.request
import json

BASE_URL = "http://127.0.0.1:8005/api"

def test_endpoint(name, url, method="GET", payload=None):
    try:
        data = json.dumps(payload).encode() if payload else None
        headers = {"Content-Type": "application/json"} if payload else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        res = urllib.request.urlopen(req)
        response_json = json.loads(res.read().decode('utf-8'))
        print(f"[OK] {name} SUCCESS (HTTP {res.status})")
        return response_json
    except Exception as e:
        print(f"[FAIL] {name} FAILED: {e}")
        return None

def run_all_tests():
    print("--- Starting Placement AI Full-Stack Endpoints Verification ---")
    
    # 1. Health
    test_endpoint("Health Check", f"{BASE_URL}/health")
    
    # 2. Chatbot
    test_endpoint("Module 1: Chatbot", f"{BASE_URL}/chatbot/chat", "POST", {
        "message": "What is the hiring process for Amazon SDE?",
        "session_id": "test_session_1"
    })
    
    # 3. Resume Generator
    test_endpoint("Module 2: Resume Analyzer", f"{BASE_URL}/resume/analyze", "POST", {
        "fullName": "Adwait Sharma",
        "skills": ["Python", "FastAPI", "React", "Data Structures"],
        "summary": "CS student looking for software developer opportunities."
    })
    
    # 4. Roadmap Generator
    test_endpoint("Module 3: Roadmap Generator", f"{BASE_URL}/roadmap/generate", "POST", {
        "role": "Software Development Engineer",
        "target_months": 6
    })
    
    # 5. Mock Interview
    test_endpoint("Module 4: Mock Interview", f"{BASE_URL}/interview/evaluate", "POST", {
        "question": "Tell me about a technical challenge you solved.",
        "user_transcript": "I optimized database queries by adding indexes and caching with Redis.",
        "role": "Software Engineer"
    })
    
    # 6. Technical DSA Studio
    test_endpoint("Module 5: DSA Problem Bank", f"{BASE_URL}/dsa/problems")
    test_endpoint("Module 5: DSA Code Runner", f"{BASE_URL}/dsa/run", "POST", {
        "problem_id": "two-sum",
        "code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        m = {}\n        for i, n in enumerate(nums):\n            if target - n in m:\n                return [m[target - n], i]\n            m[n] = i\n        return []\n"
    })
    test_endpoint("Module 5: DSA AI Hint", f"{BASE_URL}/dsa/hint", "POST", {
        "problem_id": "two-sum",
        "user_code": "class Solution:\n    def twoSum(self, nums, target):\n        pass"
    })

    print("--- Verification Finished ---")

if __name__ == "__main__":
    run_all_tests()
