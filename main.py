#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import logging

import telegram
from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from filter import BAD_TEXT
from Die_vis import dice_visual
import weather

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

AWAITING_ROLLS = 1
AWAITING_WEATHER = 1


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text(f"Короче, тема такая:\n"
                                    f"Ты кидаешь мне картинку, я на неё реагирую.\n"
                                    f"Ты будешь материться, я тебе рот помою.\n"
                                    f"Можешь мне что-то написать, я тебя по ip чекну.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Я тебе не буду помогать...Хотя ладно, смотри.\n"
                                    "\n/start - Общие правила\n"
                                    "\n/roll - бросить 2 кубика и получить статистику "
                                    "суммы бросков.\n"
                                    "\n/weather - узнать погоду в городе\n")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"Не стоило тебе писать сюда.")
    await update.message.reply_text(f"Никнейм: {update.message.chat.username}\n"
                                    f"Имя: {update.message.chat.first_name}\n"
                                    f"Id: {update.message.chat.id}\n"
                                    f"Локация: {update.message.chat.location}\n"
                                    f"Это бот?: {update.message.from_user.is_bot}\n"
                                    f"Язык в телеге: {update.message.from_user.language_code}\n"
                                    f"Вопросы есть ещё?")


async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"{update.message.chat.first_name},"
                                    f" что это херня..ой, в смысле фотокарточка?")


async def clean_mouth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("И этим ртом ты целуешь Маму?")
    await update.message.delete()
    await update.message.reply_text('Я удалил твоё грязное сообщение,'
                                    ' иди помой свой рот с мылом, пока это не сделал я.')


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user for a city"""
    user = update.message.from_user
    logger.info("User %s started /weather conversation.", user.first_name)
    await update.message.reply_text("Введи название города на английском.\n"
                                    "Пример : Riga / London / New York\n"
                                    "/w_cancel - отменить")

    return AWAITING_WEATHER


async def weather_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected city and executes command"""
    user = update.message.from_user
    logger.info("User %s selected %s", user.first_name, update.message.text)
    city = update.message.text
    await update.message.reply_text("Вот какая погода в городе " + city)
    weather_info = weather.get_weather(city)
    await update.message.reply_text(weather_info)

    return ConversationHandler.END


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about roll number"""
    reply_keyboard = [['100', '500', '1000', '5000', '10000', '50000', '100000']]

    await update.message.reply_text(
        "Давай разберем теорию вероятности"
        " на примере суммы броска 2х 6ти гранных кубиков.\n"
        "\nЕсли бросить 2 кубика, то какая сумма их значений выпадет больше всего раз?\n"
        "\nОтправь /cancel, если хочешь прервать.\n"
        "Сколько раз бросить кубики?",
        reply_markup=telegram.ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Количество бросков"
        ),
    )
    return AWAITING_ROLLS


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stores the selected roll number and execute command"""
    document_path = 'd6_1.html'
    png_document_path = 'd6_1.png'
    try:
        os.remove(document_path)
        os.remove(png_document_path)
        print(f'успешно удален.')
    except FileNotFoundError:
        print(f'Файл не найден.')
    except Exception as e:
        print(f'Произошла ошибка при удалении файла: {e}')

    user = update.message.from_user
    logger.info("User %s rolled %s", user.first_name, update.message.text)
    await update.message.reply_text(f"Количество бросков: {update.message.text}")
    dice_visual.main(int(update.message.text))
    await update.message.reply_text(f"Вот интерактивная статистика для {update.message.text} бросков :\n"
                                    f"Её ты можешь открыть через браузер")
    await update.message.reply_document(open(document_path, 'rb'))
    await update.message.reply_text(f"А вот это PNG файл статистики для {update.message.text} бросков :")
    await update.message.reply_photo(open('d6_1.png', 'rb'))
    # await update.message.reply_text("Если ты используешь компьютер, "
    #                                 "ты можешь открыть этот файл в браузере.\n"
    #                                 "Если ты используешь телефон, "
    #                                 "то тебе придется попытаться открыть "
    #                                 "его самому каким-то образом(особенно на айфоне)")
    try:
        os.remove(document_path)
        os.remove(png_document_path)
        print(f'успешно удален.')
    except FileNotFoundError:
        print(f'Файл не найден.')
    except Exception as e:
        print(f'Произошла ошибка при удалении файла: {e}')


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Значит ты хочешь остаться тупым(ой) и даже "
        "не знать статистику теорию вероятности броска 6ти гранного кубика? "
        "Мдааа...Можешь использовать любую комманду или попытаться исправиться /roll"
        , reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def cancel_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Отмена погоды"
    )

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("YOUR_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("roll", roll)],
        states={
            AWAITING_ROLLS: [MessageHandler(filters.Regex("^[1-9][0-9]*$"), answer)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    weather_handler = ConversationHandler(
        entry_points=[CommandHandler('weather', get_weather)],
        states={
            AWAITING_WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, weather_answer)]
        },
        fallbacks=[CommandHandler('w_cancel', cancel_weather)]
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    application.add_handler(weather_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(BAD_TEXT & ~filters.COMMAND, clean_mouth))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, echo_photo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
