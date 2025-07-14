# Reddit Persona Generator 🎭

This project analyzes recent posts from a Reddit **subreddit** and generates a **persona-style resume image** that summarizes the subreddit member’s tone, behavior, key words, and frustrations.

## 🔧 Features
- Uses `PRAW` to fetch Reddit posts.
- Applies `NLTK` for sentiment and keyword analysis.
- Generates a **visually formatted resume image** with `Pillow`.
- Works on both **user URLs** and **subreddit URLs**.

## 🖼️ Sample Output
Generates a resume-style image summarizing:
- Tone (positive/neutral/negative)
- Emoji behavior
- Top keywords
- Common frustrations

## 🚀 Installation

```bash
git clone https://github.com/your-username/reddit-persona.git
cd reddit-persona
pip install -r requirements.txt


