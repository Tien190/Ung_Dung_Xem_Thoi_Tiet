Cách chạy nhanh để test

Chạy backend:
Cài thư viện: pip install -r backend/requirements.txt
Chạy: uvicorn backend.main:app --reload
Mặc định sẽ ở http://localhost:8000
Chạy web-ui tĩnh:
Vào thư mục web-ui: cd web-ui
Chạy server tĩnh, ví dụ:
Python: python -m http.server 5500
hoặc Node: npx serve .
Mở http://localhost:5500/public/index.html
Điền “Backend URL” là http://localhost:8000 rồi bấm “Dùng URL này”
Dán một vài URL và bấm “Bắt đầu tải tất cả”
Quan sát bảng “Tasks” và dùng nút Pause/Resume/Stop