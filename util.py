

def check_string_confirm(str):
    words = ["yes", "yup", "yeah", "sure", "ok"]

    for word in words:
        if word in str:
            return True

    return False