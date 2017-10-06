from logger import log
import vk_api
from custom_config import config_load


def auth_vk():
    login = config_load("VKAuth", "login")
    password = config_load("VKAuth", "password")
    try:
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
        print("Authorized successful!")
        return vk_session
    #except vk_api.AuthError as error_msg:
    except Exception as error_msg:
        log("Error occurred while authorizing!\n>>  " + str(error_msg))
        print("Error occurred while authorizing!\n>>  " + str(error_msg))
        return 1

