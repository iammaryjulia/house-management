"""
巨鴻地產房源管理平台 - 後端API
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import hashlib
import json

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'juhong-2024-secret-key')

# 數據存儲（演示版本使用JSON，生產環境改為PostgreSQL/Supabase）
PROPERTIES_FILE = 'data/properties.json'
USERS_FILE = 'data/users.json'
REVIEWS_FILE = 'data/reviews.json'

# 確保data目錄存在
os.makedirs('data', exist_ok=True)

def load_json(filepath, default=None):
    """載入JSON文件"""
    if default is None:
        default = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except:
        return default

def save_json(filepath, data):
    """保存JSON文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_password(password):
    """密碼雜湊"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """登入檢查裝飾器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== 公開API ====================

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """獲取房屋列表（支持篩選）"""
    properties = load_json(PROPERTIES_FILE, [])
    
    # 篩選條件
    area = request.args.get('area', '')  # 桃園、新竹、苗栗
    type_prop = request.args.get('type', '')  # 買、租
    min_price = request.args.get('min_price', 0, type=int)
    max_price = request.args.get('max_price', 999999999, type=int)
    keywords = request.args.get('keywords', '')
    
    results = []
    for prop in properties:
        if not prop.get('published'):
            continue
        
        if area and prop.get('area') != area:
            continue
        if type_prop and prop.get('type') != type_prop:
            continue
        if prop.get('price', 0) < min_price or prop.get('price', 0) > max_price:
            continue
        if keywords:
            search_text = f"{prop.get('title', '')} {prop.get('description', '')} {prop.get('district', '')}".lower()
            if keywords.lower() not in search_text:
                continue
        
        results.append(prop)
    
    return jsonify(results)

@app.route('/api/properties/<prop_id>', methods=['GET'])
def get_property(prop_id):
    """獲取單個房屋詳情"""
    properties = load_json(PROPERTIES_FILE, [])
    for prop in properties:
        if prop.get('id') == prop_id:
            return jsonify(prop)
    return jsonify({'error': '房屋未找到'}), 404

@app.route('/api/properties/<prop_id>/reviews', methods=['GET'])
def get_property_reviews(prop_id):
    """獲取房屋評論"""
    reviews = load_json(REVIEWS_FILE, [])
    prop_reviews = [r for r in reviews if r.get('property_id') == prop_id and r.get('approved')]
    return jsonify(sorted(prop_reviews, key=lambda x: x.get('created_at', ''), reverse=True))

@app.route('/api/properties/<prop_id>/reviews', methods=['POST'])
def create_review(prop_id):
    """提交評論"""
    data = request.json
    if not data.get('author') or not data.get('content'):
        return jsonify({'error': '缺少必要字段'}), 400
    
    reviews = load_json(REVIEWS_FILE, [])
    review = {
        'id': str(len(reviews) + 1),
        'property_id': prop_id,
        'author': data.get('author'),
        'email': data.get('email', ''),
        'rating': data.get('rating', 5),
        'content': data.get('content'),
        'created_at': datetime.now().isoformat(),
        'approved': False  # 需要管理員審核
    }
    reviews.append(review)
    save_json(REVIEWS_FILE, reviews)
    
    return jsonify({'message': '評論已提交，等待審核'}), 201

@app.route('/api/areas', methods=['GET'])
def get_areas():
    """獲取區域列表"""
    return jsonify({
        'areas': ['桃園', '新竹', '苗栗'],
        'types': ['買', '租']
    })

# ==================== 管理員相關 ====================

@app.route('/admin/login', methods=['GET'])
def admin_login():
    """管理員登入頁面"""
    return render_template('admin_login.html')

@app.route('/admin/api/login', methods=['POST'])
def admin_login_post():
    """管理員登入API"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 簡單驗證（生產環境應使用真實用戶系統）
    if username == 'admin' and password == 'admin123':
        session['user_id'] = 'admin'
        session['username'] = username
        return jsonify({'success': True, 'redirect': '/admin/dashboard'})
    
    return jsonify({'error': '用戶名或密碼錯誤'}), 401

@app.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    """管理後台儀表板"""
    return render_template('admin_dashboard.html')

@app.route('/admin/api/properties', methods=['GET', 'POST'])
@login_required
def admin_properties():
    """管理員獲取/創建房屋"""
    if request.method == 'GET':
        properties = load_json(PROPERTIES_FILE, [])
        return jsonify(properties)
    
    # POST - 創建新房屋
    data = request.json
    properties = load_json(PROPERTIES_FILE, [])
    
    new_property = {
        'id': str(len(properties) + 1),
        'title': data.get('title'),
        'area': data.get('area'),
        'district': data.get('district'),
        'type': data.get('type'),  # 買/租
        'price': data.get('price'),
        'bedrooms': data.get('bedrooms'),
        'bathrooms': data.get('bathrooms'),
        'size': data.get('size'),  # 坪數
        'description': data.get('description'),
        'images': data.get('images', []),
        'contact': data.get('contact'),
        'phone': data.get('phone'),
        'published': False,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    properties.append(new_property)
    save_json(PROPERTIES_FILE, properties)
    
    return jsonify(new_property), 201

@app.route('/admin/api/properties/<prop_id>', methods=['PUT', 'DELETE'])
@login_required
def admin_property_detail(prop_id):
    """管理員編輯/刪除房屋"""
    properties = load_json(PROPERTIES_FILE, [])
    
    for i, prop in enumerate(properties):
        if prop.get('id') == prop_id:
            if request.method == 'PUT':
                data = request.json
                prop.update(data)
                prop['updated_at'] = datetime.now().isoformat()
                save_json(PROPERTIES_FILE, properties)
                return jsonify(prop)
            
            elif request.method == 'DELETE':
                properties.pop(i)
                save_json(PROPERTIES_FILE, properties)
                return jsonify({'message': '已刪除'})
    
    return jsonify({'error': '房屋未找到'}), 404

@app.route('/admin/api/reviews', methods=['GET'])
@login_required
def admin_reviews():
    """管理員獲取待審核評論"""
    reviews = load_json(REVIEWS_FILE, [])
    pending = [r for r in reviews if not r.get('approved')]
    return jsonify(pending)

@app.route('/admin/api/reviews/<review_id>/approve', methods=['POST'])
@login_required
def approve_review(review_id):
    """批准評論"""
    reviews = load_json(REVIEWS_FILE, [])
    for review in reviews:
        if review.get('id') == review_id:
            review['approved'] = True
            save_json(REVIEWS_FILE, reviews)
            return jsonify({'message': '評論已批准'})
    return jsonify({'error': '評論未找到'}), 404

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    """管理員登出"""
    session.clear()
    return redirect('/')

# ==================== 首頁和靜態頁面 ====================

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/properties')
def properties_page():
    """房屋列表頁面"""
    return render_template('properties.html')

@app.route('/properties/<prop_id>')
def property_detail_page(prop_id):
    """房屋詳情頁面"""
    return render_template('property_detail.html', property_id=prop_id)

# ==================== 錯誤處理 ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': '頁面未找到'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': '伺服器錯誤'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
