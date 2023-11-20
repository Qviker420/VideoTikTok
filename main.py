from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess
import os

TOKEN: Final = '6495099175:AAH22qel2Eu91d16MBbnC7ImVNhtxD6-V6A'
BOT_USERNAME: Final = '@tiktok_video_generator_bot'
path = ""
pathes = []
def run_external_script(parameter1, parameter2):
    command = ["python", "edit_video_downloaded.py", parameter1, parameter2]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        path = result.stdout.strip()
        print(path)
        #print("Output of the external script:", result.stdout)
        if "OutPutsWithSound\TikTok" in path:
    
            for src in path.splitlines():
                if src.startswith('OutPutsWithSound'):
                    pathes.append(src)
            print("pathes :", pathes)

    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)


async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text('''
Send tiktok URL of video you want to reuse and how many copies you need
recommended minimum 3 copies use 2 spaces to separate url and number of copies
in next format: "http://tiktok.com/examples/url  3"
                         
this will generate 3 copies
                                    ''')



#Response
def process_text(text:str) -> str:
     processed: str = text.lower()
     if 'tiktok.com' in processed:
          
          return processed.split("  ")
     else:
          return 'Invalid tiktok url'


async def handle_response(update: Update, context: ContextTypes):
    processed: str = update.message.text.lower()
    
    response = process_text(processed)
    print(response)

    await update.message.reply_text("Starting Generating Video...")
    run_external_script(response[0], response[1])
    for src in pathes:
        await update.message.reply_text("Video Generated Uploading now...")
        await update.message.reply_video(src)
        
    for p in pathes:
        os.remove(p)
    pathes.clear()
    print(pathes)
    await update.message.reply_text("This Was Last Video")
    
        
    


#Response

if __name__ == '__main__':
    print('Starting Bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_response))
    print('Polling ...')
    app.run_polling(poll_interval=3)