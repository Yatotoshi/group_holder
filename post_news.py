import json
import vk_api
import urllib
import os
from custom_config import config_load
from logger import log
import datetime

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


def generate_attachment_string(attachments):
    file_list = []
    define = ""
    for attachment in attachments:
        if define != "":
            define += ","
        define += attachment["type"]
        define += str(attachment.get(attachment["type"]).get("owner_id"))
        define += "_"
        attachment_id = attachment.get(attachment["type"]).get("id")
        define += str(attachment_id)
    return define


def collect_photos(vk_session, group_id, attachments):
    file_list = []
    for attachment in attachments:
        if attachment["type"] == "photo":
            if attachment["photo"].get("photo_2560") is not None:
                photo_link = attachment["photo"].get("photo_2560")
            elif attachment["photo"].get("photo_1280") is not None:
                photo_link = attachment["photo"].get("photo_1280")
            elif attachment["photo"].get("photo_807") is not None:
                photo_link = attachment["photo"].get("photo_807")
            elif attachment["photo"].get("photo_604") is not None:
                photo_link = attachment["photo"].get("photo_604")

        file_name = photo_link[::-1]
        index = index_of(file_name, "/")
        file_name = file_name[:index]
        file_name = file_name[::-1]

        photo_link_allowed = photo_link[:8] + "pp" + photo_link[index_of(photo_link, ".userapi"):]
        try:
            urllib.request.urlretrieve(photo_link_allowed, os.path.join(THIS_FOLDER, file_name))
        except Exception as error_msg:
            log("Error occurred while downloading photos!\n>>  " + str(error_msg))
            print("Error occurred while downloading photos!\n>>  " + str(error_msg))
            return 1
        file_list.append(file_name)
    return file_list


def post(vk_session, posts):
    group_holder_id = config_load("VKAuth", "id")
    attachments_definition = ""
    absorbers = json.load(open(os.path.join(THIS_FOLDER, "absorbers.txt"), "r"))

    vk = vk_session.get_api()

    i = 0
    for post_el in posts:
            absorber = absorbers[i]

            i += 1
            if i == len(absorbers):
                i = 0

            if "attachments" in post_el:

                if post_el.get("attachments")[0].get("type") == "photo":
                    photos = collect_photos(vk_session, absorber["id"], post_el["attachments"])

                    if photos == 1:
                        print("Error occurred!")
                        continue

                    print("Uploading " + str(len(photos)) + " photo(s) to " + absorber["name"] + "")
                    try:
                        upload = vk_api.VkUpload(vk_session).photo_wall(photos, user_id=group_holder_id, group_id=absorber["id"])
                    except Exception as error_msg:
                        log("Error occurred while uploading photos from " + str(post_el["owner_id"]) + "!\n>>  " + str(error_msg))
                        print("Error occurred while uploading photos from " + str(post_el["owner_id"]) + "!\n>>  " + str(error_msg))
                        continue

                    for photo in photos:
                        os.remove(photo)
                    obj_list = []
                    for photo in upload:
                        photo_obj = {"type":"photo", "photo":{"owner_id":photo["owner_id"], "id":photo["id"]}}
                        obj_list.append(photo_obj)
                    attachments_definition = generate_attachment_string(obj_list)
                else:
                    attachments_definition = generate_attachment_string(post_el["attachments"])
            try:
                if post_el["text"] == "":
                    posted_obj = vk.wall.post(owner_id="-" + absorber["id"], from_group=1, attachments=attachments_definition)
                else:
                    posted_obj = vk.wall.post(owner_id="-" + absorber["id"], message=post_el["text"], from_group=1, attachments=attachments_definition)
                print(">> Posted to " + absorber["name"] + " successful!")
                post_owner = open(os.path.join(THIS_FOLDER, "post_owner.txt"), "a")
                post_owner.write("[" + datetime.datetime.now().isoformat(sep=' ') + "] to \"" + str(absorber["name"]) + "\" posted " + str(posted_obj["post_id"]) + " from " + str(post_el["owner_id"]) + "\n")
            except Exception as error_msg:
                log("Error occurred while posting " + str(post_el["id"]) + " from " + str(post_el["owner_id"]) + "!\n>>  " + str(error_msg))
                print("Error occurred while posting " + str(post_el["id"]) + " from " + str(post_el["owner_id"]) + "!\n>>  " + str(error_msg))
                continue
