import sys
import os
from extractor import extract_jd_text
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ Please set OPENAI_API_KEY in your .env file")

client = OpenAI(api_key=api_key)


def analyze_jd(text: str) -> str:
    """
    Call LLM to extract technical skills and tools from the job description.
    Output: JSON with keys "technical_skills" and "tools".
    """
    prompt = f"""
    From the following job description, extract only technical skills and tools.
    Output strict JSON in the format:
    {{
      "technical_skills": [...],
      "tools": [...]
    }}

    Job description:
    {text}
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <JD_URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"🔎 Fetching JD: {url}")
    jd_text = extract_jd_text(url)
    print("✅ JD text fetched (saved to jd_text.txt if needed)")

    print("🤖 Analyzing skills...")
    skills = analyze_jd(jd_text)

    print("\n=== Extracted Skills ===")
    print(skills)
