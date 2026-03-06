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
    # 动态适应文字长度，基础文字宽估计
    text_length = len(stars_str)
    font_size = 50 if text_length <= 3 else 40 if text_length == 4 else 30
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFE45E;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFB703;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <g filter="url(#shadow)">
    <!-- 绘制一个标准的五角星, 中心在(100,100), 外径90, 内径35 -->
    <polygon points="100,10 128,66 190,75 145,119 155,181 100,152 45,181 55,119 10,75 72,66" 
             fill="url(#starGrad)" stroke="#FB8500" stroke-width="4" stroke-linejoin="round"/>
  </g>
  
  <text x="100" y="115" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" 
        font-size="{font_size}" font-weight="900" fill="#202A44" text-anchor="middle" dominant-baseline="middle">
    {stars_str}
  </text>
  
  <text x="100" y="150" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" 
        font-size="16" font-weight="bold" fill="#B15700" text-anchor="middle" dominant-baseline="middle">
    STARS
  </text>
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
