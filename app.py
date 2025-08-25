from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 允许前端访问

# 数据文件路径
DATA_FILE = "data.json"

# 初始化数据
def init_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "likes": 0,
            "coins": 0,
            "favorites": 0,
            "comments": []
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

# 读取数据
def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# 保存数据
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# 获取当前数据
@app.route('/api/data', methods=['GET'])
def get_data():
    data = read_data()
    return jsonify(data)

# 点赞
@app.route('/api/like', methods=['POST'])
def like():
    data = read_data()
    data['likes'] += 1
    save_data(data)
    return jsonify({"success": True, "likes": data['likes']})

# 投币
@app.route('/api/coin', methods=['POST'])
def coin():
    data = read_data()
    data['coins'] += 1
    save_data(data)
    return jsonify({"success": True, "coins": data['coins']})

# 收藏
@app.route('/api/favorite', methods=['POST'])
def favorite():
    data = read_data()
    data['favorites'] += 1
    save_data(data)
    return jsonify({"success": True, "favorites": data['favorites']})

# 添加评论
@app.route('/api/comment', methods=['POST'])
def add_comment():
    data = read_data()
    new_comment = {
        "user": request.json.get('user', '匿名'),
        "content": request.json.get('content', ''),
        "time": request.json.get('time', '刚刚')
    }
    data['comments'].append(new_comment)
    save_data(data)
    return jsonify({"success": True, "comments": data['comments']})

if __name__ == '__main__':
    init_data()
    app.run(debug=True)