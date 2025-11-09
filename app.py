import streamlit as st
import requests
import json
# Thư viện cho mã hóa mật khẩu (nếu triển khai đầy đủ Đăng nhập)
# import bcrypt

# --- Cấu hình Trang và Tiêu đề ---
st.set_page_config(page_title="Đối tác Lên kế hoạch Du lịch AI", layout="wide")
st.title("✈️ Đối tác Lên kế hoạch Du lịch AI")

# --- Trạng thái Phiên (Dùng cho Đăng nhập và Lịch sử) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary_history' not in st.session_state:
    st.session_state.itinerary_history = []

# --- Thông tin cấu hình (Cần thay đổi) ---
OLLAMA_API_URL = "https://fair-rules-drum.loca.lt/api/generate" # Thay thế bằng URL máy chủ Ollama của bạn
LLM_MODEL = "llama2" # Tên mô hình bạn đã cài đặt trên Ollama

# ==========================================================
# 1. Logic ĐĂNG NHẬP (Mô phỏng/Khái niệm)
# *Trong dự án thực tế, bạn cần tích hợp với cơ sở dữ liệu*
# ==========================================================
def login_form():
    """Hiển thị form đăng nhập đơn giản."""
    with st.sidebar:
        st.header("👤 Đăng nhập")
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            # Logic xác thực mô phỏng
            if username == "user" and password == "pass":
                st.session_state.logged_in = True
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")

def logout_button():
    """Nút đăng xuất."""
    with st.sidebar:
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.itinerary_history = []
            st.info("Đã đăng xuất.")
            st.rerun()

# ==========================================================
# 2. Logic TẠO LỊCH TRÌNH
# ==========================================================

def generate_itinerary(prompt):
    """
    Gửi yêu cầu đến máy chủ Ollama để tạo lịch trình.
    
    LƯU Ý: Chức năng này giả định rằng máy chủ Ollama đã được thiết lập 
    và có thể truy cập được từ ứng dụng Streamlit của bạn.
    """
    st.info("Đang tạo lịch trình... Vui lòng chờ vài giây!")
    
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False # Tắt streaming để nhận phản hồi hoàn chỉnh
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status() # Báo lỗi cho các mã trạng thái 4xx/5xx
        
        # Phân tích phản hồi JSON từ Ollama
        data = response.json()
        return data.get("response", "Không nhận được phản hồi từ LLM.")
        
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi kết nối với máy chủ Ollama: {e}")
        st.warning("Vui lòng đảm bảo Ollama đang chạy và URL API đã chính xác.")
        return None

def main_app():
    """Giao diện chính để tạo lịch trình."""
    st.header("🗺️ Nhập thông tin chuyến đi")
    
    # Sử dụng st.container() hoặc st.columns() để sắp xếp đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        origin_city = st.text_input("1. Thành phố Xuất phát (Origin City)", "Hà Nội")
        destination_city = st.text_input("2. Thành phố Đến (Destination City)", "Đà Nẵng")
        start_date = st.date_input("3. Ngày Bắt đầu")
        end_date = st.date_input("4. Ngày Kết thúc")
        
    with col2:
        interests = st.multiselect(
            "5. Sở thích/Hoạt động",
            ['Ẩm thực (Food)', 'Bảo tàng (Museums)', 'Thiên nhiên (Nature)', 'Cuộc sống về đêm (Nightlife)', 'Mua sắm (Shopping)', 'Nghệ thuật (Art)'],
            default=['Ẩm thực (Food)', 'Thiên nhiên (Nature)']
        )
        pace = st.select_slider(
            "6. Tốc độ du lịch",
            options=['Thư giãn (Relaxed)', 'Bình thường (Normal)', 'Chặt chẽ (Tight)'],
            value='Bình thường (Normal)'
        )
        
        # Tính toán số ngày
        num_days = (end_date - start_date).days + 1
        st.markdown(f"**Tổng số ngày:** `{num_days} ngày`")
        
    # Nút Tạo Lịch trình
    if st.button("✨ Tạo Lịch trình", type="primary", use_container_width=True):
        if num_days <= 0:
            st.error("Ngày kết thúc phải sau hoặc cùng ngày bắt đầu.")
        else:
            # Xây dựng Prompt cho LLM
            interests_str = ", ".join(interests)
            prompt_template = f"""
            Bạn là một chuyên gia du lịch. Hãy tạo một lịch trình chi tiết {num_days} ngày cho chuyến đi từ {origin_city} đến {destination_city}.
            - **Thời gian:** Từ {start_date} đến {end_date}.
            - **Sở thích:** {interests_str}.
            - **Tốc độ:** {pace} (thư giãn nghĩa là ít hoạt động hơn, chặt chẽ nghĩa là nhiều hoạt động hơn).

            **Định dạng đầu ra phải là:**

            Ngày X: [Tên Ngày]
            Sáng: [Hoạt động Sáng] (Giải thích ngắn gọn)
            Chiều: [Hoạt động Chiều] (Giải thích ngắn gọn)
            Tối: [Hoạt động Tối] (Giải thích ngắn gọn)

            Lặp lại cho tất cả {num_days} ngày. Đảm bảo phản hồi chỉ chứa lịch trình đã định dạng, không có bất kỳ văn bản giới thiệu hoặc kết thúc nào khác.
            """
            
            # Gọi LLM và hiển thị kết quả
            itinerary_text = generate_itinerary(prompt_template)
            
            if itinerary_text:
                st.subheader("📝 Lịch trình Du lịch của bạn:")
                st.markdown(itinerary_text)
                
                # Lưu vào lịch sử (chỉ khi đăng nhập)
                if st.session_state.logged_in:
                    st.session_state.itinerary_history.append({
                        "input": f"{destination_city} ({num_days} ngày, {pace})",
                        "output": itinerary_text
                    })

# ==========================================================
# 3. Chạy Ứng dụng
# ==========================================================

if not st.session_state.logged_in:
    # Yêu cầu người dùng đăng nhập
    login_form()
    st.info("Vui lòng đăng nhập để tạo lịch trình và xem lịch sử.")
else:
    # Hiển thị UI chính và Lịch sử
    col_main, col_history = st.columns([3, 1])
    
    with col_main:
        main_app()
        
    with col_history:
        st.header("📚 Lịch sử")
        if st.session_state.itinerary_history:
            for i, item in enumerate(reversed(st.session_state.itinerary_history)):
                with st.expander(f"Lịch trình #{len(st.session_state.itinerary_history) - i}: {item['input']}"):
                    st.markdown(item['output'])
        else:
            st.info("Không có lịch sử. Hãy tạo một lịch trình mới!")
        
        logout_button() # Nút đăng xuất