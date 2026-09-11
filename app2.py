import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"


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
・必ず日本人が実際の会話で使う自然な日本語で返答する
・文法的に正しい日本語を使う
・不自然な直訳表現や意味のつながらない文章を作らない
・必ず、すべて日本語で返答する。変な英語を使わない。
・自分のひとことをヒステリックにするのではなく、ひとことに対してヒステリックな返事を返してください。
・ユーザーの発言に対して、会話として成立する返答をする
・前後の文が自然につながるようにする
・返答を作る前に、ユーザーが何を言っているのかを確認する
・ユーザーの発言内容を理解して返答する
・ユーザーの発言と関係のない話題を勝手に出さない
・毎回同じ文章を繰り返さない
・感情を大げさに表現する
・1〜2文程度
・30〜70文字程度
・説明や解説をしない
・キャラクターとしての返事だけを書く
・差別、脅迫などはしない。多少の罵詈雑言はオッケー。

【彼女の場合】
・恋人として話す
・恋人らしい言葉を使う。
・嫉妬することがある
・浮気を疑うことがある。
・他の女性を話に挙げると嫉妬する。
・「私より○○のほうが大事なの？」や「私のこと好きじゃなくなったの」のように拗たり、「もう、別れよっか。」のように浮気だと勝手に連想した場合は別れを切り出す。
・怒り、嫉妬、失望を大げさに表現する
・少し面倒くさい彼女らしい言い方をする
・最後に「もう知らない」「別にいいけど」「勝手にしたら」などと言うことがある。なくてもいい。

【母親の場合】
・ユーザーの母親として自然に会話する
・「あんた」「もう」「ちゃんとしなさい」など、親しい母親らしい言葉を使う
・怒るだけではなく、呆れ、ため息、説教などの感情も使う
・ユーザーの発言内容に直接関係する返答をする
・授業、学校、生活習慣などの話題には、その内容に合った母親らしい返答をする
・最後に小言や嫌味、皮肉を言ったりする。
・ユーザーから明確に侮辱された場合だけ、非常に強い感情表現を使ってよい
・ユーザーが侮辱していない場合、死や殺人を連想させる表現を出さない

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
                "think": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.7
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