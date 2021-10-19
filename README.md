# What is this?

A python script you can run to automatically stop and resume charging your electric vehicle depending on whether your photovoltaic system is producing power at the moment.
It checks Kostal plenticore systems to control easee charging boxes.

# Setup
- Clone this repo
- Download [kostalplenticorepy](https://github.com/ITTV-tools/kostalplenticorepy) as `kostalplenticore.py` (from the src folder of that repository)
- Run `pip install -r requirements.txt`
- Create `authentication.py` with these variables:
  - kostal_ip = "Your kostal IP (without http)"
  - kostal_password = "Your kostal password"
  - easee_user = "Your easee username (phone number or email)"
  - easee_password = "Your easee password"
  - telegram_token = "Your telegram bot HTTP API token"
  - telegram_password = "The password you will need to give your Telegram bot before you can control charging with it (you pick it yourself)"
- Update the `check_every_minutes` and `min_watt_to_charge` parameters in `settings.py` if you'd like. (See the comments in that file for an explanation of the parameters)
- Run `python main.py`