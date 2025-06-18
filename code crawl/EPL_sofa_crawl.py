import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 🟢 **Khởi tạo trình duyệt Selenium**
driver = webdriver.Chrome()
url = "https://www.sofascore.com/tournament/football/england/premier-league/17#id:61627"
driver.get(url)

# Đợi trang tải hoàn toàn
time.sleep(5)

# ✅ **Chọn mùa giải**
try:
    season_dropdown_xpath = '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/button'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, season_dropdown_xpath))).click()
    time.sleep(2)

    season_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/ul/li'))
    )

    seasons = [season.text for season in season_elements if season.text.strip() != ""]
    print("📜 Danh sách mùa giải:", seasons)
except:
    print("⚠️ Không thể lấy danh sách mùa giải!")
    driver.quit()
    exit()

# 🟢 **Duyệt từng mùa giải để crawl**
all_players_data = []

for i in range(len(seasons)):
    try:
        # Mở lại dropdown
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, season_dropdown_xpath))).click()
        time.sleep(2)

        # Chọn mùa giải
        season_xpath = f'//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/ul/li[{i+1}]'
        season_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, season_xpath))
        )
        season_element.click()
        season_name = seasons[i]
        print(f"✅ Đã chọn mùa giải: {season_name}")
        time.sleep(3)
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000);")  # Cuộn 100px mỗi lần
            time.sleep(1)  # Chờ dữ liệu tải thêm

        # ✅ **Chờ bảng dữ liệu xuất hiện**
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sc-67e6dd27-8"))
            )
            print("✅ Bảng dữ liệu đã sẵn sàng!")
        except:
            print("🚨 Không tìm thấy bảng dữ liệu!")
            continue

        time.sleep(3)

        players_data = []
        page = 1

        while True:
            print(f"📄 Đang lấy dữ liệu mùa {season_name} - trang {page}...")

            # Lấy HTML trang hiện tại
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find("table", class_="sc-67e6dd27-8 bctIbM")

# Nếu có bảng thì mới lấy cột tiêu đề
            if table:
                header_row = table.find("tr")
                headers = [col.text.strip() for col in header_row.find_all("th")]
                # print("📌 Tiêu đề cột thực tế:", headers)

    # 🟢 Xác định vị trí các cột cần lấy
            col_indexes = {
                "team": headers.index("Team") if "Team" in headers else None,
                "name": headers.index("Name") if "Name" in headers else None,
                "goals": headers.index("Goals") if "Goals" in headers else None,
                "succ_dribbles": headers.index("Succ. dribbles") if "Succ. dribbles" in headers else None,
                "tackles": headers.index("Tackles") if "Tackles" in headers else None,
                "assists": headers.index("Assists") if "Assists" in headers else None,
                "accurate_passes": headers.index("Accurate passes %") if "Accurate passes %" in headers else None,
                "sofa_score": headers.index("Average Sofascore Rating") if "Average Sofascore Rating" in headers else None
        }


            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                
                # 🟢 Lấy tên đội từ ảnh logo
                team_element = cols[col_indexes["team"]].find("img") if col_indexes["team"] is not None else None
                team_name = team_element["alt"].strip() if team_element and "alt" in team_element.attrs else "Không rõ"

                name = cols[col_indexes["name"]].text.strip() if col_indexes["name"] is not None else "Không rõ"
                goals = cols[col_indexes["goals"]].text.strip() if col_indexes["goals"] is not None else "0"
                succ_dribbles = cols[col_indexes["succ_dribbles"]].text.strip() if col_indexes["succ_dribbles"] is not None else "0"
                tackles = cols[col_indexes["tackles"]].text.strip() if col_indexes["tackles"] is not None else "0"
                assists = cols[col_indexes["assists"]].text.strip() if col_indexes["assists"] is not None else "0"
                accurate_passes = cols[col_indexes["accurate_passes"]].text.strip() if col_indexes["accurate_passes"] is not None else "0"
                sofa_score = cols[col_indexes["sofa_score"]].text.strip() if col_indexes["sofa_score"] is not None else "N/A"
    
                players_data.append((season_name, team_name, name, goals, succ_dribbles, tackles, assists, accurate_passes, sofa_score))

            # ✅ **Tìm và click nút "Next" để chuyển trang**
            try:
                next_button_xpath = '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[4]/div/div/button[2]'
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                )
                if "disabled" in next_button.get_attribute("class"):
                    print("🚫 Nút 'Next' bị vô hiệu hóa. Kết thúc mùa!")
                    break

                print(f"➡️ Đang chuyển sang trang {page + 1}...")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)
                page += 1
            except:
                print("🚫 Không tìm thấy hoặc không thể nhấn nút tiếp tục. Kết thúc mùa!")
                break
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        all_players_data.extend(players_data)

    except Exception as e:
        print(f"⚠️ Lỗi khi crawl mùa {seasons[i]}: {e}")
        continue

# ✅ **Đóng trình duyệt**
driver.quit()

# ✅ **Lưu vào DataFrame**
df = pd.DataFrame(all_players_data, columns=[
    'Mùa giải', 'Tên đội', 'Tên cầu thủ', 'Số bàn thắng', 'Số pha rê bóng thành công', 
    'Số pha tắc bóng', 'Số pha kiến tạo', 'Tỉ lệ chuyền chính xác', 'Điểm TB (SofaScore)'
])

# ✅ **Xuất file CSV**
df.to_csv("121233all_premier_league.csv", index=False, encoding='utf-8-sig')
print("✅ Dữ liệu đã được lưu vào sofascore_premier_league.csv! 🎉")