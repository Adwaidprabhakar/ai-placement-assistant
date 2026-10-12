import json
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.dsa_runner import dsa_runner
from app.services.llm_service import llm_service

router = APIRouter()

PROBLEMS_DB = [
    {
        "id": "two-sum",
        "title": "1. Two Sum",
        "difficulty": "Easy",
        "category": "Arrays & Hashing",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "starter_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Write your Python solution here\n        pass\n",
        "entry_class": "Solution",
        "entry_method": "twoSum",
        "test_cases": [
            {"args": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"args": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
            {"args": {"nums": [3, 3], "target": 6}, "expected": [0, 1]}
        ]
    },
    {
        "id": "valid-anagram",
        "title": "2. Valid Anagram",
        "difficulty": "Easy",
        "category": "Strings & Hashing",
        "description": "Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.",
        "starter_code": "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        # Write your Python solution here\n        pass\n",
        "entry_class": "Solution",
        "entry_method": "isAnagram",
        "test_cases": [
            {"args": {"s": "anagram", "t": "nagaram"}, "expected": True},
            {"args": {"s": "rat", "t": "car"}, "expected": False}
        ]
    },
    {
        "id": "container-with-most-water",
        "title": "3. Container With Most Water",
        "difficulty": "Medium",
        "category": "Two Pointers",
        "description": "Given an integer array `height` of length `n`, find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
        "starter_code": "class Solution:\n    def maxArea(self, height: list[int]) -> int:\n        # Write your Python solution here\n        pass\n",
        "entry_class": "Solution",
        "entry_method": "maxArea",
        "test_cases": [
            {"args": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected": 49},
            {"args": {"height": [1, 1]}, "expected": 1}
        ]
    },
    {
        "id": "reverse-linked-list",
        "title": "4. Reverse Array / List",
        "difficulty": "Easy",
        "category": "Arrays",
        "description": "Given a list of integers `nums`, return the array reversed.",
        "starter_code": "class Solution:\n    def reverseList(self, nums: list[int]) -> list[int]:\n        # Write your Python solution here\n        pass\n",
        "entry_class": "Solution",
        "entry_method": "reverseList",
        "test_cases": [
            {"args": {"nums": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]},
            {"args": {"nums": [10, 20]}, "expected": [20, 10]}
        ]
    }
]

class CodeRunRequest(BaseModel):
    problem_id: str
    code: str

class HintRequest(BaseModel):
    problem_id: str
    user_code: str

@router.get("/problems")
async def get_problems(difficulty: Optional[str] = Query(None)):
    if difficulty and difficulty != "All":
        return [p for p in PROBLEMS_DB if p["difficulty"].lower() == difficulty.lower()]
    return PROBLEMS_DB

@router.post("/submit")
@router.post("/run")
async def submit_code(req: CodeRunRequest):
    problem = next((p for p in PROBLEMS_DB if p["id"] == req.problem_id), PROBLEMS_DB[0])
    
    execution_result = dsa_runner.execute_solution(
        user_code=req.code,
        entry_class=problem["entry_class"],
        entry_method=problem["entry_method"],
        test_cases=problem["test_cases"]
    )
    
    return execution_result

@router.post("/hint")
async def get_hint(req: HintRequest):
    problem = next((p for p in PROBLEMS_DB if p["id"] == req.problem_id), PROBLEMS_DB[0])
    
    prompt = f"""Provide AI Tutor hint for coding problem:
Problem: {problem['title']}
Description: {problem['description']}
User Python Code Submission:
```python
{req.user_code}
```

Provide a helpful hint without giving away the full solution, an optimal logic explanation, expected Time Complexity, and Space Complexity. Output JSON."""

    system_prompt = "You are an AI DSA Tutor. Output pure JSON with keys: hint (str), logic_explanation (str), time_complexity (str), space_complexity (str)."

    response_text = await llm_service.generate_response(prompt, system_prompt=system_prompt)

    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            return json.loads(response_text[start_idx:end_idx])
    except Exception:
        pass

    return {
        "hint": "Try using a Hash Map to store elements you have seen along with their indices.",
        "logic_explanation": "As you iterate through array x, check if (target - x) exists in hash map. If found, return [map[target - x], i].",
        "time_complexity": "O(N) - single pass through array",
        "space_complexity": "O(N) - storing elements in Hash Map"
    }
