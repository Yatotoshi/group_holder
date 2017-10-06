import json
import os
from logger import log

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def get_last_posts(vk_session):
    new_posts = []
    victims = json.load(open(os.path.join(THIS_FOLDER, "victims.txt"), "r"))                                    # load victims to a vector

    vk = vk_session.get_api()

    for victim in victims:                                                              # for every victim
        try:
            response = vk.wall.get(count=2, domain=victim.get("id"))                        # get the last post
        except Exception as error_msg:
            log(str("Error occurred while getting new post from " + str(victim["id"]) + "public!\n>>  " + str(error_msg)))
            print("Error occurred while getting new post from " + str(victim["id"]) + "public!\n>>  " + str(error_msg))
            return 1

        if response["items"] and response["items"][1].get("id") != victim.get("last"):  # if it is not posted
            print("Getting new wall post from " + victim["id"])
            new_posts.append(response["items"][1])                                      # add it to the returned vector of new posts
            victim["last"] = response["items"][1].get("id")                             # else - continue with the next victim

    json.dump(victims, open(os.path.join(THIS_FOLDER, "victims.txt"), "w"))
    return new_posts
