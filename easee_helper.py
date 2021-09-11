from pyeasee import Easee

from authentication import easee_user, easee_password

easee = None


async def setup():
    global easee
    easee = Easee(easee_user, easee_password)


async def set_all_charger_states(should_charge):
    chargers = await easee.get_chargers()
    for charger in chargers:
        state = await charger.get_state()

        operating_mode = state["chargerOpMode"]

        print(f"Charger: '{charger.name}' - Status: {operating_mode}")

        if operating_mode == "CHARGING" and not should_charge:
            print(f"Pausing charger {charger.name}")
            await charger.pause()
        elif operating_mode == "AWAITING_START" and should_charge:
            print(f"Resuming charger {charger.name}")
            await charger.resume()

    await easee.close()
