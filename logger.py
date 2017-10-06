from urllib import request
from custom_config import config_load
import time, datetime


def try_send(get_parameters, date, message):
    try:
        print("Try sending error")
        request.urlopen("https://api.telegram.org" + get_parameters + message + "%0Aat%20" + str(date))
        print("Error sent")
    except Exception as error_msg:
        print("Unable to sent error\n" + str(error_msg))
        return 1
    return 0


def log(message):
    date = datetime.datetime.now().isoformat(sep=' ')
    bot_token = config_load("BOT", "token")
    message = request.quote(message)
    get_parameters = bot_token + "/sendMessage?chat_id=287322046&text="

    sending_error = try_send(get_parameters, date, message)

    while sending_error == 1:
        time.sleep(int(30))
        sending_error = try_send(get_parameters, date, message)
    return 0
