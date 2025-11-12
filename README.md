# ✈️ Ứng dụng Lập kế hoạch Du lịch AI (Streamlit + Ollama)

Ứng dụng này là một công cụ lập kế hoạch du lịch sử dụng giao diện Streamlit (Frontend) để thu thập sở thích của người dùng và Mô hình Ngôn ngữ Lớn (LLM) từ máy chủ Ollama (Backend) để tạo ra lịch trình chi tiết theo từng ngày.

## 1. Kiến trúc và Phụ thuộc

| Thành phần | Công nghệ | Mục đích |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Thu thập đầu vào, hiển thị lịch trình, Đăng nhập/Lịch sử. |
| **Backend** | Ollama + Llama 2/Mistral | Máy chủ suy luận LLM. |
| **Kết nối** | API HTTP/HTTPS | Giao tiếp giữa Streamlit và Ollama. |

### Yêu cầu Cục bộ
* **Python:** 3.8+
* **Thư viện:** Cài đặt các gói trong `requirements.txt` (`streamlit`, `requests`, `fpdf2`, v.v.).
* **Phần cứng:** Khuyến nghị có **GPU NVIDIA (ví dụ: RTX 3050)** để chạy Ollama với tốc độ cao.

## 2. Hướng dẫn Vận hành (Hai Chế độ)

### Chế độ A: Phát triển Cục bộ (Sử dụng GPU Laptop)

Đây là chế độ nhanh và ổn định nhất để phát triển và gỡ lỗi.

1.  **Thiết lập Ollama:** Đảm bảo bạn đã cài đặt Ollama và CUDA, sau đó chạy máy chủ Ollama và kéo mô hình:
    ```bash
    ollama serve
    # Trong Terminal khác:
    ollama pull llama2
    ```
2.  **Cập nhật URL Cục bộ:** Đảm bảo `app.py` trỏ đến `localhost`:
    ```python
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    ```
3.  **Khởi chạy Streamlit:**
    ```bash
    streamlit run app.py
    ```

---

### Chế độ B: Triển khai Đám mây và Nộp bài (Sử dụng Colab)

Chế độ này đảm bảo ứng dụng đã triển khai công khai hoạt động.

1.  **Chạy Notebook Colab:** Mở Notebook Colab và chạy các lệnh sau trong các ô code riêng biệt để cài đặt, khởi động và phơi bày API một cách ổn định:

    ```bash
    # (1) Khởi động Ollama ổn định (giải quyết lỗi PATH và 403 Forbidden)
    !curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
    import os
    os.environ['PATH'] += ':/usr/local/bin'
    !OLLAMA_HOST=0.0.0.0 nohup ollama serve &
    
    # (2) Tải mô hình
    !ollama pull llama2
    
    # (3) Lấy URL Công khai MỚI
    !npm install -g localtunnel
    !lt --port 11434
    ```

2.  **Cập nhật URL Đám mây:** Sao chép **URL công khai mới** từ Colab (ví dụ: `https://[dãy-ký-tự].loca.lt`) và cập nhật `OLLAMA_API_URL` trong `app.py`.
3.  **Đẩy và Redeploy:** Commit thay đổi và triển khai lại ứng dụng Streamlit Cloud.

## 3. Thông tin Đăng nhập Thử nghiệm

Ứng dụng yêu cầu đăng nhập mô phỏng:

* **Tên đăng nhập:** `user`
* **Mật khẩu:** `pass`
