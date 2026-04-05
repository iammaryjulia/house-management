import streamlit as st
from supabase import create_client, Client
import os

st.set_page_config(page_title="房源管理平台", layout="wide")

# Supabase 連線
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("請在 Streamlit Secrets 設定 SUPABASE_URL 和 SUPABASE_KEY")
        st.stop()
    return create_client(url, key)

supabase = get_supabase()

# ====================== 登入系統 ======================
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    with st.form("login_form"):
        st.subheader("🔑 登入房源管理平台")
        email = st.text_input("Email")
        password = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("登入")
        
        if submitted:
            if email and password:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    st.session_state.user = response.user
                    st.success("登入成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"登入失敗：{str(e)}")
            else:
                st.error("請輸入 Email 和密碼")

# ====================== 主程式 ======================
if st.session_state.user is None:
    login()
else:
    st.title("🏠 個人地產房源共享平台")
    st.write(f"歡迎回來，**{st.session_state.user.email}**")
    
    if st.button("登出"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    # 顯示所有房源
    st.header("📋 所有房源（大家都能看到）")
    response = supabase.table("properties").select("*").execute()
    properties = response.data or []

    if properties:
        for prop in properties:
            with st.expander(f"🏠 {prop.get('title', '無標題')} - NT${prop.get('price', 0):,}"):
                st.write(f"**地址**：{prop.get('address', '')}")
                st.write(f"**描述**：{prop.get('description', '')}")
                if prop.get('images'):
                    cols = st.columns(3)
                    for i, url in enumerate(prop['images'][:6]):
                        with cols[i % 3]:
                            st.image(url, use_column_width=True)
    else:
        st.info("目前還沒有房源，請先新增。")

    # 新增房源
    st.header("➕ 新增房源")
    with st.form("new_property", clear_on_submit=True):
        title = st.text_input("房源標題 *")
        price = st.number_input("價格 (台幣)", min_value=0, step=10000)
        address = st.text_input("地址")
        description = st.text_area("房屋描述")
        uploaded_files = st.file_uploader("上傳照片（可多張）", accept_multiple_files=True, type=["jpg","png","jpeg"])
        
        if st.form_submit_button("新增房源"):
            if title:
                data = {
                    "title": title,
                    "price": price,
                    "address": address,
                    "description": description,
                    "owner_id": st.session_state.user.id   # 記錄是誰新增的
                }
                result = supabase.table("properties").insert(data).execute()
                
                if result.data and uploaded_files:
                    prop_id = result.data[0]["id"]
                    image_urls = []
                    for file in uploaded_files:
                        try:
                            file_bytes = file.getvalue()
                            file_path = f"properties/{prop_id}/{file.name}"
                            supabase.storage.from_("properties").upload(file_path, file_bytes)
                            public_url = supabase.storage.from_("properties").get_public_url(file_path)
                            image_urls.append(public_url)
                        except:
                            pass
                    
                    if image_urls:
                        supabase.table("properties").update({"images": image_urls}).eq("id", prop_id).execute()
                
                st.success("房源新增成功！")
                st.rerun()
            else:
                st.error("請填寫房源標題")
