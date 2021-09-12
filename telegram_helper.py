import asyncio

from telegram.ext import Updater, CommandHandler

import easee_helper
import kostal_helper
import settings
from authentication import telegram_token, telegram_password

trusted_chats = []
automatic_charging_control = True


def run_bot():
    updater = Updater(token=telegram_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("authenticate", authenticate))

    dispatcher.add_handler(CommandHandler("manual", manual))

    dispatcher.add_handler(CommandHandler("auto", auto))

    dispatcher.add_handler(CommandHandler("current", current))

    dispatcher.job_queue.run_repeating(callback=check, interval=60 * settings.check_every_minutes, first=10)

    updater.start_polling()


def check(context):
    if automatic_charging_control:
        current_pv_output = kostal_helper.get_pv_output()
        print(f"Current PV output: {current_pv_output}")

        asyncio.run(easee_helper.set_all_charger_states(current_pv_output >= settings.min_watt_to_charge, get_messenger_function(context)))
    else:
        print("Automatic charging control is disabled.")


def get_messenger_function(context):
    def wrapped(message):
        return message_all_trusted_chats(context, message)

    return wrapped

def message_all_trusted_chats(context, message):
    for trusted_chat in trusted_chats:
        context.bot.send_message(chat_id=trusted_chat, text=message)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Willkommen an der Zapfsäule. Sag mir mit /authenticate das Passwort.")


def authenticate(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sag mir das Passwort.")
    else:
        password = context.args[0]

        if password == telegram_password:
            trusted_chats.append(update.effective_chat.id)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Alles klar, ich vertraue dir. Du kannst jetzt /manual und /auto nutzen.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Falsch.")


def is_authenticated(update):
    return update.effective_chat.id in trusted_chats


def check_authentication(command_function):
    def decorator(update, context):
        if is_authenticated(update):
            command_function(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Von dir lass ich mir gar nichts sagen. Sag mir mit /authenticate das Passwort.")

    return decorator


@check_authentication
def auto(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Soso, willst du also doch meine Hilfe.")

    global automatic_charging_control
    automatic_charging_control = True


@check_authentication
def manual(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Dann mach halt selber wenn du willst.")

    global automatic_charging_control
    automatic_charging_control = False

    # we can't await it because we can't make manual async (tried run_async in CommandHandler too)
    asyncio.run(easee_helper.set_all_charger_states(True, get_messenger_function(context)))


def current(update, context):
    current_pv_output = round(kostal_helper.get_pv_output())

    if current_pv_output > settings.min_watt_to_charge:
        message = f"Bei {current_pv_output} Watt geb ich gern ein bisschen Strom ab."
    else:
        message = f"Nur {current_pv_output} Watt? Da brauch ich alles selbst für meine Bitcoin miner."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)



