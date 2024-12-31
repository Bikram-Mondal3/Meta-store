# Importing the necessary libraries
import os
import telebot
import yt_dlp
import subprocess

BOT_TOKEN = os.environ.get('Facebook store')  # Ensure this matches the environment variable name

# Initializing the telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Message handler that handles incoming /start, /hello, and /hi commands
@bot.message_handler(commands=['start', 'hello', 'hi'])
def send_welcome(message):
    bot.reply_to(message, "Hello!👋 Nice to meet you. I'm Meta store, your personal social media partner 😊❤️.\nJust send me an URL link and I'll download the video post for you 😉🚀")

# Command to send a video file to a specific user
@bot.message_handler(commands=['send_video'])
def send_video(message):
    video_path = 'output.mp4'  # Replace with the actual path to your video file
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            try:
                bot.send_video(message.chat.id, video, timeout=60)  # Adjusting timeout parameter for your requirements
                bot.reply_to(message, "Your video is successfully downloaded!\nEnjoy 😊🥂")
            except Exception as e:
                bot.reply_to(message, f"Failed to send video: {e}\nTry again the command /send_video")
                return
        
        # Ensure the file handle is closed before deleting the file
        try:
            os.remove(video_path)
        except Exception as e:
           print(f"Video sent, but failed to delete the file: {e}")
    else:
        bot.reply_to(message, "Sorry, I couldn't find the video file. It seems your file is large, be patient and try the command /send_video again later.")

# Handling random text messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    if any(keyword in text for keyword in ["fb.watch", "facebook.com", "youtu.be", "youtube.com", "instagram.com", "x.com", "reddit.com", "tiktok.com"]):
        bot.reply_to(message, "Downloading the content...")
        download_media_content(message)
    else:
        bot.reply_to(message, "I received your message: " + message.text)

# **Download the requested video file**
def download_media_content(message):
    url = message.text
    try:
        # Use yt-dlp to download the video
        result = subprocess.run(["yt-dlp", url, "-o", "output.mp4"], capture_output=True, text=True)
        if result.returncode == 0:
            bot.reply_to(message, "Download complete!\nTry /send_video command to send your video.\nBe patient while we send you the video.")
        else:
            bot.reply_to(message, "Failed to download the video.")
            print(result.stderr)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Add the following to the end of your file to launch the bot
bot.infinity_polling()
