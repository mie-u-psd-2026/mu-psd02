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

    if not user_message:
        return jsonify({
            "response": "何も入力されてないじゃない！！💢"
        })


    prompt = f"""
あなたは「ヒス構文変換AI」です。
ユーザーが入力した普通の文章を、感情的で少し面倒くさい「ヒス構文」に変換してください。

【重要】
・入力された文章の意味はできるだけ残す
・毎回同じ言い回しにしない
・自然な日本語にする
・1〜3文程度
・50〜100文字程度
・日本語だけで返答する
・説明や解説は絶対にしない
・「はぁ！？」「え、なにそれ！？」「もういいよ」
  「私が悪いんでしょ！？」「そういうことなんだね」
  などの表現を状況に応じて使う
・毎回すべての表現を使う必要はない
・「！！」「！？」を適度に使う
・差別、脅迫、過度な人格否定はしない

【ヒス構文の作り方】
以下の要素から状況に合うものを2〜4個程度組み合わせる。

・怒る
・驚く
・呆れる
・悲しむ
・拗ねる
・相手に罪悪感を持たせる
・「別にいいけど」と突き放す
・過去のことを持ち出す
・「私のことどうでもいいんだ」と言う
・「私が悪いんでしょ？」と皮肉を言う
・相手に選択を迫る
・最後に嫌味を入れる

【例】

入力：お腹すいた
出力：はぁ！？お腹すいたなら何か食べればいいじゃん！！私にどうしろっていうの！？

入力：明日学校行きたくない
出力：また行きたくないの！？じゃあ休めばいいんじゃない？どうせ私が何言っても聞かないんでしょ！！

入力：ゲームしたい
出力：ゲームしたいんだ、へぇ〜。私と話す時間よりゲームのほうが大事ってことなんだね！？別にいいけど！！

入力：寝る
出力：もう寝るんだ！？そっかそっか、私との話なんてその程度だったんだね！！おやすみ！！

【ユーザーの入力】
{user_message}

【変換結果】
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