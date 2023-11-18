import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from tkinter import filedialog


import requests
import json
import re
import os
import subprocess
import uuid
import random


def get_video(url):
    video_id = re.search(r'video/(\d+)', url).group(1)
    api_url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"

    headers = {
        'User-Agent': 'TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet'
    }

    response = requests.get(api_url, headers=headers)
    data = json.loads(response.text)
    video_url = data['aweme_list'][0]['video']['play_addr']['url_list'][0]

    return video_url, video_id

def download_video(url):
    video_url, video_id = get_video(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    response = requests.get(video_url, headers=headers)

    if not os.path.exists('InputVideos'):
        os.makedirs('InputViideos')

    with open(f"InputVideos/Downloaded_from_TikTok.mp4", 'wb') as f:
        f.write(response.content)

    return f"InputVideos/Downloaded_from_TikTok.mp4"

