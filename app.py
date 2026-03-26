import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="房源管理平台", layout="wide")
st.title("🏠 個人地產房源共享平台")
st.markdown("你們 5 個人共同使用的房源管理後台")

# === Supabase 連線 ===
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"] if "SUPABASE_URL" in st.secrets else os.getenv("SUPABASE_URL")
    key = st.secrets["SUPABASE_KEY"] if "SUPABASE_KEY" in st.secrets else os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("請設定 Supabase URL 和 Key")
        st.stop()
    return create_client(url, key)

supabase = get_supabase()

# 顯示所有房源
st.header("📋 所有房源（大家都能看到）")
response = supabase.table("properties").select("*").execute()
properties = response.data

if properties:
    for prop in properties:
        with st.expander(f"🏠 {prop.get('title', '無標題')} - NT${prop.get('price', 0):, }"):
            st.write(f"**地址**：{prop.get('address', '未填寫')}")
            st.write(f"**描述**：{prop.get('description', '')}")
            if prop.get('images'):
                cols = st.columns(3)
                for i, img_url in enumerate(prop['images'][:6]):  # 最多顯示6張
                    with cols[i % 3]:
                        st.image(img_url, use_column_width=True)
else:
    st.info("目前還沒有房源資料，請先新增。")

# 新增房源表單
st.header("➕ 新增房源")
with st.form("new_property_form", clear_on_submit=True):
    title = st.text_input("房源標題 *")
    price = st.number_input("價格 (台幣)", min_value=0, step=10000)
    address = st.text_input("地址")
    description = st.text_area("房屋描述")
    uploaded_files = st.file_uploader("上傳照片（可多選）", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    
    submitted = st.form_submit_button("新增房源")
    if submitted:
        if not title:
            st.error("請填寫房源標題")
        else:
            # 先插入文字資料
            data = {
                "title": title,
                "price": price,
                "address": address,
                "description": description
            }
            result = supabase.table("properties").insert(data).execute()
            
            if result.data:
                prop_id = result.data[0]["id"]
                image_urls = []
                
                # 上傳圖片
                if uploaded_files:
                    for file in uploaded_files:
                        file_bytes = file.getvalue()
                        file_path = f"properties/{prop_id}/{file.name}"
                        try:
                            supabase.storage.from_("properties").upload(file_path, file_bytes)
                            public_url = supabase.storage.from_("properties").get_public_url(file_path)
                            image_urls.append(public_url)
                        except Exception as e:
                            st.warning(f"圖片 {file.name} 上傳失敗: {e}")
                
                # 更新圖片網址到資料
                if image_urls:
                    supabase.table("properties").update({"images": image_urls}).eq("id", prop_id).execute()
                
                st.success("✅ 房源新增成功！")
                st.rerun()