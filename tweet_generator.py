import subprocess
import json
import os

def load_file(path):
    with open(path, "r") as f:
        return f.read()

SCHOOL_INFO = load_file(os.path.expanduser("~/sunabaco-tweet/school_info.txt"))
PAST_TWEETS = load_file(os.path.expanduser("~/sunabaco-tweet/past_tweets.txt"))

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

def generate_tweets(category, extra_info):
    prompt = f"""あなたはSUNABACO NEYAGAWAというプログラミング・ビジネススクールの公式Twitterアカウントの中の人です。

以下の教室情報と過去ツイートのトーンを参考に、ツイートを3案作成してください。

【教室情報】
{SCHOOL_INFO}

【過去ツイート例（トーン参考）】
{PAST_TWEETS}

【今回のカテゴリ】
{category}

【追加情報・今日のネタ】
{extra_info if extra_info else "特になし"}

【ツイート作成ルール】
- 140文字以内
- 過去ツイートのトーンに合わせる（フランクで親しみやすい）
- ハッシュタグは最後に2〜3個
- 改行を使って読みやすくする
- トレンドワードや外部の人が検索しそうなワードを自然に入れる
- 3案それぞれ少し違うアプローチで

【出力形式】
--- 案1 ---
（ツイート本文）

--- 案2 ---
（ツイート本文）

--- 案3 ---
（ツイート本文）"""

    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout

def main():
    print("\n🌴 SUNABACO NEYAGAWA ツイート生成ツール\n")
    print("カテゴリを選んでください：")
    for key, val in CATEGORIES.items():
        print(f"  {key}. {val}")

    category_key = input("\n番号を入力 > ").strip()
    category = CATEGORIES.get(category_key, "日常・オープン")

    print(f"\n今日の追加情報があれば入力してください（なければEnter）")
    print("例：今日は雨、新しい本が入った、イベントは明日など")
    extra_info = input("> ").strip()

    print("\n⏳ 生成中...\n")
    result = generate_tweets(category, extra_info)
    print(result)
    print("\n✅ 気に入った案をコピーして投稿してください！\n")

if __name__ == "__main__":
    main()
