import os
import yaml

# 設定輸入與輸出路徑
YAML_FILE = "itinerary.yaml"
OUTPUT_HTML = "index.html"

# 1. 確保外部 YAML 檔案存在並正確讀取
if not os.path.exists(YAML_FILE):
    raise FileNotFoundError(f"❌ 錯誤：找不到 {YAML_FILE} 檔案！請確保它與此腳本放在同一個資料夾。")

with open(YAML_FILE, "r", encoding="utf-8") as f:
    aomori_data = yaml.safe_load(f)

# 2. 網頁 HTML & CSS 模板（更新：加入圖片固定寬高比防止滾動跑位）
html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍏 2026 青森家族自駕之旅 ｜ 五天四夜初夏新綠完美行程</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f2f7f4;
            --card-bg: #ffffff;
            --primary-color: #1b4332; 
            --accent-red: #d90429;    
            --text-dark: #2b2d42;
            --soft-green: #40916c;
            --option-bg: #f8fdfa;     
            --option-border: #b7e4c7; 
        }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Noto Sans TC', sans-serif; background-color: var(--bg-color); color: var(--text-dark); margin: 0; padding-bottom: 80px; }}
        header {{ position: relative; background-image: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.65)), url('https://lipstb.com/wp-content/uploads/2021/04/hirosakipark-greenseason-scaled.jpg'); background-size: cover; background-position: center; color: white; text-align: center; padding: 40px 15px 30px 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        header h1 {{ margin: 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.6); }}
        header p {{ margin: 8px 0 20px 0; font-size: 1rem; opacity: 0.95; font-weight: 500; text-shadow: 0 1px 3px rgba(0,0,0,0.6); }}
        .weather-tip-box {{ max-width: 570px; margin: 0 auto; background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 12px; padding: 14px 18px; font-size: 0.88rem; color: #ffffff; line-height: 1.6; text-align: left; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }}
        .weather-tip-box b {{ color: #ffeaa7; font-size: 0.95rem; }}
        .weather-tip-box ul {{ margin: 6px 0 0 0; padding-left: 20px; }}
        .day-scroller {{ position: sticky; top: 0; background: rgba(255, 255, 255, 0.97); box-shadow: 0 3px 10px rgba(0,0,0,0.08); display: flex; overflow-x: auto; padding: 12px 8px; z-index: 1000; }}
        .day-scroller::-webkit-scrollbar {{ display: none; }}
        .day-badge {{ display: inline-block; padding: 8px 16px; margin: 0 4px; background-color: #e9ecef; color: var(--text-dark); border-radius: 20px; text-decoration: none; font-size: 0.85rem; font-weight: 500; white-space: nowrap; }}
        .day-badge.active {{ background-color: var(--soft-green); color: white; font-weight: bold; }}
        .container {{ max-width: 600px; margin: 15px auto; padding: 0 12px; }}
        .country-header {{ border-left: 6px solid var(--accent-red); padding-left: 12px; margin: 20px 0 15px 0; font-size: 1.3rem; color: var(--primary-color); font-weight: bold; }}
        
        /* 🌤️ 每日天氣提示方塊樣式 */
        .weather-info-box {{ background-color: #f0f7ff; border-left: 5px solid #007bff; padding: 12px; margin: 12px 0; border-radius: 0 8px 8px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.02); }}
        .weather-info-title {{ margin: 0 0 6px 0; font-weight: 700; font-size: 0.92rem; color: #2b2d42; }}
        .weather-info-tip {{ margin: 0; font-size: 0.85rem; color: #555; line-height: 1.5; }}
        
        /* 修正：增加 scroll-margin-top 確保不被上方固定 Scroller 擋到 */
        .day-card {{ background: var(--card-bg); border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 20px; padding: 18px; scroll-margin-top: 75px; }}
        .day-card-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #e9ecef; padding-bottom: 10px; margin-bottom: 12px; }}
        .day-tag {{ background: var(--primary-color); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; }}
        .day-date {{ color: var(--accent-red); font-weight: 700; font-size: 1rem; }}
        .day-title {{ font-size: 1.15rem; font-weight: 700; margin: 10px 0; color: #111111; line-height: 1.4; }}
        .item-block {{ background: #fafafa; border-left: 4px solid var(--soft-green); padding: 12px; margin-top: 15px; border-radius: 0 8px 8px 0; }}
        .time-tag {{ display: inline-block; background-color: #f1f3f5; color: #495057; font-size: 0.8rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; margin-bottom: 8px; border: 1px solid #dee2e6; }}
        .item-title {{ font-weight: 700; font-size: 1rem; color: #222; margin-top: 2px; margin-bottom: 10px; }}
        
        /* 修正：限制圖片高度並設定寬高比，防非同步載入撐開元件導致定位飄開 */
        .item-img {{ width: 100%; height: auto; max-height: 220px; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; margin-bottom: 10px; background-color: #e9ecef; }}
        
        .item-details {{ margin: 8px 0 0 0; padding-left: 18px; font-size: 0.9rem; color: #444; line-height: 1.5; }}
        .item-details li {{ margin-bottom: 4px; }}
        .food-option-card {{ background: var(--option-bg); border: 1px solid var(--option-border); border-radius: 8px; padding: 12px; margin-top: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.01); }}
        .option-name {{ font-weight: 700; font-size: 0.95rem; color: #111; margin-bottom: 6px; border-bottom: 1px solid #e1f4e8; padding-bottom: 4px; }}
        .option-info-list {{ margin: 5px 0 10px 0; padding-left: 16px; font-size: 0.85rem; color: #555; line-height: 1.5; }}
        .option-info-list li {{ margin-bottom: 4px; }}
        .btn-group {{ display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }}
        .action-btn {{ display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: bold; text-decoration: none; }}
        .btn-map {{ background-color: #e2eafc; color: #1d3557; }}
        .btn-ticket {{ background-color: #ffe3a8; color: #d90429; border: 1px solid #ffe3a8; }}
        .back-to-top {{ position: fixed; bottom: 20px; right: 20px; background: var(--primary-color); color: white; width: 44px; height: 44px; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2); text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <h1>🍏 2026 青森初夏新綠之旅</h1>
        <p>2026/06/09 - 06/13 ｜ 五天四夜家族自駕多餐飲方案版</p>
        <div class="weather-tip-box">
            <b>🌤️ 6月中旬 ｜ 點餐與自駕提示：</b>
            <ul>
                <li>💡 每日用餐時段內嵌<b>多間備選餐廳選項</b>，含招牌必點與預約攻略，可看當天心情一鍵導航！</li>
                <li>⛰️ 山區（奧入瀨、八甲田）體感偏冷，請為長輩隨身攜帶外套、好走路的防滑球鞋。</li>
            </ul>
        </div>
    </header>

    <div class="day-scroller" id="dayScroller">
        {navigation_badges}
    </div>

    <div class="container">
        {main_content}
    </div>

    <a href="#" class="back-to-top">▲</a>

    <script>
        const badges = document.querySelectorAll('.day-badge');
        const scroller = document.getElementById('dayScroller');
        const cards = document.querySelectorAll('.day-card');
        let isClickScrolling = false;
        let clickTimeout;

        function centerBadge(activeBadge) {{
            const badgeOffset = activeBadge.offsetLeft;
            const badgeWidth = activeBadge.offsetWidth;
            const scrollerWidth = scroller.offsetWidth;
            scroller.scrollTo({{ left: badgeOffset - (scrollerWidth / 2) + (badgeWidth / 2), behavior: 'smooth' }});
        }}

        badges.forEach(badge => {{
            badge.addEventListener('click', function(e) {{
                isClickScrolling = true;
                clearTimeout(clickTimeout);
                badges.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                centerBadge(this);
                clickTimeout = setTimeout(() => {{ isClickScrolling = false; }}, 800); 
            }});
        }});

        const observerOptions = {{ root: null, rootMargin: '-20% 0px -60% 0px', threshold: 0 }};
        const observer = new IntersectionObserver((entries) => {{
            if (isClickScrolling) return;
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const currentId = entry.target.getAttribute('id');
                    const targetBadge = document.querySelector(`.day-badge[href="#${{currentId}}"]`);
                    if (targetBadge) {{
                        badges.forEach(b => b.classList.remove('active'));
                        targetBadge.classList.add('active');
                        centerBadge(targetBadge);
                    }}
                }}
            }});
        }}, observerOptions);

        cards.forEach(card => observer.observe(card));
        if(badges.length > 0) {{ badges[0].classList.add('active'); }}
    </script>
</body>
</html>
"""

# 3. 解析與組裝邏輯
def generate_aomori_html(data):
    navigation_badges = ""
    main_content = ""
    
    # 建立天數導航
    for country, days in data.items():
        for d in days:
            day_id = d['day']
            date_raw = d['date']
            try:
                parts = date_raw.split('/')
                short_date = f"{int(parts[1])}/{int(parts[2])}"
            except:
                short_date = date_raw
            navigation_badges += f'<a href="#{day_id}" class="day-badge">{day_id} ({short_date})</a>\n'

    # 建立主行程
    for country, days in data.items():
        main_content += f'<div class="country-section">\n<h2 class="country-header">{country}</h2>\n'
        for d in days:
            # 💡 關鍵修正：將原本錯誤的 id="{day_id}" 改為正確的 id="{d['day']}"
            main_content += f'  <div class="day-card" id="{d["day"]}">\n'
            main_content += f'    <div class="day-card-header">\n'
            main_content += f'      <span class="day-tag">{d["day"]}</span>\n'
            main_content += f'      <span class="day-date">{d["date"]}</span>\n'
            main_content += f'    </div>\n'
            main_content += f'    <div class="day-title">{d["title"]}</div>\n'
            
            # ====== 🌤️ 自動注入每日天氣與降雨率資訊 ======
            if d.get("weather") or d.get("rain_prob"):
                weather_str = d.get("weather", "未知")
                rain_str = d.get("rain_prob", "--%")
                tip_str = d.get("weather_tip", "無特別提醒。")
                
                main_content += f'    <div class="weather-info-box">\n'
                main_content += f'      <div class="weather-info-title">📊 今日氣象預報：<span style="color: #007bff;">{weather_str}</span> ｜ 降雨機率：<span style="color: #dc3545;">{rain_str}</span></div>\n'
                main_content += f'      <p class="weather-info-tip">🧣 <b>自駕與穿搭提醒</b>：{tip_str}</p>\n'
                main_content += f'    </div>\n'
            # ===================================================
            
            for item in d["items"]:
                main_content += f'    <div class="item-block">\n'
                main_content += f'      <span class="time-tag">⏱ {item["time"]}</span>\n'
                main_content += f'      <div class="item-title">{item["title"]}</div>\n'
                
                if item.get("image"):
                    main_content += f'      <img class="item-img" src="{item["image"]}" alt="{item["title"]}" loading="lazy">\n'
                
                if item.get("details"):
                    main_content += f'      <ul class="item-details">\n'
                    for detail in item["details"]:
                        main_content += f'        <li>{detail}</li>\n'
                    main_content += f'      </ul>\n'
                
                if item.get("options"):
                    for opt in item["options"]:
                        main_content += f'      <div class="food-option-card">\n'
                        main_content += f'        <div class="option-name">{opt["name"]}</div>\n'
                        
                        if opt.get("infos"):
                            main_content += f'        <ul class="option-info-list">\n'
                            for info in opt["infos"]:
                                main_content += f'          <li>{info}</li>\n'
                            main_content += f'        </ul>\n'
                            
                        main_content += f'        <div class="btn-group">\n'
                        main_content += f'          <a class="action-btn btn-map" href="{opt["map_url"]}" target="_blank">📍 餐廳地圖導航</a>\n'
                        if opt.get("tabelog_url"):
                            main_content += f'          <a class="action-btn btn-ticket" href="{opt["tabelog_url"]}" target="_blank">🎫 Tabelog 連結</a>\n'
                        main_content += f'        </div>\n'
                        main_content += f'      </div>\n'
                
                if not item.get("options"):
                    main_content += f'      <div class="btn-group">\n'
                    encoded_loc = item["map_loc"].replace(" ", "+")
                    map_url = f"https://www.google.com/maps/search/?api=1&query={encoded_loc}"
                    main_content += f'        <a class="action-btn btn-map" href="{map_url}" target="_blank">📍 地圖導航</a>\n'
                    if item.get("ticket_url"):
                        main_content += f'        <a class="action-btn btn-ticket" href="{item["ticket_url"]}" target="_blank">🔗 相關資訊</a>\n'
                    main_content += f'      </div>\n' 
                    
                main_content += f'    </div>\n'     
            main_content += f'  </div>\n' 
        main_content += f'</div>\n'     

    # 格式化輸出
    final_html = html_template.format(navigation_badges=navigation_badges, main_content=main_content)
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"🎉 網頁已透過 YAML 資料重新編譯完成！\n👉 檔案路徑：{os.path.abspath(OUTPUT_HTML)}")

if __name__ == "__main__":
    generate_aomori_html(aomori_data)
