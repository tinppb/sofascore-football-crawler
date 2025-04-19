# Sofascore Football Crawler

## Giới thiệu
**Sofascore Football Crawler** là một công cụ thu thập dữ liệu bóng đá từ trang [Sofascore](https://www.sofascore.com/). Dự án này giúp bạn lấy thông tin về cầu thủ, đội bóng, và thống kê các chỉ số của cầu thủ một cách tự động.

## Tính năng
- Lấy dữ liệu theo giải đấu (Premier League, UEFA Champions League, La Liga, Serie A,...).
- Trích xuất thông tin chi tiết cầu thủ:
  - Season
  - Team
  - Name
  - Goals
  - Successful dribbles
  - Tackles
  - Assists
  - Accurate passes %
  - Average Sofascore Rating
- Xuất dữ liệu ra file `.csv`.

## Cài đặt

### Yêu cầu hệ thống
- Python 3.x
- Các thư viện cần thiết: `selenium`, `pandas`, `beautifulsoup4`, ...

### Cách cài đặt
1. Clone repo này về máy:
   ```
   git clone https://github.com/BAOTIN2004/sofascore-football-crawler.git ```
2. Di chuyển đến thư mục:
    ```cd "code crawl sofascore"```
3. Chạy chương trình:
    ```python EPL_sofa_crawl.py ```
4. Sau khi chạy thành công, file `.csv` chứa dữ liệu được tạo ra trong thư mục làm việc.

#### Tùy chỉnh cài đặt
Dự án hiện tại hỗ trợ thu thập dữ liệu từ giải Premier League. 
Tuy nhiên, bạn có thể dễ dàng thay đổi giải đấu bằng cách chỉnh sửa mã trong file `EPL_sofa_crawl.py`.
1. Mở file `EPL_sofa_crawl.py` tìm phần mã chứa URL của giải đấu.
2. Thay thế URL đó bằng URL của giải đấu bạn muốn thu thập dữ liệu (ví dụ: La Liga, Serie A,...).
3. Chạy lại script và dữ liệu sẽ được thu thập cho giải đấu mới.

## Đóng góp
Nếu bạn muốn đóng góp cho dự án:
1. Fork repo này.
2. Tạo branch mới:
    ```
    git checkout -b branch-moi ```
3. Commit thay đổi:
    ```
    git commit -m "Mô tả thay đổi" ```
4. Push lên Github:
    ```
    git push origin branch-moi ```
5. Tạo Pull Request để được xem xét và hợp nhất vào nhánh chính.

## Liên hệ
Nếu có bất kỳ câu hỏi nào, hãy liên hệ qua emai hoặc tạo issue trên GitHub.

---
## Người phát triển
**Phạm Phước Bảo Tín (tinppb)**  
📧 Email: [baotinphamphuoc@gmail.com](mailto:baotinphamphuoc@gmail.com)  
