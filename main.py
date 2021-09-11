import asyncio

import easee_helper
import kostal_helper


check_every_minutes = 30
min_watt_to_charge = 2000


async def main():
    while True:
        # not sure if kostal automatically refreshes sessions when they expire, so setup every time
        kostal_helper.setup()

        # pyeasee most likely automatically refreshes the authentication token, but setup every time just to be safe
        await easee_helper.setup()

        current_pv_output = kostal_helper.get_pv_output()

        await easee_helper.set_all_charger_states(current_pv_output >= min_watt_to_charge)

        await asyncio.sleep(check_every_minutes * 60)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
