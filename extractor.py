# -*- coding: utf-8 -*-
"""
Enhanced extractor.py
1. Try requests first
2. If failed, fall back to Playwright (headless Chromium)
Supports: iCIMS, Workday, Greenhouse, Ashby, Lever, SmartRecruiters, BambooHR, etc.
"""

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def _extract_from_html(html: str, url: str) -> str:
    """Extract job description text from HTML for common ATS platforms."""
    soup = BeautifulSoup(html, "html.parser")
    domain = url.lower()

    # iCIMS
    if "icims.com" in domain:
        job_content = soup.find("div", id="jobcontent")
        if job_content:
            return job_content.get_text(" ", strip=True)

    # Workday
    if "myworkdayjobs.com" in domain:
        selectors = [
            {"data-automation-id": "jobPostingDescription"},
            {"data-automation-id": "richTextArea"},
            {"role": "text"},
        ]
        for c in selectors:
            wd_div = soup.find("div", c)
            if wd_div:
                return wd_div.get_text(" ", strip=True)
        wd_section = soup.find("section")
        if wd_section:
            return wd_section.get_text(" ", strip=True)

    # Greenhouse
    if "greenhouse.io" in domain:
        gh_div = soup.find("div", class_="job")
        if gh_div:
            return gh_div.get_text(" ", strip=True)

    # Ashby
    if "ashbyhq.com" in domain:
        ashby_div = soup.find("div", {"data-testid": "JobDescription"})
        if ashby_div:
            return ashby_div.get_text(" ", strip=True)

    # Lever
    if "lever.co" in domain:
        lever_div = soup.find("div", class_="posting")
        if lever_div:
            return lever_div.get_text(" ", strip=True)

    # SmartRecruiters
    if "smartrecruiters.com" in domain:
        sr_div = soup.find("div", class_="job-sections")
        if sr_div:
            return sr_div.get_text(" ", strip=True)

    # BambooHR
    if "bamboohr.com" in domain:
        bh_div = soup.find("div", id="content")
        if bh_div:
            return bh_div.get_text(" ", strip=True)

    # Fallback
    body_text = soup.get_text(" ", strip=True)
    if body_text:
        return body_text

    return ""


def extract_jd_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, timeout=15, headers=headers)
        text = _extract_from_html(res.text, url)
        if text and len(text) > 200:
            print("Extracted via requests")
            return text
    except Exception as e:
        print(f"requests failed: {e}")

    # Fallback: Playwright
    print("Falling back to Playwright rendering...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(5000)  # wait 5s for dynamic content
        html = page.content()
        browser.close()

    text = _extract_from_html(html, url)
    if not text:
        raise RuntimeError("Failed to extract job description after Playwright rendering: " + url)

    print("Extracted via Playwright")
    return text


# ----------- Test -----------
if __name__ == "__main__":
    test_url = "https://allegion.wd5.myworkdayjobs.com/en-US/careers/job/Golden-CO/Summer-Intern---Software-Engineering---Platform-Software_JR33861"
    jd = extract_jd_text(test_url)
    print("First 500 chars:\n", jd[:500])
