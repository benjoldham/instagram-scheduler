import React, { useState } from "react";
import axios from "axios";

const SchedulePost = () => {
    const [imageUrl, setImageUrl] = useState("");
    const [caption, setCaption] = useState("");
    const [postTime, setPostTime] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        await axios.post("http://localhost:5000/schedule", {
            image_url: imageUrl,
            caption: caption,
            post_time: postTime
        });
        alert("Post Scheduled!");
    };

    return (
        <div>
            <h2>Schedule Instagram Post</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Image URL"
                    value={imageUrl}
                    onChange={(e) => setImageUrl(e.target.value)}
                    required
                />
                <textarea
                    placeholder="Caption"
                    value={caption}
                    onChange={(e) => setCaption(e.target.value)}
                    required
                />
                <input
                    type="datetime-local"
                    value={postTime}
                    onChange={(e) => setPostTime(e.target.value)}
                    required
                />
                <button type="submit">Schedule Post</button>
            </form>
        </div>
    );
};

export default SchedulePost;
