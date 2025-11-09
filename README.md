# travel_planner
# ✈️ Ứng dụng Lập kế hoạch Du lịch AI (Streamlit + Ollama)

Ứng dụng này cung cấp giao diện người dùng (Frontend) tương tác để người dùng nhập thông tin chuyến đi và sử dụng Mô hình Ngôn ngữ Lớn (LLM) từ Ollama (Backend) để tạo ra lịch trình du lịch chi tiết theo từng ngày.

## 1. Kiến trúc Tổng quan

* **Frontend (FE):** Streamlit (Giao diện người dùng).
* **Backend (BE):** Ollama, chạy trên Google Colab/Kaggle để có thể truy cập công khai.
* **Kết nối:** Giao tiếp qua API HTTP.

## 2. Yêu cầu Tiên quyết (Prerequisites)

* Python 3.8+
* Git
* Tài khoản GitHub
* **Phụ thuộc:** Các gói trong `requirements.txt` (`streamlit`, `requests`).

## 3. Hướng dẫn Thiết lập và Chạy Ứng dụng

### 3.1. Chạy Backend (LLM Server - BẮT BUỘC)

Vì ứng dụng được triển khai trên Cloud (Streamlit Cloud), máy chủ LLM (Ollama) phải chạy trên một địa chỉ công khai.

1.  **Khởi động Colab:** Mở Notebook Colab của dự án này và chạy tất cả các ô lệnh để:
    * Cài đặt và khởi động Ollama (`!OLLAMA_HOST=0.0.0.0 nohup ollama serve &`).
    * Tải mô hình (`!ollama pull llama2`).
    * Tạo URL công khai bằng `localtunnel` (`!lt --port 11434`).
2.  **Sao chép URL:** Sao chép URL công khai mới nhất (ví dụ: `https://[dãy-ký-tự].loca.lt`).
3.  **Cập nhật Mã code:** Đảm bảo biến `OLLAMA_API_URL` trong tệp `app.py` trỏ đến URL công khai đang hoạt động này, kèm theo `/api/generate`.
    
    ```python
    OLLAMA_API_URL = "https://[URL_CÔNG_KHAI_CỦA_BẠN]/api/generate"
    ```
    
    *LƯU Ý: Nếu bạn tắt Notebook Colab, URL sẽ thay đổi và ứng dụng sẽ bị lỗi kết nối.*

### 3.2. Chạy Frontend (Streamlit)

Phiên bản đã triển khai trên Streamlit Cloud có thể được truy cập trực tiếp qua đường link công khai:

* **Link Triển khai:** [Dán link triển khai Streamlit Cloud của bạn vào đây]

#### Thông tin Đăng nhập Thử nghiệm

Ứng dụng yêu cầu đăng nhập:

* **Tên đăng nhập:** `user`
* **Mật khẩu:** `pass`

## 4. Kiểm tra và Gỡ lỗi

* Nếu ứng dụng báo lỗi `403 Forbidden` hoặc `Connection refused`, hãy kiểm tra xem Notebook Colab có đang chạy và đã tạo lại đường hầm `localtunnel` với cấu hình `OLLAMA_HOST=0.0.0.0` chưa.
