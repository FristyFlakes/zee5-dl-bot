from telethon import TelegramClient, events, Button
import requests
import sqlite3
from headers import headers
import urls
import os
#from flask import request

client = TelegramClient('anfghohn', int(os.environ.get("APP_ID" )), os.environ.get("API_HASH")).start(bot_token= os.environ.get("TG_BOT_TOKEN"))
@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    chat = await event.get_chat()
    await client.send_message(chat,"""Hi, this is Zee5 & MX Player Video Uploader Bot. You can use me for making Streamable Link of any Zee5 or MX Player Video. \n\nSupport Group: @linux_repo \nBy @Discovery_Updates""")
    
@client.on(events.NewMessage(pattern='/help'))
async def handler(event):
    chat = await event.get_chat()
    await client.send_message(chat,"""Hi, this is **Zee5** & **MX Player** Video Transloader Bot. You can use me for making Streamable Link of any Zee5 or MX Player Video. Just copy Video Link from Zee5 or MX Player and send it to me I will Transload it and send it to you. \n\n⭕️ **MX Player Example:** https://www.mxplayer.in/movie/039664d4d85c603cfb5a6cd66b9e29ec \n⭕️ **Zee5 Example:** https://www.zee5.com/movies/details/courier-boy-kalyan-2015-hindi-drama/0-0-courierboykalyan \n\nFormat should be like this, else bot will not work. And no DRM Protected or Premuim Videos Please. \n\nFor more help ask in @linux_repo""", disable_web_page_preview=True)

@client.on(events.NewMessage(pattern='(?i)https://www.zee5.com'))

async def handler(event):
    link =event.text.split('/')[-1]
    
    chat = await event.get_chat()
    w =link
    markup = client.build_reply_markup(Button.url("https://www.zee5.com/tvshows/details/sembaruthi/0-6-675/sembaruthi-november-18-2020/0-1-manual_7adlhget67b0"+link))
    req1 = requests.get(urls.token_url1, headers=headers).json()
    req2 = requests.get(urls.platform_token).json()["token"]
    headers["X-Access-Token"] = req2
    req3 = requests.get(urls.token_url2, headers=headers).json()
           
    r1 = requests.get(urls.search_api_endpoint + w,headers=headers, params={"translation":"en", "country":"IN"}).json()
    g1 = (r1["hls"][0].replace("drm", "hls") + req1["video_token"])
   # await client.send_file(chat,r1["image_url"],caption = r1["title"])
    #markup = client.build_reply_markup(Button.url("Transloaded Link",urls.stream_baseurl+g1))
    await client.send_message(urls.stream_baseurl+g1)
    await client.send_message(chat, "Zee5 Link Transloaded! \n\n"+"**Video Title:** "+r1["title"]+" \n**Video Description:** "+r1["description"],file=r1["image_url"])
            
            #rgx = w
   # await client.send_message(chat, g1)
   #await client.send_message(chat,"445")
    
@client.on(events.NewMessage(pattern='(?i)https://www.mxplayer.in'))
async def handler(event):
    link =event.text.split('/')[-1]
    video_d = "https://llvod.mxplay.com/"
    A =requests.get("https://api.mxplay.com/v1/web/detail/video?type=movie&id="+link+"&platform=com.mxplay.desktop&device-density=2&userid=30bb09af-733a-413b-b8b7-b10348ec2b3d&platform=com.mxplay.mobile&content-languages=hi,en,ta").json()
    #A =requests.get("https://api.mxplay.com/v1/web/detail/video?type=movie&id="+link+"&platform=com.mxplay.desktop&device-density=2&userid=30bb09af-733a-413b-b8b7-b10348ec2b3d&platform=com.mxplay.mobile&content-languages=hi,en,ta").json()
    chat = await event.get_chat()
    #markup = client.build_reply_markup(Button.url("Transloaded Link",video_d+A["stream"]['hls']['high']))
    await client.send_message(video_d+A["stream"]['hls']['high'])
    await client.send_message(chat,"Title: "+A["title"])
    print(A)
    print(link)

@client.on(events.NewMessage(pattern='(?i)https://www.hotstar.com/in/'))
async def handler(event):
    link =event.text
    print(link)
    #import youtube_dl
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
        link,
        download=True # We just want to extract the info
    )
    await client.send_message(chat,result)
    
@client.on(events.NewMessage(pattern='(?i)/ls'))
async def handler(event):
    link =event.text.split(" ")[1]
    e = os.listdir(link)
    chat = await event.get_chat()
    c = "|"
    #str1.join(s)
    #print(c)
    await client.send_message(chat,c.join(e))
@client.on(events.NewMessage(pattern='(?i)sm'))
async def handler(event):
    link =event.text.split(" ")[1]
    print(link)
    chat = await event.get_chat()
    await client.send_file(chat, '/Download'+link,force_document=True)
    
    
    
    
client.start()
client.run_until_disconnected()
