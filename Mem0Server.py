from flask import Flask, request, jsonify
from mem0 import Memory
import json
import os

# from dotenv import load_dotenv
#
# # 加载 .env 文件中的环境变量
# load_dotenv()
app = Flask(__name__)

config = {
    "vector_store": {
        "provider": os.environ.get("VECTOR_STORE_PROVIDER", "qdrant"),
        "config": {
            "embedding_model_dims": int(os.environ.get("EMBEDDING_MODEL_DIMS", 768)),
            "host": os.environ.get("VECTOR_STORE_HOST", "localhost"),
            "port": int(os.environ.get("VECTOR_STORE_PORT", 6333))
        }
    },
    "llm": {
        "provider": os.environ.get("LLM_PROVIDER", "openai"),
        "config": {
            **({"ollama_base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")}
               if os.environ.get("LLM_PROVIDER", "openai") == "ollama" else {}),
            "model": os.environ.get("LLM_MODEL", "gpt-4o"),
            "temperature": float(os.environ.get("LLM_TEMPERATURE", 0.2)),
            "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", 1500))
        }
    },
    "embedder": {
        "provider": os.environ.get("EMBEDDER_PROVIDER", "openai"),
        "config": {
            **({"ollama_base_url": os.environ.get("EMBEDDER_OLLAMA_BASE_URL", "http://localhost:11434")}
               if os.environ.get("EMBEDDER_PROVIDER", "openai") == "ollama" else {}),
            "model": os.environ.get("EMBEDDER_MODEL", "text-embedding-3-large"),
            "embedding_dims": int(os.environ.get("EMBEDDER_DIMS", 768))
        }
    }
}

print(json.dumps(config))
m = Memory.from_config(config)

# 存储内存
@app.route('/memory/add', methods=['POST'])
def add_memory():
    data = request.get_json()

    if "metadata" in data:
        result = m.add(data["data"], user_id=data["user_id"], metadata=data["metadata"])
    else:
        result = m.add(data["data"], user_id=data["user_id"])

    return jsonify(result), 201


# 获取所有内存
@app.route('/memory/get_all', methods=['POST'])
def get_all_memories():
    all_memories = m.get_all()
    return jsonify(all_memories), 200

# 获取特定内存
@app.route('/memory/get', methods=['POST'])
def get_memory():
    memory_id = request.get_json().get("memory_id")
    specific_memory = m.get(memory_id)
    return jsonify(specific_memory), 200

# 搜索内存
@app.route('/memory/search', methods=['POST'])
def search_memories():
    data = request.get_json()
    related_memories = m.search(query=data["query"], user_id=data["user_id"])
    return jsonify(related_memories), 200

# 更新内存
@app.route('/memory/update', methods=['POST'])
def update_memory():
    data = request.get_json()
    result = m.update(memory_id=data["memory_id"], data=data["data"])
    return jsonify(result), 200

# 获取内存历史
@app.route('/memory/history', methods=['POST'])
def memory_history_view():
    memory_id = request.get_json().get("memory_id")
    history = m.history(memory_id)
    return jsonify(history), 200

# 删除内存
@app.route('/memory/delete', methods=['POST'])
def delete_memory():
    memory_id = request.get_json().get("memory_id")
    m.delete(memory_id)
    return jsonify({"result": "deleted"}), 200

# 删除用户的所有内存
@app.route('/memory/delete_all', methods=['POST'])
def delete_all_memories():
    user_id = request.get_json().get("user_id")
    m.delete_all(user_id=user_id)
    return jsonify({"result": "deleted all"}), 200

# 重置内存
@app.route('/memory/reset', methods=['POST'])
def reset_memory():
    m.reset()
    return jsonify({"result": "reset"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
