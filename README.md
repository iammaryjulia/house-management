# 🏠 巨鴻地產房源管理平台

一個完整的房屋買賣及租賃管理系統，專注於桃竹苗地區。

## ✨ 功能特性

### 公開網站

- 🏠 **房屋列表展示** - 響應式設計，支持各種設備
- 🔍 **多條件搜索** - 按地區、房型、價格等篩選
- 📋 **房屋詳情頁** - 完整的房屋信息展示
- ⭐ **用戶評論** - 用戶可以發表評論和評分
- 📱 **移動端優化** - 完全響應式設計

### 管理後台

- 🏢 **房源管理** - 發布、編輯、刪除房源
- 📊 **儀表板** - 實時統計和數據展示
- ⭐ **評論審核** - 管理員審核用戶評論
- 🔐 **帳號管理** - 安全的登入系統
- ⚙️ **設置管理** - 公司信息配置

## 🚀 快速開始

### 環境需求

- Python 3.7+
- pip (Python 包管理器)
- 任何現代的網頁瀏覽器

### 安裝步驟

1. **克隆或下載專案**

```bash
cd house-management
```

2. **創建虛擬環境（推薦）**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **安裝依賴**

```bash
pip install -r requirements.txt
```

4. **設定環境變數**

```bash
# 複製範本
cp .env.example .env

# 編輯 .env 文件（如需自訂）
```

5. **運行應用**

```bash
python backend.py
```

6. **打開瀏覽器訪問**

```
http://localhost:5000
```

## 📝 使用指南

### 用戶側（公開網站）

#### 首頁

- 點擊導航菜單瀏覽功能
- 使用搜索欄快速查找房屋

#### 房源查詢

- 按地區篩選：桃園、新竹、苗栗
- 按房型篩選：買、租
- 按價格範圍篩選
- 輸入關鍵字搜索

#### 房屋詳情

- 查看完整房屋信息
- 查看用戶評論
- 提交新評論（需審核）
- 聯絡業務人員

### 管理員側（後台管理）

#### 登入

- 網址：`http://localhost:5000/admin/login`
- 演示帳號：
  - 用戶名：`admin`
  - 密碼：`admin123`

#### 儀表板

- 查看實時統計數據
- 快速訪問最近發布的房源

#### 房源管理

- **發布房源**
  - 填寫房屋基本信息
  - 上傳房屋圖片URL
  - 設定聯絡方式
  - 勾選「發布」即可上線

- **編輯房源**
  - 修改房屋信息
  - 更新圖片和描述
  - 調整發布狀態

- **刪除房源**
  - 確認後即可刪除

#### 評論管理

- 查看待審核評論
- 批准或拒絕評論
- 批准的評論將顯示在房屋詳情頁

## 📁 專案結構

```
house-management/
├── backend.py                 # Flask應用主文件
├── requirements.txt          # Python依賴
├── .env.example             # 環境變數範本
├── README.md                # 本文件
│
├── templates/               # HTML模板
│   ├── index.html          # 首頁
│   ├── properties.html     # 房屋列表
│   ├── property_detail.html # 房屋詳情
│   ├── admin_login.html    # 管理員登入
│   └── admin_dashboard.html # 管理後台
│
├── data/                    # 數據文件（演示版本使用JSON）
│   ├── properties.json     # 房屋數據
│   ├── reviews.json        # 評論數據
│   └── users.json          # 用戶數據
│
└── static/                 # 靜態資源（CSS、JS、圖片）
    ├── css/
    ├── js/
    └── images/
```

## 🔧 配置說明

### 後端配置（backend.py）

主要配置項：

- `PROPERTIES_FILE` - 房屋數據存儲位置
- `USERS_FILE` - 用戶數據存儲位置
- `REVIEWS_FILE` - 評論數據存儲位置

### 前端配置

所有前端文件都在 `templates/` 目錄中，無需額外配置。

## 🌐 API 端點

### 公開 API

```
GET  /api/properties           # 獲取房屋列表（支持篩選）
GET  /api/properties/<id>      # 獲取單個房屋詳情
GET  /api/properties/<id>/reviews # 獲取房屋評論
POST /api/properties/<id>/reviews # 提交新評論
GET  /api/areas                # 獲取地區和房型列表
```

### 管理員 API

```
GET  /admin/api/properties           # 獲取所有房屋
POST /admin/api/properties           # 創建新房屋
PUT  /admin/api/properties/<id>      # 更新房屋
DELETE /admin/api/properties/<id>    # 刪除房屋
GET  /admin/api/reviews              # 獲取待審核評論
POST /admin/api/reviews/<id>/approve # 批准評論
```

## 🎨 自訂外觀

### 修改公司信息

1. **公司名稱和logo**
   - 編輯 `templates/index.html` 中的 `<title>` 和 logo 元素

2. **公司聯絡方式**
   - 在各頁面中搜索 `巨鴻地產` 和 `(03) 1234-5678` 進行替換

3. **顏色主題**
   - 搜索並替換 `#667eea` （主色）和 `#764ba2` （副色）

### 修改搜索選項

編輯 `templates/properties.html` 中的地區和房型選項：

```html
<select id="area">
  <option value="">所有地區</option>
  <option value="桃園">桃園</option>
  <option value="新竹">新竹</option>
  <option value="苗栗">苗栗</option>
</select>
```

## 📱 部署到生產環境

### 使用 Gunicorn 部署

```bash
# 安裝 Gunicorn（requirements.txt 已包含）
pip install gunicorn

# 運行應用
gunicorn -w 4 -b 0.0.0.0:5000 backend:app
```

### 使用 Heroku 部署

1. 創建 `Procfile` 文件：

```
web: gunicorn backend:app
```

2. 部署：

```bash
heroku create juhong-realestate
git push heroku main
```

### 使用 Docker 部署

1. 創建 `Dockerfile`：

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend:app"]
```

2. 構建並運行：

```bash
docker build -t juhong-realestate .
docker run -p 5000:5000 juhong-realestate
```

## 🗄️ 升級到數據庫

目前使用 JSON 文件存儲數據。要升級到 PostgreSQL：

1. 安裝 PostgreSQL
2. 修改 `backend.py` 使用 SQLAlchemy
3. 創建數據庫模型
4. 遷移數據

詳見文件末尾的「高級配置」部分。

## 🐛 故障排除

### 問題：無法連接到 localhost:5000

**解決方案：**

- 確保 Python 應用正在運行
- 檢查防火牆設置
- 嘗試更換端口：編輯 `backend.py` 最後一行

### 問題：頁面無法加載

**解決方案：**

- 打開瀏覽器開發者工具（F12）檢查錯誤
- 清除瀏覽器緩存
- 重新啟動應用

### 問題：無法登入管理後台

**解決方案：**

- 確保使用正確的帳號密碼（admin/admin123）
- 檢查 `.env` 文件配置
- 查看瀏覽器控制台是否有錯誤

## 📚 高級功能

### 計劃中的功能

- [ ] 數據庫集成（PostgreSQL/Supabase）
- [ ] 圖片上傳功能
- [ ] Google Maps 集成
- [ ] 虛擬看房 (VR)
- [ ] 推薦系統
- [ ] 用戶帳號系統
- [ ] 電子郵件通知
- [ ] 分析和報表

### 數據庫遷移指南

計劃將 JSON 數據轉換為 PostgreSQL：

```python
# 安裝依賴
pip install sqlalchemy psycopg2-binary

# 創建數據庫連接
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:password@localhost/juhong_db')

# 創建模型並遷移數據
# 詳見 docs/database-migration.md
```

## 📞 支持和反饋

有問題或建議？請聯絡：

- 電話：(03) 1234-5678
- 郵件：info@juhong.com.tw

## 📄 許可證

本項目僅供巨鴻地產有限公司使用。

## 🎯 開發者指南

### 添加新的搜索過濾

1. 編輯 `templates/properties.html` 添加新的篩選控件
2. 編輯 `backend.py` 的 `get_properties()` 函數添加新的篩選邏輯
3. 測試篩選功能

### 自訂管理員介面

所有管理員頁面的代碼都在 `templates/admin_dashboard.html`，包含了 HTML、CSS 和 JavaScript。

### 數據驗證

所有表單提交都應進行客戶端和服務器端驗證。

---

**最後更新：2024年8月17日**

版本：1.0.0 - Beta

**下一步：**

1. 自訂公司信息和配置
2. 添加房源數據
3. 測試各項功能
4. 根據需要進行自訂
5. 部署到生產環境
