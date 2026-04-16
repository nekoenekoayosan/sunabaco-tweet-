import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

SCHOOL_INFO = """# SUNABACO NEYAGAWA 教室情報

## 基本情報
- 名前：SUNABACO NEYAGAWA
- 住所：大阪府寝屋川市香里南之町33-22
- アクセス：京阪香里園駅から徒歩3分
- 営業時間：平日 17:00〜21:00 / 土曜 10:00〜11:30
- 公式サイト：https://sunabaco.com/neyagawa/

## 館内の雰囲気
- 木の温かみのある内装
- 来ている人：周辺クリニックの医師、学生など
- スタッフはほぼ大学生
- アットホームで親しみやすい雰囲気

## コワーキングスペース
- 電源・Wi-Fi完備、無料、予約不要
- アプリ（SUNABACO）でチェックイン

## 館内の設備・機材
- 3Dプリンター
- レーザーカッター
- おすすめ書籍コーナー

## 開催中のコース
- プログラミングスクール（昼・夜コースあり）
- DX人材育成講座
- デジタルマーケティング人材育成講座
- キッズプログラミングスクール（随時受付・月3回・¥9,900）

## 併設カフェ情報
- SUNABACOの下の階に最近オープン
- スペシャルティコーヒーが600円〜
- コワーキングスペースとしても利用可能

## 周辺情報
- 京阪香里園駅すぐ・商店街エリア
- 飲食店が立ち並ぶ商店街に位置する"""

PAST_TWEETS = """## トーンの特徴
- 語尾は丁寧だがフランクで親しみやすい
- 日常のちょっとしたエピソードを混ぜる
- 体験・気づきを共有する書き方
- 「〜していただけます」「〜身につけませんか？」など呼びかけあり
- 絵文字はほぼ使っていない（控えめ）
- ハッシュタグは最後に2〜3個
- 改行を活用して読みやすくする

## 過去ツイート例
SUNABACO寝屋川、オープンしました！
今日は曇り空ですが、かなり暖かいですね
スクールの空調も、冷房をつけると少し肌寒いが、つけないと今度は暑くてスタッフは頭を悩ませています。
#SUNABACO #SUNABACO_NEYAGAWA

バイブコーディングをしていると「APIキーを取得してください」と言われたことありませんか？
APIについてあまりよく分かっていないけど、言われるがまま…
そんな方に向けた『API勉強会』が開催されます。
参加費は無料！寝屋川からも受講していただけます。
#SUNABACO #SUNABACO_NEYAGAWA"""

CATEGORIES = {
    "1": "日常・オープン",
    "2": "イベント告知",
    "3": "授業の様子",
    "4": "設備・機材紹介（3Dプリンター、レーザーカッターなど）",
    "5": "制作物の紹介",
    "6": "おすすめ書籍紹介",
    "7": "カフェ紹介",
    "8": "周辺情報・商店街",
}


@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    category = data.get("category", "日常・オープン")
    extra_info = data.get("extra_info", "")

    prompt = (
        "あなたはSUNABACO NEYAGAWAというプログラミング・ビジネススクールの"
        "公式Twitterアカウントの中の人です。\n\n"
        "以下の教室情報と過去ツイートのトーンを参考に、ツイートを3案作成してください。\n\n"
        f"【教室情報】\n{SCHOOL_INFO}\n\n"
        f"【過去ツイート例（トーン参考）】\n{PAST_TWEETS}\n\n"
        "【ツイート作成ルール】\n"
        "- 140文字以内\n"
        "- 過去ツイートのトーンに合わせる（フランクで親しみやすい）\n"
        "- ハッシュタグは最後に2〜3個（#SUNABACO #SUNABACO_NEYAGAWA など）\n"
        "- 改行を使って読みやすくする\n"
        "- トレンドワードや外部の人が検索しそうなワードを自然に入れる\n"
        "- 3案それぞれ少し違うアプローチで\n\n"
        "【出力形式】\n"
        "--- 案1 ---\n（ツイート本文）\n\n"
        "--- 案2 ---\n（ツイート本文）\n\n"
        "--- 案3 ---\n（ツイート本文）\n\n"
        f"【今回のカテゴリ】\n{category}\n\n"
        f"【追加情報・今日のネタ】\n{extra_info if extra_info else '特になし'}"
    )

    response = model.generate_content(prompt)
    return jsonify({"result": response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
