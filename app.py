# 保存为 app.py，无需安装任何依赖
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import random
from datetime import datetime


# 生成模拟污染数据（支持任意城市）
def generate_pollution_data(city):
    pm25 = random.randint(0, 500)

    # 确定空气质量等级
    if pm25 <= 50:
        level = "Good"
        color = "green"
        advice = "Air quality is excellent, suitable for outdoor activities."
    elif pm25 <= 100:
        level = "Moderate"
        color = "yellow"
        advice = "Air quality is acceptable, but sensitive groups should reduce outdoor activities."
    elif pm25 <= 150:
        level = "Unhealthy for Sensitive Groups"
        color = "orange"
        advice = "Sensitive groups should avoid prolonged outdoor activities."
    elif pm25 <= 200:
        level = "Unhealthy"
        color = "red"
        advice = "Reduce outdoor activities; sensitive groups should stay indoors."
    elif pm25 <= 300:
        level = "Very Unhealthy"
        color = "purple"
        advice = "Everyone should minimize outdoor activities."
    else:
        level = "Hazardous"
        color = "maroon"
        advice = "Close windows and avoid all outdoor activities."

    return {
        "city": city,
        "pm25": pm25,
        "pm10": random.randint(0, 300),
        "o3": random.randint(0, 200),
        "no2": random.randint(0, 100),
        "so2": random.randint(0, 50),
        "co": round(random.uniform(0, 10), 1),
        "level": level,
        "color": color,
        "advice": advice,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# 热门城市列表（英文）
POPULAR_CITIES = [
    "Beijing", "Shanghai", "New York", "London", "Paris", "Tokyo",
    "Sydney", "Moscow", "Los Angeles", "Singapore", "Seoul", "Berlin",
    "Toronto", "Vancouver", "Bangkok", "Dubai", "São Paulo", "Mumbai",
    "Istanbul", "Sydney"
]

# HTML模板 - 基础模板
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }}
        body {{ background-color: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ width: 90%; max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        header {{ 
            background-color: #2c3e50; 
            color: white; 
            padding: 1.5rem 0; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .logo {{ display: flex; align-items: center; gap: 10px; }}
        .logo h1 {{ font-size: 1.8rem; font-weight: 600; }}
        main {{ padding: 2rem 0; min-height: calc(100vh - 150px); }}
        footer {{ 
            background-color: #2c3e50; 
            color: white; 
            text-align: center; 
            padding: 1.5rem 0; 
            margin-top: 3rem;
        }}
        .search-section {{ 
            background: white; 
            border-radius: 10px; 
            padding: 2.5rem; 
            margin-bottom: 2rem; 
            text-align: center; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        .search-section h2 {{ 
            font-size: 2rem; 
            margin-bottom: 0.8rem; 
            color: #2c3e50;
        }}
        .search-form {{ max-width: 700px; margin: 0 auto 2rem; }}
        .search-box {{ display: flex; }}
        .search-box input {{ 
            flex: 1; 
            padding: 0.8rem; 
            border: 2px solid #e1e4e8; 
            border-right: none; 
            border-radius: 8px 0 0 8px; 
            font-size: 1rem;
        }}
        .search-box button {{ 
            background: #3498db; 
            color: white; 
            border: none; 
            padding: 0 1.5rem; 
            border-radius: 0 8px 8px 0; 
            cursor: pointer; 
            font-weight: 500;
        }}
        .city-tags {{ 
            display: flex; 
            flex-wrap: wrap; 
            gap: 0.8rem; 
            margin-top: 1rem;
            justify-content: center;
        }}
        .city-tags a {{ 
            background: #e8f4fd; 
            color: #3498db; 
            padding: 0.5rem 1.2rem; 
            border-radius: 20px; 
            text-decoration: none; 
            font-size: 0.95rem;
        }}
        .index-guide {{ 
            display: flex; 
            flex-wrap: wrap; 
            gap: 1rem; 
            justify-content: center; 
            margin-top: 1rem;
        }}
        .index-item {{ 
            text-align: center; 
            padding: 1rem; 
            border-radius: 8px; 
            min-width: 120px; 
            color: white; 
            font-weight: 500;
        }}
        .results-header {{ margin-bottom: 2rem; }}
        .back-link a {{ 
            color: #3498db; 
            text-decoration: none; 
            display: inline-flex; 
            align-items: center; 
            margin-bottom: 1rem;
        }}
        .main-pollution {{ 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 2rem; 
            margin-bottom: 2rem;
        }}
        @media (max-width: 768px) {{
            .main-pollution {{ grid-template-columns: 1fr; }}
        }}
        .pm25-card, .health-advice {{ 
            background: white; 
            border-radius: 10px; 
            padding: 2rem; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        .pm25-value {{ 
            font-size: 4rem; 
            font-weight: bold; 
            margin: 1rem 0; 
            color: white; 
            text-align: center;
        }}
        .pollutants-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); 
            gap: 1.5rem; 
            margin-top: 1rem;
        }}
        .pollutant-card {{ 
            background: #f9f9f9; 
            border-radius: 8px; 
            padding: 1.5rem; 
            text-align: center;
        }}
        .green {{ background-color: #2ecc71; }}
        .yellow {{ background-color: #f39c12; }}
        .orange {{ background-color: #e67e22; }}
        .red {{ background-color: #e74c3c; }}
        .purple {{ background-color: #9b59b6; }}
        .maroon {{ background-color: #c0392b; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">
                <h1>Global Pollution Index</h1>
            </div>
        </div>
    </header>
    <main class="container">
        {content}
    </main>
    <footer>
        <div class="container">
            <p>© 2023 Global Pollution Index | Data for reference only</p>
        </div>
    </footer>
</body>
</html>
"""

# 首页内容
INDEX_HTML = """
<section class="search-section">
    <h2>Check Pollution Index Worldwide</h2>
    <p>Get real-time air quality data including PM2.5, PM10 and other pollutants</p>

    <form action="/search" method="get" class="search-form">
        <div class="search-box">
            <input type="text" name="city" placeholder="Enter city name..." required>
            <button type="submit">Search</button>
        </div>
    </form>

    <div>
        <h3>Popular Cities</h3>
        <div class="city-tags">
            {city_tags}
        </div>
    </div>

    <div style="margin-top: 2rem;">
        <h3>Air Quality Index Guide</h3>
        <div class="index-guide">
            <div class="index-item green"><span>0-50</span><p>Good</p></div>
            <div class="index-item yellow"><span>51-100</span><p>Moderate</p></div>
            <div class="index-item orange"><span>101-150</span><p>Unhealthy for Sensitive Groups</p></div>
            <div class="index-item red"><span>151-200</span><p>Unhealthy</p></div>
            <div class="index-item purple"><span>201-300</span><p>Very Unhealthy</p></div>
            <div class="index-item maroon"><span>301+</span><p>Hazardous</p></div>
        </div>
    </div>
</section>
"""

# 结果页内容
RESULTS_HTML = """
<section class="results-header">
    <div class="back-link">
        <a href="/">← Back to search</a>
    </div>
    {content}
</section>
"""


class PollutionHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)

        # 首页
        if parsed_url.path == '/':
            self._set_headers()
            # 生成热门城市标签
            city_tags = ''.join([f'<a href="/search?city={city}">{city}</a>' for city in POPULAR_CITIES[:8]])
            index_content = INDEX_HTML.format(city_tags=city_tags)
            html = BASE_HTML.format(title="Global Pollution Index", content=index_content)
            self.wfile.write(html.encode('utf-8'))

        # 搜索结果页 - 支持任何城市
        elif parsed_url.path == '/search':
            self._set_headers()
            query_params = parse_qs(parsed_url.query)
            city = query_params.get('city', [''])[0].strip()

            if not city:
                content = "<h2>Please enter a city name</h2>"
            else:
                # 对任何输入的城市都生成数据
                data = generate_pollution_data(city)
                content = f"""
                <h2>Real-time Pollution Index - {data['city']}</h2>
                <p>Last updated: {data['updated']}</p>

                <div class="main-pollution">
                    <div class="pm25-card">
                        <h3>PM2.5 Index</h3>
                        <div class="pm25-value {data['color']}">{data['pm25']}</div>
                        <div>Air Quality: <span class="{data['color']}" style="color: white; padding: 3px 8px; border-radius: 4px;">{data['level']}</span></div>
                    </div>

                    <div class="health-advice">
                        <h3>Health Advice</h3>
                        <p>{data['advice']}</p>
                    </div>
                </div>

                <div style="background: white; border-radius: 10px; padding: 2rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                    <h3>Detailed Pollutant Data</h3>
                    <div class="pollutants-grid">
                        <div class="pollutant-card">
                            <h4>PM10</h4>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #3498db;">{data['pm10']} μg/m³</div>
                            <div>Inhalable Particles</div>
                        </div>
                        <div class="pollutant-card">
                            <h4>Ozone (O₃)</h4>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #3498db;">{data['o3']} μg/m³</div>
                        </div>
                        <div class="pollutant-card">
                            <h4>Nitrogen Dioxide (NO₂)</h4>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #3498db;">{data['no2']} μg/m³</div>
                        </div>
                        <div class="pollutant-card">
                            <h4>Sulfur Dioxide (SO₂)</h4>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #3498db;">{data['so2']} μg/m³</div>
                        </div>
                        <div class="pollutant-card">
                            <h4>Carbon Monoxide (CO)</h4>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #3498db;">{data['co']} mg/m³</div>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 2rem;">
                    <h3>Search Other Cities</h3>
                    <div class="city-tags">
                        {''.join([f'<a href="/search?city={c}">{c}</a>' for c in POPULAR_CITIES[:5]])}
                    </div>
                </div>
                """

            results_content = RESULTS_HTML.format(content=content)
            html = BASE_HTML.format(title=f"{city} - Pollution Index", content=results_content)
            self.wfile.write(html.encode('utf-8'))

        # 404页面
        else:
            self._set_headers(404)
            html = BASE_HTML.format(title="Page Not Found",
                                    content="<h2>404 - Page Not Found</h2><p><a href='/'>Return to homepage</a></p>")
            self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, PollutionHandler)
    print(f"Server started, visit http://localhost:{port} to view the website")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Server stopped")