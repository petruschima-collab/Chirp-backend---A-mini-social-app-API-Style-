"""
CHIRP - Tiny Social App
Backend API Simulation using Python Functions

Author:
Assessment:
"""

# ==========================
# In-memory "Database"
# ==========================

users = {}      # username -> {"following": []}
posts = {}      # post_id -> {"author": "", "text": "", "likes": 0}


# ==========================
# 1. Create User
# ==========================

def create_user(username):
    """Register a new user."""

    username = username.strip()

    if username == "":
        return {
            "ok": False,
            "error": "Username cannot be empty."
        }

    if username in users:
        return {
            "ok": False,
            "error": f"User '{username}' already exists."
        }

    users[username] = {
        "following": []
    }

    return {
        "ok": True,
        "user": username
    }


# ==========================
# 2. Create Post
# ==========================

def create_post(username, text):
    """Create a new post."""

    if username not in users:
        return {
            "ok": False,
            "error": f"User '{username}' does not exist."
        }

    text = text.strip()

    if text == "":
        return {
            "ok": False,
            "error": "Post cannot be empty."
        }

    post_id = len(posts) + 1

    posts[post_id] = {
        "author": username,
        "text": text,
        "likes": 0
    }

    # Dictionary unpacking
    return {
        "ok": True,
        "post": {
            "id": post_id,
            **posts[post_id]
        }
    }


# ==========================
# 3. Like Post
# ==========================

def like_post(post_id):
    """Like a post."""

    try:
        post_id = int(post_id)
    except (ValueError, TypeError):
        return {
            "ok": False,
            "error": "Post ID must be a number."
        }

    if post_id not in posts:
        return {
            "ok": False,
            "error": f"Post {post_id} not found."
        }

    posts[post_id]["likes"] += 1

    return {
        "ok": True,
        "post": {
            "id": post_id,
            **posts[post_id]
        }
    }


# ==========================
# 4. Follow User
# ==========================

def follow(follower, followee):
    """Follow another user."""

    if follower not in users:
        return {
            "ok": False,
            "error": f"User '{follower}' does not exist."
        }

    if followee not in users:
        return {
            "ok": False,
            "error": f"User '{followee}' does not exist."
        }

    if follower == followee:
        return {
            "ok": False,
            "error": "You cannot follow yourself."
        }

    if followee not in users[follower]["following"]:
        users[follower]["following"].append(followee)

    return {
        "ok": True,
        "follower": follower,
        "following": users[follower]["following"]
    }


# ==========================
# 5. Get Profile
# ==========================

def get_profile(username):
    """Return user's profile."""

    if username not in users:
        return {
            "ok": False,
            "error": f"User '{username}' does not exist."
        }

    user_posts = []

    for pid, post in posts.items():
        if post["author"] == username:
            user_posts.append({
                "id": pid,
                **post
            })

    return {
        "ok": True,
        "username": username,
        "following": users[username]["following"],
        "posts": user_posts
    }


# ==========================
# 6. Get Feed
# ==========================

def get_feed(username):
    """Return posts from followed users."""

    if username not in users:
        return {
            "ok": False,
            "error": f"User '{username}' does not exist."
        }

    feed = []

    following = users[username]["following"]

    for pid, post in posts.items():
        if post["author"] in following:
            feed.append({
                "id": pid,
                **post
            })

    return {
        "ok": True,
        "feed": feed
    }


# ==========================
# 7. Trending Posts
# ==========================

def trending(n=5):
    """
    Return the top n most-liked posts.

    Uses a list of tuples:
        (likes, post_id)

    Tuples are ideal because they are immutable and
    sort naturally by the first value (likes).
    """

    ranking = []

    for pid, post in posts.items():
        ranking.append((post["likes"], pid))

    ranking.sort(reverse=True)

    trending_posts = []

    for likes, pid in ranking[:n]:
        trending_posts.append({
            "id": pid,
            **posts[pid]
        })

    return {
        "ok": True,
        "trending": trending_posts
    }


# ==========================
# BONUS FUNCTIONS
# ==========================

def unfollow(follower, followee):
    """Remove someone from following list."""

    if follower not in users or followee not in users:
        return {
            "ok": False,
            "error": "User not found."
        }

    if followee in users[follower]["following"]:
        users[follower]["following"].remove(followee)

    return {
        "ok": True,
        "following": users[follower]["following"]
    }


def delete_post(post_id):
    """Delete a post."""

    try:
        post_id = int(post_id)
    except (ValueError, TypeError):
        return {
            "ok": False,
            "error": "Invalid post id."
        }

    if post_id not in posts:
        return {
            "ok": False,
            "error": "Post not found."
        }

    deleted = posts.pop(post_id)

    return {
        "ok": True,
        "deleted": {
            "id": post_id,
            **deleted
        }
    }


def search(term):
    """Search posts containing a keyword."""

    term = term.lower()

    results = []

    for pid, post in posts.items():
        if term in post["text"].lower():
            results.append({
                "id": pid,
                **post
            })

    return {
        "ok": True,
        "results": results
    }


def trending_tags():
    """Return hashtags ranked by frequency."""

    tag_counts = {}

    for post in posts.values():
        words = post["text"].split()

        for word in words:
            if word.startswith("#"):
                tag = word.lower()

                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1

    ranked = sorted(
        tag_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return {
        "ok": True,
        "hashtags": ranked
    }


# ==========================
# TESTING
# ==========================

if __name__ == "__main__":

    print(create_user("Petrus"))
    print(create_user("Sochima"))

    # print(create_post("Petrus", "Hello Chirp Family!"))
    # print(create_post("Petrus", "I am relaible Backend developer #python"))
    # print(create_post("Sochima", "Software Development is the new deal #python"))

    # print(like_post(1))
    # print(like_post("1"))
    # print(like_post(2))

    print(follow("Petrus", "Sochima"))

    # print(get_profile("Petrus"))

    # print(get_feed("Petrus"))

    # print(trending())

    # print(search("python"))

    # print(trending_tags())