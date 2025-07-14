import praw
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import re

from persona import save_persona_as_image  

nltk.download('vader_lexicon')
nltk.download('stopwords')

def extract_subreddit_name(url):
    return url.strip().rstrip('/').split("/")[-1]

def fetch_subreddit_posts_praw(subreddit_name, limit=30):
    reddit = praw.Reddit(
        client_id="QJctggGMpRbKZT1_y7hG4A",
        client_secret="WtKEfmh-AbGZvwvkWPxNNi-xc4OqHA",
        user_agent="RedditPersonaScript/0.1 by PersonaScript"
    )
    posts = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=limit):
            text = submission.title + " " + (submission.selftext or "")
            posts.append(text)
    except Exception as e:
        print(f"Error fetching posts from r/{subreddit_name}: {e}")
    return posts


def analyze_posts(posts):
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words('english'))

    all_words = []
    sentiments = []
    post_lengths = []
    emoji_count = 0
    frustrations = []

    for post in posts:
        words = re.findall(r'\b\w+\b', post.lower())
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(filtered_words)

        sentiment = sia.polarity_scores(post)
        sentiments.append(sentiment['compound'])

        post_lengths.append(len(post.split()))
        emoji_count += len(re.findall(r'[^\w\s,]', post))

        if any(neg in post.lower() for neg in ["hate", "wait", "frustrated", "annoyed", "delay", "confused"]):
            frustrations.append(post.strip())

    common_words = Counter(all_words).most_common(10)
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    avg_length = sum(post_lengths) / len(post_lengths) if post_lengths else 0

    return {
        "keywords": common_words,
        "avg_sentiment": avg_sentiment,
        "avg_length": avg_length,
        "emoji_count": emoji_count,
        "frustrations": frustrations[:3]
    }


def main():
    subreddit_url = input("🔗 Enter a subreddit URL (e.g., https://www.reddit.com/r/Deltarune/): ").strip()
    subreddit = extract_subreddit_name(subreddit_url)
    print(f"Fetching posts from r/{subreddit}...")
    posts = fetch_subreddit_posts_praw(subreddit)
    if not posts:
        print("❌ No posts found. Please check the subreddit name or try another one.")
        return
    info = analyze_posts(posts)
    save_persona_as_image(info)

if __name__ == "__main__":
    main()
