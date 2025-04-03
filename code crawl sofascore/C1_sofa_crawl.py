import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# URL trang web
url = "https://www.sofascore.com/tournament/football/europe/uefa-champions-league/7#id:61644"

# Khởi tạo trình duyệt Selenium
driver = webdriver.Chrome()
driver.get(url)

# Đợi trang tải hoàn toàn
time.sleep(5)

# 🟢 **Lấy danh sách tất cả mùa giải từ dropdown**
try:
    # Mở dropdown
    season_dropdown_xpath = '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/button'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, season_dropdown_xpath))).click()
    time.sleep(2)

    # Lấy danh sách các mùa giải
    season_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/ul/li'))
    )

    seasons = [season.text for season in season_elements if season.text.strip() != ""]
    print("📜 Danh sách mùa giải:", seasons)
except:
    print("⚠️ Không thể lấy danh sách mùa giải!")
    driver.quit()
    exit()

# 🟢 **Duyệt qua từng mùa giải và crawl dữ liệu**
all_players_data = []

for i in range(len(seasons)):
    try:
        # Mở lại dropdown
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, season_dropdown_xpath))).click()
        time.sleep(2)

        # Chọn mùa giải
        season_xpath = f'//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/ul/li[{i+2}]'

        season_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, season_xpath))
        )
        season_element.click()
        season_name = seasons[i]
        print(f"✅ Đã chọn mùa giải: {season_name}")
        time.sleep(5)  # Đợi trang load lại dữ liệu

        # 🟢 **Nhấn "Detailed" nếu có**
        try:
            detailed_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Detailed')]"))
            )
            driver.execute_script("arguments[0].click();", detailed_button)
            print("✅ Đã nhấn nút 'Detailed'")
            time.sleep(3)
        except:
            print("⚠️ Không tìm thấy nút 'Detailed'! Có thể đã mở sẵn.")

        # 🟢 **Nhấn "Apply" nếu có**
        try:
            apply_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply')]"))
            )
            driver.execute_script("arguments[0].click();", apply_button)
            print("✅ Đã nhấn nút 'Apply'")
            time.sleep(5)
        except:
            print("⚠️ Không tìm thấy nút 'Apply'! Có thể không cần thiết.")

        # 🟢 **Chờ bảng dữ liệu xuất hiện**
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sc-67e6dd27-8"))
            )
            print("✅ Bảng dữ liệu đã sẵn sàng!")
        except:
            print("🚨 Không tìm thấy bảng dữ liệu!")
            continue

        time.sleep(3)  # Đợi dữ liệu tải hoàn toàn

        players_data = []
        page = 1  # Đếm số trang

        while True:
            print(f"📄 Đang lấy dữ liệu mùa {season_name} - trang {page}...")

            # Lấy HTML trang hiện tại
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find("table", class_="sc-67e6dd27-8 bctIbM")

            # Trích xuất dữ liệu
            if table:
                rows = table.find_all("tr")[1:]  # Bỏ qua hàng tiêu đề
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 9:
                        team_element = cols[1].find("img")  # Tìm ảnh logo đội
                        if team_element:
                            team_name = team_element.get("alt", "Không rõ").strip()  # Lấy tên từ `alt`
                        else:
                            team_name = "Không rõ"
                        name = cols[2].text.strip()  # Tên cầu thủ
                        goals = cols[3].text.strip()  # Số bàn thắng
                        succ_dribbles = cols[4].text.strip()  # Số pha rê bóng thành công
                        tackles = cols[5].text.strip()  # Số pha tắc bóng
                        assists = cols[6].text.strip()  # Số pha kiến tạo
                        accurate_passes = cols[7].text.strip()  # Tỉ lệ chuyền chính xác
                        sofa_score = cols[8].text.strip()  # Điểm TB (SofaScore)
                        players_data.append((season_name,team_name, name, goals, succ_dribbles, tackles, assists, accurate_passes, sofa_score))

            # 🟢 **Tìm và click nút chuyển trang**
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[8]/div/div/button[2]'))
                )
                if "disabled" in next_button.get_attribute("class"):
                    print("🚫 Nút 'Next' bị vô hiệu hóa. Kết thúc mùa!")
                    break

                print(f"➡️ Đang chuyển sang trang {page + 1}...")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)  # Đợi trang mới tải
                page += 1
            except:
                print("🚫 Không tìm thấy hoặc không thể nhấn nút tiếp tục. Kết thúc mùa!")
                break

        # Lưu dữ liệu mùa giải vào danh sách tổng
        all_players_data.extend(players_data)

    except Exception as e:
        print(f"⚠️ Lỗi khi crawl mùa {seasons[i]}: {e}")
        continue

# Đóng trình duyệt
driver.quit()

# 🟢 **Tạo DataFrame**
df = pd.DataFrame(all_players_data, columns=[
    'Mùa giải','Tên đội', 'Tên cầu thủ', 'Số bàn thắng', 'Số pha rê bóng thành công', 'Số pha tắc bóng',
    'Số pha kiến tạo', 'Tỉ lệ chuyền chính xác', 'Điểm TB (SofaScore)'
])

# 🟢 **Lưu vào file CSV**
df.to_csv("tintinc1sofascore_all_seasons.csv", index=False, encoding='utf-8-sig')
print("✅ Dữ liệu đã được lưu vào file sofascore_all_seasons.csv!")
