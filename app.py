import types
import telebot
import requests


#lets create telegram bot that downloads tiktok videos i will create func that return video url  gimme the rest
bot = telebot.TeleBot('6666666666:AAH-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H')

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_url = types.KeyboardButton('🔗 Join Channel',url='https://t.me/tiktok_downloader_bot')
    keyboard.add(button_url)
    bot.send_message(message.chat.id, 'Hello! I am tiktok downloader bot\nSend me tiktok video url', reply_markup=keyboard)
    bot.send_message(message.chat.id, '🔗 Join Channel',url='https://t.me/tiktok_downloader_bot')
    bot.register_next_step_handler(message, download_video)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '🔗 Join Channel',url='https://t.me/tiktok_downloader_bot')


def download_video(message):
    video_url = message.text
    response = requests.get(video_url)
    return response.json()


bot.polling()   
