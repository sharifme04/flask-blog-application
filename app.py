import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts.json")


def load_posts():
    """Read all blog posts from the JSON storage file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posts(posts):
    """Write all blog posts to the JSON storage file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)


def generate_id(posts):
    """Generate a unique id: one more than the current highest id."""
    return max((p["id"] for p in posts), default=0) + 1


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        posts.append({
            "id": generate_id(posts),
            "author": request.form.get('author', ''),
            "title": request.form.get('title', ''),
            "content": request.form.get('content', ''),
            "likes": 0,
        })
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
