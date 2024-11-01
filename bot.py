import telebot
import requests
from telebot import types

# Initialize the bot
bot = telebot.TeleBot('6892743133:AAEFTD526-R2QzcKrb8C5YaY-Car5X2Dr-M')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Hello {message.from_user.first_name}👋\n\n"
        "This bot can download media from TikTok. To get started, send a link to the video.\n\n"
        "The bot works directly and in chats. Add the bot to the group, then send a link to the video and the bot will send the video to the chat.\n\n"
        "/help - assistance in use"
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Send me a TikTok video URL.')

@bot.message_handler(func=lambda message: message.text.startswith('https://'))
def download_video(message):
    url = message.text
    if not "tiktok.com/@" in url and not "tiktok.com/t/" in url and not "vm.tiktok.com" in url:
        bot.send_message(message.chat.id, "Invalid TikTok URL format. Please paste a valid direct URL to the TikTok video.")
        return
    else:
        bot.send_message(message.chat.id, "Downloading...")   
        try:
            video_path, description , response= tiktok_downloader(url)
            with open(video_path, 'rb') as video:
                keyboard = types.InlineKeyboardMarkup()
                comments = types.InlineKeyboardButton(f"comments 💬 {response['comment_count']}", callback_data='comments')
                likes_count = types.InlineKeyboardButton(f"likes 💖 {response['like_count']}", callback_data='likes')
                keyboard.add(comments, likes_count)
                join_channel = types.InlineKeyboardButton(f"Join channel 🔗", url=f"https://t.me/tegegndev")
                keyboard.add(join_channel)
                bot.send_video(message.chat.id, video, caption=description, reply_markup=keyboard)
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


@bot.message_handler(func=lambda message: True)
def handle_invalid_input(message):
    if not message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Please send a valid URL.')

def tiktok_downloader(video_url):
    api_url = f'https://bj-tricks.serv00.net/BJ_Coder-Apis/TikTok_Api.php?url={video_url}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status
        data = response.json()
        video_content = requests.get(data['url'])
        video_content.raise_for_status()

        with open('video.mp4', 'wb') as file:
            file.write(video_content.content)

        return 'video.mp4', data.get('des', 'TikTok Video'),response.json()
    except requests.RequestException as e:
        raise Exception("Failed to download video.") from e
    except KeyError:
        raise Exception("Unexpected response format from the server.")

print("bot started running")
bot.polling()
