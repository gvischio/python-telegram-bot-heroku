import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

from datetime import date
import datetime
today = date.today()

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '2005961070:AAEdp4NMbA3yjFGOlx8lTEYhuAl-sYzb84w'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def rifiuti(update, context):
    """Send a message when the command /rifiuti is issued."""
    rifiuti = ["Residuo, vetro, organico", "", "",
               "Carta, organico", "Imballaggi", "", ""]
    weekday = today.weekday()
    update.message.reply_text(
        'Rifiuti per il giorno di oggi: ' + rifiuti[weekday])


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def weekly_job(bot, update, job_queue):
    """ Running on Mon = tuple(range(1)) """
    #bot.send_message(chat_id="Ruoli", text='Setting a daily notifications!')
    t = datetime.time(22, 47, 00, 000000)
    job_queue.run_daily(notify_roles, t, days=(3), context=update)


def notify_roles(bot, job):
    resto = (today.isocalendar()[1]) % 4
    nomi = ["Valentina", "Nicola", "Giacomo", "Asia"]
    turni = ["Cucina", "Bagno", "Spazzatura", "Pavimenti"]
    messaggi = ["Valentina: Pavimenti", "Nicola: Cucina",
                "Giacomo: Bagno", "Asia: Cucina"]
    toPrint = ""
    for i in range(4):
        toPrint += nomi[i] + "  : " + turni[(i + resto) % 4] + "\n"
        #messaggi[i] = nomi[i] + "  : " + turni[(i + resto) % 4]
        #toPrint = toPrint + messaggi[i] + "\n"
    #dp.sendMessage(chat_id="Ruoli", text=toPrint)
    bot.sendMessage(chat_id="Ruoli", text=toPrint)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rifiuti", rifiuti))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # to print message at certain time
    giorno = today.weekday()
    settimana = today.isocalendar()[1]
    ora = datetime.datetime.now().hour
    minuti = datetime.datetime.now().minute
    resto = settimana % 4
    nomi = ["Valentina", "Nicola", "Giacomo", "Asia"]
    turni = ["Cucina", "Bagno", "Spazzatura", "Pavimenti"]
    messaggi = ["Valentina: Pavimenti", "Nicola: Cucina",
                "Giacomo: Bagno", "Asia: Cucina"]
    toPrint = ""
    if giorno == 0 and ora == 8 and minuti == 0:
        for i in range(4):
            messaggi[i] = nomi[i] + "  : " + turni[(i + resto) % 4]
            toPrint = toPrint + messaggi[i] + "\n"
    #dp.sendMessage(chat_id="Ruoli", text=toPrint)
    #bot.sendMessage(chat_id="Ruoli", text=toPrint)

    dp.add_handler(CommandHandler('notify', weekly_job, pass_job_queue=True))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://prova-bot-povo.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
