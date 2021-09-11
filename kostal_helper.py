# from https://github.com/ITTV-tools/kostalplenticorepy
import kostalplenticore
from authentication import kostal_ip, kostal_password

kostal = None


def setup():
    global kostal
    kostal = kostalplenticore.connect(kostal_ip, kostal_password)
    kostal.login()


def get_pv_output():
    current_pv_output = kostal.getPvPower()
    print(f"Current PV output: {current_pv_output}")

    return current_pv_output
