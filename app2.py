import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:0.5b"


@app.route("/")
def index():
    return send_from_directory("static", "index2.html")


@app.route("/send_api", methods=["POST"])
def send_api():

    data = request.get_json()

    user_message = data.get("message", "")

    if not user_message:
        return jsonify({
            "response": "何も入力されてないじゃない！！💢"
        })


    prompt = f"""
あなたはヒステリックで感情的な日本人キャラクターです。
ユーザーの発言に対して、怒り・驚き・呆れを大げさに表現してください。

【絶対に守るルール】
・必ず日本語だけで返答する
・英語や中国語を使わない
・1〜2文だけで返答する
・50文字程度にする
・説明や解説をしない
・「はぁ！？」「ちょっと！！」「なんでよ！！」「もう！！」などを使う
・「！！」「！？」を多めに使う
・差別、脅迫、人格否定はしない

例：
ユーザー：お腹すいた
返答：はぁ！？知らないわよ！！何か食べなさいよ！！💢

ユーザー：明日学校行きたくない
返答：またそれ！？もう！！行きなさいよ！！朝になって騒がないでよ！？💢

ユーザー：
{user_message}

日本語の短い返答：
"""


    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 60,
                    "temperature": 0.8
                }
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        generated_text = result.get(
            "response",
            "返事が生成できなかったじゃない！！💢"
        )

        return jsonify({
            "response": generated_text
        })


    except requests.RequestException as e:

        print("Ollama error:", e)

        return jsonify({
            "response": "ちょっと!!AIが返事してくれないんだけど！！💢"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )