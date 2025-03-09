from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import schedule
import time
import threading

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
CORS(app)

# Instagram API Credentials (Replace with actual values)
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
INSTAGRAM_USER_ID = "YOUR_INSTAGRAM_USER_ID"

class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=False)
    post_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="scheduled")

# Function to post on Instagram
def post_to_instagram(post_id):
    post = ScheduledPost.query.get(post_id)
    if not post or post.status == "posted":
        return

    url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_USER_ID}/media"
    payload = {
        "image_url": post.image_url,
        "caption": post.caption,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    container_id = response.json().get("id")

    if container_id:
        publish_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_USER_ID}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        if "id" in publish_response.json():
            post.status = "posted"
            db.session.commit()

# Schedule posts
def check_and_post():
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    posts = ScheduledPost.query.filter_by(post_time=now, status="scheduled").all()
    for post in posts:
        post_to_instagram(post.id)

# API to schedule a post
@app.route("/schedule", methods=["POST"])
def schedule_post():
    data = request.json
    new_post = ScheduledPost(
        image_url=data["image_url"],
        caption=data["caption"],
        post_time=data["post_time"]
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post scheduled successfully!"})

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = ScheduledPost.query.all()
    return jsonify([{"id": p.id, "image_url": p.image_url, "caption": p.caption, "post_time": p.post_time, "status": p.status} for p in posts])

# Run scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
