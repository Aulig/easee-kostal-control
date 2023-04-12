import asyncio

from telegram.ext import Updater, CommandHandler, ApplicationBuilder

import easee_helper
import kostal_helper
import settings
from authentication import telegram_token, telegram_password

trusted_chats = []
automatic_charging_control = True


def run_bot():
    application = ApplicationBuilder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("authenticate", authenticate))

    application.add_handler(CommandHandler("manual", manual))

    application.add_handler(CommandHandler("auto", auto))

    application.add_handler(CommandHandler("current", current))

    application.job_queue.run_repeating(callback=check, interval=60 * settings.check_every_minutes, first=10)

    application.run_polling()


async def check(context):
    if automatic_charging_control:
        current_pv_output = kostal_helper.get_pv_output()
        print(f"Current PV output: {current_pv_output}")

        await easee_helper.set_all_charger_states(current_pv_output >= settings.min_watt_to_charge, get_messenger_function(context))
    else:
        print("Automatic charging control is disabled.")


def get_messenger_function(context):
    def wrapped(message):
        return message_all_trusted_chats(context, message)

    return wrapped

def message_all_trusted_chats(context, message):
    for trusted_chat in trusted_chats:
        context.bot.send_message(chat_id=trusted_chat, text=message)


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Willkommen an der Zapfsäule. Sag mir mit /authenticate das Passwort.")


async def authenticate(update, context):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sag mir das Passwort.")
    else:
        password = context.args[0]

        if password == telegram_password:
            trusted_chats.append(update.effective_chat.id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Alles klar, ich vertraue dir. Du kannst jetzt /manual und /auto nutzen.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Falsch.")


def is_authenticated(update):
    return update.effective_chat.id in trusted_chats


def check_authentication(command_function):
    async def decorator(update, context):
        if is_authenticated(update):
            await command_function(update, context)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Von dir lass ich mir gar nichts sagen. Sag mir mit /authenticate das Passwort.")

    return decorator


@check_authentication
async def auto(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Soso, willst du also doch meine Hilfe.")

    global automatic_charging_control
    automatic_charging_control = True


@check_authentication
async def manual(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Dann mach halt selber wenn du willst.")

    global automatic_charging_control
    automatic_charging_control = False

    await easee_helper.set_all_charger_states(True, get_messenger_function(context))


async def current(update, context):
    current_pv_output = round(kostal_helper.get_pv_output())

    if current_pv_output > settings.min_watt_to_charge:
        message = f"Bei {current_pv_output} Watt geb ich gern ein bisschen Strom ab."
    else:
        message = f"Nur {current_pv_output} Watt? Da brauch ich alles selbst für meine Bitcoin miner."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)



