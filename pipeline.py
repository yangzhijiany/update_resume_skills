# -*- coding: utf-8 -*-
"""
Pipeline for updating resume skills:
1. Input JD URL
2. Extract job description text
3. Call LLM to extract and classify skills
4. Merge with existing resume skills (max 9 per category)
5. Update Word resume
"""

import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
from extractor import extract_jd_text
from update_resume import update_resume_skills

# ---------------- Config ----------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

# Fixed resume paths
INPUT_RESUME = os.getenv("INPUT_RESUME")
OUTPUT_RESUME = os.getenv("OUTPUT_RESUME")


# ---------------- Skill Extraction ----------------
def analyze_jd(text: str) -> dict:
    """
    Call LLM to extract and classify skills into:
    - programming
    - development
    - ai

    Constraints:
    - Only keep concrete skills mentioned in JD
    - Discard vague/broad terms (e.g., "backend technologies", "cloud platform")
    - Each category max 9 skills
    - Output strict JSON
    """
    prompt = f"""
    You are a "resume skill optimizer".
    From the following job description, extract skills and classify them.
    Categories:
    - programming: programming languages, frameworks, toolchains (e.g., Java, Python, React, Docker, Git)
    - development: databases, backend services, cloud services, devops (e.g., MySQL, MongoDB, AWS, Redis, Spring Boot)
    - ai: AI / Data Science / statistical modeling tools (e.g., R, Pandas, Regression analysis, Tableau, A/B Testing)

    Rules:
    1. Keep only concrete technical skills explicitly mentioned in the JD.
    2. Remove vague or overly broad terms (e.g., "backend technologies", "cloud platform").
    3. No more than 9 skills per category to avoid line wrapping in Word.
    4. Output valid JSON only. No explanations.

    Job description:
    {text}
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}  # force JSON
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)

    except Exception as e:
        print("JSON parse failed:", e)
        return {"programming": [], "development": [], "ai": []}


# ---------------- Merge Logic ----------------
def merge_skills(old_list, new_list, max_len=9):
    """
    Merge old and new skills:
    - Start from old_list
    - Add new_list items if not already present
    - Ensure total length <= max_len
    - If over limit, remove items from old_list first
    """
    merged = list(old_list)
    for skill in new_list:
        if skill not in merged:
            merged.append(skill)

    while len(merged) > max_len:
        for old in old_list:
            if old in merged:
                merged.remove(old)
                break
        if len(merged) > max_len:
            merged = merged[:max_len]

    return merged


# ---------------- Main ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <JD URL>")
        sys.exit(1)

    url = sys.argv[1]

    print(f"Fetching JD: {url}")
    jd_text = extract_jd_text(url)

    print("Analyzing skills...")
    extracted = analyze_jd(jd_text)

    # Default resume skills (used for merging)
    old_skills = {
        "programming": ["Java", "C/C++", "Python", "Vue.js", "React", "Docker", "Git"],
        "development": ["MySQL", "MongoDB", "Firebase", "Spring Boot", "Redis"],
        "ai": ["RAG", "R", "Pandas", "Regression analysis", "A/B Testing", "Tableau"]
    }

    new_skills = {
        "programming": merge_skills(old_skills["programming"], extracted.get("programming", [])),
        "development": merge_skills(old_skills["development"], extracted.get("development", [])),
        "ai": merge_skills(old_skills["ai"], extracted.get("ai", []))
    }

    print("\n=== Final Skills Written to Resume ===")
    print(json.dumps(new_skills, indent=2, ensure_ascii=False))

    update_resume_skills(INPUT_RESUME, OUTPUT_RESUME, new_skills)
