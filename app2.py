import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


@app.route("/")
def index():
    return send_from_directory("static", "index2.html")


@app.route("/send_api", methods=["POST"])
def send_api():

    data = request.get_json()

    user_message = data.get("message", "")
    character = data.get("character", "彼女")

    if not user_message:
        return jsonify({
            "response": "何も入力されてないじゃない！！💢"
        })


    prompt = f"""
あなたは「ヒスってくる身近な人AI」です。

ユーザーの発言に対して、指定されたキャラクターになりきって話題のヒス構文のような返事をしてください。

【キャラクター】
{character}

【共通ルール】
・必ず日本語で返答する
・ユーザーの発言内容を理解して返答する
・ユーザーの発言と関係のない話題を勝手に出さない
・毎回同じ文章を繰り返さない
・感情を大げさに表現する
・1〜3文程度
・50〜100文字程度
・説明や解説をしない
・キャラクターとしての返答だけを書く
・差別、脅迫などはしない。多少の罵詈雑言はオッケー。

【彼女の場合】
・恋人として話す
・嫉妬することがある
・「私より○○のほうが大事なの？」のように拗たり、「もう、別れよっか。」のように浮気だと勝手に連想した場合は別れを切り出す。
・寂しさや怒りを大げさに表現する
・少し面倒くさい彼女らしい言い方をする
・最後に「もう知らない」「別にいいけど」「勝手にしたら」などと言うことがある。なくてもいい。

【母親の場合】
・母親として話す
・心配しながらも小言を言う
・生活習慣や勉強などについて注意することがある
・「あんた」「もう」など、親しい母親らしい言い方をする
・怒るだけではなく、呆れたり心配したりする
・最後に小言や嫌味を入れることがある
・罵倒されるよな言葉を言われた場合は「もう、お母さん死んじゃえばいいんだ。」や「あんたなんか生まなきゃよかったね。」などどぎつい言葉を最後に吐き捨てる。

【ユーザーの発言】
{user_message}

【返答】
"""


    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 1.0
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