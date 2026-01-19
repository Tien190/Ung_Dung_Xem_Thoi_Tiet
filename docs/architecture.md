# Tài liệu Thiết kế Kiến trúc

Tài liệu này ghi lại các quyết định thiết kế và luồng hoạt động của hệ thống.

## 1. Tổng quan

Hệ thống được xây dựng theo mô hình Client-Server.

*   **Server (Backend):** Một ứng dụng Python `asyncio` chạy liên tục, có nhiệm vụ quản lý kết nối từ nhiều client và điều phối dữ liệu.
*   **Client (Frontend):** Một ứng dụng GUI (Tkinter/PyQt) mà người dùng cuối tương tác. Mỗi client sẽ duy trì một kết nối socket liên tục đến server.

## 2. Luồng Giao tiếp (Communication Flow)

Giao tiếp giữa Client và Server sử dụng `socket` dựa trên TCP. Dữ liệu được trao đổi dưới dạng chuỗi JSON để dễ dàng phân tích và mở rộng.

### 2.1. Luồng Lấy Dữ liệu Thời tiết

1.  **Client:** Người dùng nhập tên một thành phố và nhấn "Tìm kiếm".
2.  **Client:** Gửi một message đến Server qua socket.
    *   **Định dạng:** `{"command": "GET_WEATHER", "payload": {"city": "Hanoi"}}`
3.  **Server:** Nhận message, phân tích `command`.
4.  **Server:** Gọi hàm xử lý tương ứng. Hàm này sẽ sử dụng `aiohttp` để thực hiện các yêu cầu **bất đồng bộ song song** đến các API:
    *   API thời tiết (OpenWeatherMap)
    *   API chất lượng không khí (Open-Meteo)
5.  **Server:** Chờ tất cả các API trả về kết quả. Tổng hợp dữ liệu thành một đối tượng JSON duy nhất.
6.  **Server:** Gửi lại kết quả cho client.
    *   **Định dạng (Thành công):** `{"status": "SUCCESS", "command": "WEATHER_DATA", "payload": {"temp": 25, "humidity": 80, "aqi": 150, ...}}`
    *   **Định dạng (Thất bại):** `{"status": "ERROR", "message": "City not found"}`
7.  **Client:** Nhận JSON, phân tích và cập nhật giao diện người dùng.

### 2.2. Luồng Tự động Gợi ý (Autocomplete)

*   Sử dụng một API Geocoding.
*   Client sẽ có logic `debounce` để tránh gửi quá nhiều yêu cầu khi người dùng đang gõ.
*   Luồng này có thể được xử lý hoàn toàn ở phía Client (Client gọi thẳng API Geocoding) để giảm tải cho Server, hoặc thông qua Server nếu muốn giấu API key. **Quyết định ban đầu: Client sẽ tự gọi API.**

## 3. Cấu trúc Dữ liệu (JSON)

Mọi gói tin trao đổi sẽ có cấu trúc cơ bản:
```json
{
  "command": "TÊN_LỆNH",
  "payload": { ... } // Dữ liệu dành riêng cho lệnh đó
}
```

**Ví dụ các lệnh:**
*   `GET_WEATHER`: Client yêu cầu dữ liệu thời tiết.
*   `WEATHER_DATA`: Server trả về dữ liệu thời tiết.
*   `ERROR_MESSAGE`: Server thông báo lỗi.