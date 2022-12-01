

def check_string_confirm(str):
    words = ["yes", "yup", "yeah", "sure", "ok", "understand", "ready", "good", "start"]

    for word in words:
        if word in str:
            return True

    return False