from pyeasee import Easee

from authentication import easee_user, easee_password


async def set_all_charger_states(should_charge, logging_function):
    """Pause or resume all connected easee chargers. Returns True if the state was changed, False if no change was made."""

    # pyeasee most likely automatically refreshes the authentication token
    # but setup every time just to be safe and because calling the function via the telegram thread broke otherwise
    easee = Easee(easee_user, easee_password)
    chargers = await easee.get_chargers()

    for charger in chargers:
        state = await charger.get_state()

        operating_mode = state["chargerOpMode"]

        print(f"Charger: '{charger.name}' - Status: {operating_mode}")

        if operating_mode == "CHARGING" and not should_charge:
            logging_function(f"Genug Saft gezogen. Wallbox '{charger.name}' wird abgeschaltet.")
            await charger.pause()
        elif operating_mode == "AWAITING_START" and should_charge:
            logging_function(f"Ich gönn dir noch n bisschen Strom bei Wallbox '{charger.name}'.")
            await charger.resume()

    await easee.close()