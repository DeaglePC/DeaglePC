import json
import urllib.request
import os
import sys

def get_total_stars(username, token):
    stars = 0
    page = 1
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Star-Counter-Script"
    }
    if token:
        headers["Authorization"] = f"token {token}"
        
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                repos = json.loads(response.read().decode('utf-8'))
                if not repos:
                    break
                for repo in repos:
                    stars += repo.get("stargazers_count", 0)
            page += 1
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return stars

def generate_svg(stars):
    stars_str = str(stars)
    # Using a modern flat design badge
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="110" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="110" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0h70v20H0z"/>
    <path fill="#eebb00" d="M70 0h40v20H70z"/>
    <path fill="url(#b)" d="M0 0h110v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="35" y="15" fill="#010101" fill-opacity=".3">Total Stars</text>
    <text x="35" y="14">Total Stars</text>
    <text x="90" y="15" fill="#010101" fill-opacity=".3">{stars_str}</text>
    <text x="90" y="14">{stars_str}</text>
  </g>
</svg>"""

if __name__ == "__main__":
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "DeaglePC")
    token = os.environ.get("GH_TOKEN")
    
    total_stars = get_total_stars(username, token)
    print(f"Total stars for {username}: {total_stars}")
    
    os.makedirs("dist", exist_ok=True)
    with open("dist/stars_badge.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(total_stars))
    print("Successfully generated dist/stars_badge.svg")
