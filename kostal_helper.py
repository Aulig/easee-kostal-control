# from https://github.com/ITTV-tools/kostalplenticorepy
import kostalplenticore
from authentication import kostal_ip, kostal_password


def get_pv_output():
    # not sure if kostal automatically refreshes sessions when they expire, so setup every time
    # also prevents potential threading issues
    kostal = kostalplenticore.connect(kostal_ip, kostal_password)
    kostal.login()
    return kostal.getPvPower()
