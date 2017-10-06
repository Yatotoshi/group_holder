import random
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def index_of(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1


def remove_ads(posts):
    i = 0
    block_list = [".com", ".ru", ".me", ".cc", ".net",
                  "@", "[", "|", "}",
                  "www.", "http", "https",
                  "/", ":", "родолжение"]
    posts_to_remove = []
    for post in posts:
        for element in block_list:
            if index_of(post["text"], element) != -1 or post["post_type"] != "post":
                posts_to_remove.append(i)
                break
        i += 1

    posts_to_remove.reverse()

    for post_to_remove in posts_to_remove:
        print("Post " + str(posts[post_to_remove].get("id")) + " is an advertisement or reply")
        posts.pop(post_to_remove)

    return posts


def get_random_posts(posts):
    absorbers = json.load(open(os.path.join(THIS_FOLDER, "absorbers.txt"), "r"))
    posts = random.sample(posts, len(posts))

    if len(absorbers) <= len(posts):
        posts = posts[0:len(absorbers)]
    else:
        posts = posts[0:len(posts)]

    for post in posts:
        print("Chosen to post " + str(post["id"]) + " from " + str(post["owner_id"]))

    return posts
