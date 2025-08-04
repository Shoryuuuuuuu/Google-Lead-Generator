import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def check_website_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_company_insight(link):
    try:
        resp = requests.get(link, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text() for p in paragraphs[:3])
        return text.strip()
    except:
        return "No insight available"

def find_social_media_links(link):
    try:
        resp = requests.get(link, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        anchors = soup.find_all('a', href=True)
        social_links = {
            'LinkedIn': '',
            'Instagram': '',
            'Twitter': '',
            'Facebook': ''
        }
        for a in anchors:
            href = a['href']
            if 'linkedin.com' in href and not social_links['LinkedIn']:
                social_links['LinkedIn'] = href
            elif 'instagram.com' in href and not social_links['Instagram']:
                social_links['Instagram'] = href
            elif 'twitter.com' in href and not social_links['Twitter']:
                social_links['Twitter'] = href
            elif 'facebook.com' in href and not social_links['Facebook']:
                social_links['Facebook'] = href
        return social_links
    except:
        return {
            'LinkedIn': '',
            'Instagram': '',
            'Twitter': '',
            'Facebook': ''
        }

def score_lead(snippet, active):
    score = 0
    if active:
        score += 5
    if snippet:
        score += 3 if len(snippet) > 100 else 1
    return score

def scrape_google(keyword, pages=1):
    api_key = "7260b89ba2b3386bbde38e4590ddb0a44891def7d7fc3d58cd9ec6c3ef2d532c"  # ← Ganti dengan API key kamu
    results = []

    for page in range(pages):
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": api_key,
            "start": page * 10
        }

        search = GoogleSearch(params)
        data = search.get_dict()
        organic_results = data.get("organic_results", [])

        for result in organic_results:
            title = result.get("title")
            link = result.get("link")
            snippet = result.get("snippet", "")
            active = check_website_status(link)
            valid = is_valid_url(link)
            insight = get_company_insight(link)
            socials = find_social_media_links(link)
            score = score_lead(snippet, active)

            results.append({
                "Title": title,
                "Link": link,
                "Snippet": snippet,
                "Active": "Yes" if active else "No",
                "Valid URL": "Yes" if valid else "No",
                "Insight": insight,
                "Score": score,
                "LinkedIn": socials['LinkedIn'],
                "Instagram": socials['Instagram'],
                "Twitter": socials['Twitter'],
                "Facebook": socials['Facebook']
            })

    return results
