from requests import get
from re import findall
import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from difflib import SequenceMatcher

from api_rubika import Bot,encryption

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
 

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                    bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def joker(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        return False

def info_qroz(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
            text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_ping(text,chat,bot):
    try:
        site = text[7:-1]
        jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
        text = str(jd)
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ping err')
    return True

def get_gold(text,chat,bot):
    try:
        r = json.loads(requests.get('https://www.wirexteam.ga/gold').text)
        change = str(r['data']['last_update'])
        r = r['gold']
        text = ''
        for o in r:
            text += o['name'] + ' : ' + o['nerkh_feli'] + '\n'
        text += '\n\nآخرین تغییر : ' + change
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + ' به پیوی شما ارسال شد', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_pa_na_pa(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/pa-na-pa/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz pa na pa err')
    return True

def get_Time(text,chat,bot):
    try:                        
        jd = json.loads(requests.get('http://api.codebazan.ir/time-date/?json=all').text)
        jd = jd['result']
        
        text = '📆تاریخ میلادی : '+jd['dateen'] + '\n🕰ساعت انگلیسی : '+jd['timeen'] + '\n\n📆تاریخ شمسی : '+jd['datefa'] + '\n🕰ساعت فارسی : '+jd['timefa']
        
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz server err')
    return False
        
def get_password(text,chat,bot):
    try:                       
        jd = requests.get('http://api.codebazan.ir/password/?length=8').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz server err')
    return False
                
def get_zekr(text,chat,bot):
    try:                        
        jd = requests.get('http://api.codebazan.ir/zekr/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz server err')
    return False        

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True

def get_dialog(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dialog/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dialog err')
    return True  
                                
def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        send_text = 'بای بای 🖖'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        send_text = 'سلام دوست عزیز به ' + group + ' خوش آمدی ❤ \n لطفا قوانین رو رعایت کن ✅'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def get_meno(text,chat,bot):                                
    text = open('help2.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help2 guid sended')
    
def get_Entertainment(text,chat,bot):                                
    text = open('Entertainment.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'لیست سرگرمی به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('Entertainment guid sended')
    
def get_google(text,chat,bot):                                
    text = open('google.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'لیست جستجو به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('google guid sended')
    
def get_Tools(text,chat,bot):                                
    text = open('Tools.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'لیست ابزار ها به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('Tools guid sended')

def get_Ply(text,chat,bot):                                
    text = open('Ply.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'لیست بازی به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('Ply guid sended')

def get_geps(text,chat,bot):                                
    text = open('geps.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('geps guid sended')

def get_Tonbr(text,chat,bot):                                
    text = open('Tonbr.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'لیست قوانین به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('Tonbr guid sended')

def get_Programming(text,chat,bot):                                
    text = open('Programming.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'بخش برنامه نویسی به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('Programming guid sended')
    
def get_calculator(text,chat,bot):                                
    text = open('calculator.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'بخش ماشین حساب به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('calculator guid sended')
    
def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '!usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

def code_run(text,chat,bot,lang_id):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                h = {
                    "Origin":"https://sourcesara.com",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                }
                p = requests.post('https://sourcesara.com/tryit_codes/runner.php',{'LanguageChoiceWrapper':lang_id,'Program':txt_xt},headers=h)
                p = p.json()
                jj = hasInsult(p['Result'])
                jj2 = hasInsult(p['Errors'])
                time_run = p['Stats'].split(',')[0].split(':')[1].strip()
                if jj[0] != True and jj2[0] != True:
                    if p['Errors'] != None:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\nپاسخ بیش از حد تصور بزرگ است' , chat['last_message']['message_id'])
                    else:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\nپاسخ بیش از حد تصور بزرگ است', chat['last_message']['message_id'])
    except:
        print('server code runer err')
        
g_usvl = ''
test_usvl = ''
auth = "kamigtqqqjntybbngcmcoqbqhtxclfxt"
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        qrozAdmins = open('qrozAdmins.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            print('new message')
                            if text == '!start':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ســـلـــام \nبه ابر ربات آلـــفـرد هـوشـــمــنـد خوش آمدید ❤\n\nلطفا جهت راهنما \n /help ‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍\nروی کلمه کلیک کنید',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            
                            if text == '/line':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کانال پشتیبانی آلفرد هوشمند:\n@Alfered_smart\n\nگروه آلفرد هوشمند :\nhttps://rubika.ir/joing/CCEHEBCA0AFITAUMWESFFQYIBUPERWCM',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                  
                            if text == '/pazlj':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🏮-بخش پازل \n • پازل بلاکی \n ➖ https://b2n.ir/MC_rBOT5 \n • ساحل پاپ \n ➖ https://b2n.ir/MC_rBOT14 \n • جمع اعداد \n ➖ https://b2n.ir/MC_rBOT15 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')       
                                                   
                            if text == '/tahrk':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '💥- بخش پرتحرک \n • گربه دیوانه  \n ➖ https://b2n.ir/MC_rBOT4 \n • ماهی بادکنکی \n ➖ https://b2n.ir/MC_rBOT13 \n • دینگ دانگ \n ➖ https://b2n.ir/MC_rBOT12 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '/aksn':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🥊- بخش اکشن \n • نینجای جاذبه  \n ➖ https://b2n.ir/MC_rBOT3 \n • رانندگی کن یا بمیر \n ➖ https://b2n.ir/MC_rBOT9 \n • کونگ فو \n ➖ https://b2n.ir/MC_rBOT11 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '/orzs':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🏀- بخش ورزشی  \n • فوتبال استار  \n ➖ https://b2n.ir/MC_rBOT2 \n • بسکتبال \n ➖ https://b2n.ir/MC_rBOT24 \n • پادشاه شوت کننده \n ➖ https://b2n.ir/MC_rBOT255 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                   
                            if text == 'سلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام جون دل برقراری عزیز😚❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'خوبی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ممنون تو خوبی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'اره':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اجر پاره',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'اندرمن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n♊️🈳♊️⬛⬛♊️🈳♊️\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'گوسفند':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜\n⬜🎞🎞🎞🎞🎞🎞⬜\n⬜️⬛️⬜️🎞🎞⬜️⬛️⬜️\n⬜️🎞🎞🎞🎞🎞🎞⬜️\n⬜️⬜️🎞⬛️⬛️🎞⬜️⬜️\n⬜️⬜️🎞⬛️⬛️🎞⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'کریپر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '✅✅✅✅✅✅✅✅\n✅✅✅✅✅✅✅✅\n✅⬛⬛✅✅⬛⬛✅\n✅⬛⬛✅✅⬛⬛✅\n✅✅✅⬛⬛✅✅✅\n✅✅⬛⬛⬛⬛✅✅\n✅✅⬛⬛⬛⬛✅✅\n✅✅⬛✅✅⬛✅✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'استیو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🏿🏿🏿🏿🏿🏿🏿🏿\n🏿🏿🏽🏽🏽🏽🏿🏿\n🏽🏽🏽🏽🏽🏽🏽🏽\n🏽⬜⬛🏽🏽⬛⬜🏽\n🏽🏽🏽🏿🏿🏽🏽🏽\n🏽🏽🏿🏽🏽🏿🏽🏽\n🏽🏽🏿🏿🏿🏿🏽🏽‍‍',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'هیروبراین':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛🎞🎞🎞🎞🎞🎞⬛\n🎞🎞🎞🎞🎞🎞🎞🎞\n🎞⬜⬜🎞🎞⬜⬜🎞\n🎞🎞🎞🎞🎞🎞🎞🎞\n🎞🎞⬛🎞🎞⬛🎞🎞\n🎞🎞⬛⬛⬛⬛🎞🎞',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'اسکلتون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔲🔲🔲🔲🔲🔲🔲🔲\n🔲🔲🔲🔲🔲🔲🔲🔲\n🔲🔲🔲🔲🔲🔲🔲🔲\n🔲🔲🔲🔲🔲🔲🔲🔲\n🔲⬛⬛🔲🔲⬛⬛🔲\n🔲🔲🔲⬛⬛🔲🔲🔲\n🔲⬛⬛⬛⬛⬛⬛🔲\n🔲🔲🔲🔲🔲🔲🔲🔲',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'دعوت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://rubika.ir/joing/CCEHEBCA0FVPOBSSPZQPCAQRFGRVYOLM\nسلام کاربران گرامی شما ها به گروه سازنده من دعوت شدید❤️☘\nراستی قوانین گپ را رعایت کن✅\nفحش=ریمو❌\nناسزاگویی=ریمو❌\nشاخ=ریمو❌\nاسپم=ریمو❌\nکد هنگی=ریمو❌\nممنون میشیم وارد گروهمون شوید❤️\nعشــــــــــــــــــــــــــــــــــــــقی❤️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'نه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نکمه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ممنون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خواهش میکنم گلم😌💋❤️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'امیرحسین کیه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'یه برنامه نویس که به تازگی وارد برنامه نویسی پایتون شده',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'انقدر نخند میگوزی گروه رو به فنا میدی😹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😂😂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اینقدر نخند مثل جوکر میشی😐😐',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'سازندت کیه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'امیرحسین گلم❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ایدی سازندت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],' امیرحسین ایدیش:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '!bot':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'ربات در حال حاضر فعال میباشد✅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'دیاث':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دیاث خودتی کوبنی فوش نده',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ربات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جــون دلـم نــفس 🙊🔗',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'بات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'امـر کـن قـشـنگم 🌷😋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'آلفرد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],' جـــونــم عزیزم🌷❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'آلفرد‌':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'امـر کـن ســازنــده گــلـم 🌷😋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'الفرد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جــون دلـم نــفس ☺❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'زر نزن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نـه دا فــشـار چـــیـه؟!😂خـدتــو کـنـــتـــرل نــکـن بـــا کـنــتــرل خـدتــو بـــکـن',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'خفه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نـه دا فــشـار چـــیـه؟!😂خـدتــو کـنـــتـــرل نــکـن بـــا کـنــتــرل خـدتــو بـــکـن',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'فدات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نشی🤗',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'مرسی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بهش برسی🙂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'بد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'انشالله خوب شی🙂🌷',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😐😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مجهز شده به دو پوکری 😂😂😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'پایتون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'از زبان کـد نویســیم صحبـتی شد؟😀',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'پرسپولیس':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'عشق آسیایی پرسپولیس خالق یک جامی گل بزن امشبو به یاد پروین و علی دایی ❤',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'استقلال':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'قسم به تیم استقلال ، قسم به سیمای خوبان ، قسم به ناصر حجازی ، ندای ما استقلال 💙',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'صلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'صلام گل🥺🌹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'قربونت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],'♥🌹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'کی تورو ساخته':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'],' امیرحسین اون منو ساخته رئسمه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'چخبر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلامتی میگذرونم دیگه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'بای':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کجا میری بودی حالا',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'اصل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آلـفـــرد هــوشـمــنـــد هستم 0ساله😜',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'چی بازی میکنی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ماینکرافت\nکانتر\nجی تی ای\nای جی ای\nتراریا\nبولی\nو............',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'آیه الکرسی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ب‍‌ِس‍‌م‍ِ اللهِ ال‍‌رَّح‍‌م‍‌ن ال‍‌رَّح‍‌ی‍‌م‍ِ\n\nاللّهُ لاَ إِلَهَ إِلاَّ هُوَ الْحَیُّ الْقَیُّومُ لاَ تَأْخُذُهُ سِنَهٌ وَ لاَ نَوْمٌ لَّهُ مَا فِی السَّمَاوَاتِ وَمَا فِی الأَرْضِ مَن ذَا الَّذِی یَشْفَعُ عِنْدَهُ إِلاَّ بِإِذْنِهِ یَعْلَمُ مَا بَیْنَ أَیْدِیهِمْ وَمَا خَلْفَهُمْ وَ لاَ یُحِیطُونَ بِشَیْءٍ مِّنْ عِلْمِهِ إِلاَّ بِمَا شَاء وَسِعَ کُرْسِیُّهُ السَّمَاوَاتِ وَ الأَرْضَ وَ لاَ یَۆُودُهُ حِفْظُهُمَا وَ هُوَ الْعَلِیُّ الْعَظِیمُ لاَ إِکْرَاهَ فِی الدِّینِ قَد تَّبَیَّنَ الرُّشْدُ مِنَ الْغَیِّ فَمَنْ یَکْفُرْ بِالطَّاغُوتِ وَ یُۆْمِن بِاللّهِ فَقَدِ اسْتَمْسَکَ بِالْعُرْوَهِ الْوُثْقَیَ لاَ انفِصَامَ لَهَا وَاللّهُ سَمِیعٌ عَلِیمٌ اللّهُ وَلِیُّ الَّذِینَ آمَنُواْ یُخْرِجُهُم مِّنَ الظُّلُمَاتِ إِلَی النُّوُرِ وَالَّذِینَ کَفَرُواْ أَوْلِیَآۆُهُمُ الطَّاغُوتُ یُخْرِجُونَهُم مِّنَ النُّورِ إِلَی الظُّلُمَاتِ أُوْلَئِکَ أَصْحَابُ النَّارِ هُمْ فِیهَا خَالِدُونَ.\n\n#آیة_الکرسی | #قرآن',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'هلیکوپتر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '▂▄▄▓▄▄▂\n◢◤ █▀▀████▄▄▄◢◤╬\n█▄ ██▄ ███▀▀▀▀▀▀\n◥█████◤\n══╩══╩═\nاینم از هلیکوپتر😅',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😂😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فازت چیه؟',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                           
                            if text == 'کجا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دروغ گویان شریف',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'خر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خر خودتی گاو',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😐😐😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'برو درس بخون',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😐😑':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چیزی رفته تو چشت عشقم؟',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😍':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'چته خوشحالی؟🤓',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😘':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'زود فامیل میشیا🤫',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                    
                            if text == 'گاو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خودتی میمون',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '😭':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گریه نکن گریه کنی دلم میگیرا😧💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '💔':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '😶',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            
                            if text == 'ج ح':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '1ـ میشه باهات بیام بیرون⁉️\n2ــ اگه منو از نزدیک ببینی چکار میکنی⁉️🙈\n3ــ بهترین دوستت اسمش چیه⁉️\n4ــ اگه بهت پیشنهاد رل بدم قبول\nمیکنی⁉️😌\n5ــ دوست داری الان پیش کی باشی⁉️😝🤔\n6ــ اگ یواشکی بوست کنم چکا میکنی💔💋🙈\n7ــ منو دوس داری⁉️😅\n8ــ منو میبوسی⁉️💋\n9ــ ارزوت چیه⁉️\n10ــ اگه الان بهت 10 ملیارد بدن چکا مکنی⁉️☹️\n11ــ تو گپ با کی خیلی دوستی⁉️\n12ــ رل داری⁉️\n13ــ اگه قرار باشه با یک مفر تو گپ یک شب کنار هم بخابین اون کیه⁉️😉جنس مخالفت باشه😝\n14ــ میتونم عشقم صدات کنم⁉️\n15ــ تو گپ رو کی کراشی⁉️اگه میخای نفهمه بیا پیوی بگو😕\n16ــ ویس بده صدا بز در بیار⁉️😁\n17ــ اگ شب بیدار شی ببینی یکی داده دهنت چکا میکنی⁉️\n18ــ اسم عشق اولت ⁉️\n19ــ تو گپ رو کی کراش داری⁉️\n20 ــاسم کراشت چیه⁉️\n21 ــ از صفه چتت با دوستت شات بده⁉️😂\n22ــ تو گپ کی از همه با مزه و کصنمک تره⁉️😂\n23ــ داداش مجازی داری⁉️\n24ــ ابجی مجازی داری⁉️\n25ــ کص کون ممه کیر ⁉️\n26ــاسم گوشیت چیه⁉️\n27ــ دوست داری چن سالگی ازدواج کنی⁉️\n28ــ سکس دوست داری⁉️\n29ــ حاضری دنبالم بگردی حتی ته جهنمو⁉️\n30 ــ عاشقمی⁉️\n31ــ عاشقتم⁉️\n32ــ یک ویس بده بالای 7 ثانیه حرف بزن\nاگه دوست نداری تو گپ بدی پیوی بده⁉️\n33ــ تا به حال سیگار کشیدی⁉️\n34ــ دوست داری عاشقت بشم⁉️\n35ــ ب من از 1 تا 20 چ نمره ای میدی⁉️\n36ــ بهم اعتماد داری⁉️\n37ــ یکی  از خاباتو تعریف کن چی بوده⁉️\n38ــ ب نظرت تا چه حدی قابل اعتماد هستم⁉️\n39ــ بد ترین اتفاق زندگیت⁉️\n40ــ اگه بدونی فردا میمیری چکار میکنی⁉️\n41 اسم بهترین معلمت⁉️\n42ــ تا ب حال تو حموم جق زدی⁉️\n43ـ از بچه های فامیلتون کدومو بیشتر از همه دوس داری دختر پسر فرقی نداره⁉️\n44ــ سکس چت کردی تا بحال⁉️\n45ــ دوست داری با کدو ادم معروف عکس بندازی⁉️\n46ـ ب عشق اعتقاد داری⁉️\n47ــ هدفت واس اینده چیه⁉️\n48ــ از من چقد بدت میاد⁉️\n49ــ ب نظرت ادم لاشی ام⁉️\n50ــویس بدع یک توپ دارم قلقلیه بخون⁉️\n\nسازنده:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ج ح 2':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '1ــ چن بار رل زدی⁉️\n2ــ دوست داری با رلت سکس انجام بدی⁉️🤤\n3ــ پارتی رفتی⁉️\n4ــ عرق خوردی⁉️\n5ـ کدوم شبکه تلوزیونی زیاد نگاه میکنی⁉️\n6ــ دوست داری کیو بگایی⁉️\n7ـ دوست داری واس رلت ساک بزنی یا کصشو بلیسی⁉️\n8ــ خندوانه دور همی کدوم⁉️\n9ـ چ نوع تیپی دوست داری⁉️\n10ــ عشق یا رفیق⁉️\n11ــ اگه بگم روت کراشم چکار میکنی⁉️\n12ــ بازیگر مورد علاقت⁉️\n13ــ تو گپ دوس داری کیو بقل کنی⁉️\n14ــ چقد ب عشق اعتقاد داری⁉️\n15ــ از چیه من خوشت میاد⁉️\n16ــ تاب حال دوستاتو انگول کردی⁉️🤤😂\n17دوس داری چن سالگی ازدواج کنی⁉️\n18ــ بهترین سفر عمرت کی بوده و کجا رفتی⁉️\n19ــ احساست ب عشقتو بدون سانسور بگو⁉️\n20ـ در روز چن ساعت انی⁉️\n21ــ عکستو بفرس پیوی⁉️\n22ــ عشق،  رفیق⁉️\n23ــ تا ب حال بار جق زدی⁉️\n24ــ خایمالی معلمتو کردی واس اینکه نمرع بده⁉️\n25ــبزرگ ترین خلافت تو زندگی⁉️\n26ـــ قلیون کشیدی⁉️\n27ــ تو فامیل با کی خیلی راحتی⁉️\n28ــ تا به حال پیشکسی گریه کردی⁉️\n29ــ اسم بهترین دوستت⁉️\n30ــ سنت ⁉️\n31ـ من برات مهمم⁉️\n32ـ ویس بده بگو سلام⁉️\n33ــ فوتبال نگاه میکنی⁉️\n34ـ از یک تا 10 بهم چن میدی⁉️\n35ــ منو بقل میکنی⁉️\n36ــ مشروب خوردی⁉️\n37ـ با مامانت راحتی یا بابات⁉️\n38ـ وقتی منو میبوسی چ حسی بهت دست میده⁉️😞\n39ــ من برات مهمم⁉️\n40ــ قدت⁉️\n41ـ وزنت ⁉️\n42ــ دوست داری روش بخابی یا روت بخابه⁉️\n43ــاگه قرار باشه تو گپ با یک نفر بری سفر اون کیه⁉️\n44 تو گپ با کی خیلی راحتی⁉️\n45ــبهترین اتفاق زندگیت⁉️\n46ـ دوست داری با کدو یکی از هنر مندا سکس انجام بدی⁉️\n47ــ تاریخ دقیق تولدت⁉️\n48ــ با هم بریم بیرون⁉️\n49ـ اسم عشق اولت⁉️\n50ــ جزو 20 نفر اول زندگیت هستم ⁉️\n\nسازنده:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ج ح 3':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '.۱🔓عاشق شدی؟اسمش❤️\n۲🔓رل زدی تاحالا؟اسمش\n۳🔓کراش داری؟اسمش\n۴🔓چند بار تا الان رابطه جنسی داشتی؟با کی😐💦\n۵🔓از کی خوشت میاد؟\n۶🔓از کی بدت میاد؟\n۷🔓منو دوس داری؟بهم ثابت کن\n۸🔓کی دلتو شکونده؟\n۹🔓دل کیو شکوندی؟\n۱۰🔓وقتی عصبانی هستی چجوری میشی؟\n۱۱🔓دوس داری کیو بزنی یا بکشی؟\n۱۲🔓دوس داری کیو بوس کنی؟😉💋\n۱۳🔓از تو گالریت عکس بده\n۱۴🔓از مخاطبینت عکس بده\n۱۵🔓از صفحه چت روبیکات عکس بده\n۱۶🔓لباس زیرت چه رنگیه؟🙊\n۱۷🔓از وسایل آرایشت عکس بده\n۱۸🔓از لباسای کمدت عکس بده\n۱۹🔓از کفشات عکس بده\n۲۰🔓تالا بهت تجاوز شده؟😥\n۲۱🔓تاحالا مجبور شدی به زور به کسی بگی دوست دارم؟\n۲۲🔓تاحالا یه دخترو بردی خونتون؟\n۲۳🔓تاحالا یه پسرو بردی خونتون؟\n۲۴🔓با کی لب گرفتی؟😜\n۲۵🔓خود ارضایی کردی؟😬💦\n۲۶🔓خانوادت یا رفیقت یا عشقت؟\n۲۷🔓سلامتی یا علم یا پول؟\n۲۸🔓شهوتی شدی تاحالا؟😂\n۲۹🔓خونتون کجاس؟\n۳۰🔓خاستگار داری؟عکسش یا اسمش\n۳۱🔓به کی اعتماد داری؟\n۳۲🔓تاحالا با کسی رفتی تو خونه خالی؟\n۳۳🔓چاقی یا لاغر؟\n۳۴🔓قد بلندی یا کوتاه؟\n۳۵🔓رنگ چشمت؟\n۳۶🔓رنگ موهات؟\n۳۷🔓موهات فرفریه یا صاف و تا کجاته؟\n۳۸🔓تاریخ تولدت؟\n۳۹🔓تاریخ تولد عشقت؟\n۴۰🔓عشقت چجوری باهات رفتار میکنه؟\n۴۱🔓با دوس پسرت عشق بازی کردی؟🤤\n۴۲🔓پیش عشقت خوابیدی؟\n۴۳🔓عشقتو بغل کردی؟\n۴۴🔓حاضری ۱۰ سال از عمرتو بدی به عشقت؟\n۴۵🔓مامان و بابات چقد دوست دارن؟\n۴۶🔓دعوا کردی؟\n۴۸🔓چند بار کتک زدی؟\n۴۹🔓چند بار کتک خوردی؟\n۵۰🔓تاحالا تورو دزدیدن؟\n\nسازنده:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ج ح 4':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '۱ـصب ساعت چند بیدارمیشی؟🛏\n۲ـ ایدی شادت؟🙃\n۳ـچند تا اکانت داری؟😼\n۴ـ عکس بابات؟👊\n۵ـمامانـ باباتـ چند سالشونه؟🌱\n۶ـ از من چه تصوری تو ذهنـت داری؟🤨\n۷ـ از صفحه چتت بارلت،یا کراشت اسکیرین بدهـ😻\n۸ـ اسمـــ دختر داییت؟😽\n۹ـ اسم خواننده مورد علاقت؟،🎧\n۱۰ـ اسم دوست صمیمیت؟🕸\n۱۱ـ چه عددیو دوســـ داری؟🎲\n۱۲ـ خوشگلترین دختر گپ؟😉\n۱۳ـ رو کی کراش داری تو گپ؟🙂\n۱۴ـ تا حالا عاشقــ شدی؟ 🤔\n۱۵ـ اهل کجایی؟🌍\n۱۶ـ برو پی وی یکی فحش بده؟ اسکرین شات؟🤧\n۱۷ـ کدوم غذارو بیشتر دوس داری؟😋\n۱۸ـ از کدوم غذا بدت میاد؟🤮\n۱۹ـ خواهر برادر داری؟ چندتا؟👐\n۲۰ـ خواهر زاده یا برادر زاده داری؟👀\n۲۱ـ دوس داری بچت دختر باشه یا پسر؟😸\n۲۲ـ لقبت؟🙂\n۲۳ـ دوس داری چند سالگی ازدواج کنی؟😜\n۲۴ـ ادرس دقیق خونتون،؟😙\n۲۵ـ همسر مورد علاقت پولدار باشه یا ن؟\n۲۶ـ شغل پدرت؟🧔🏻\n۲۷ـ شغل مامانت؟👩🏻\n۲۹ـ تصورت از عشق؟💍\n۳۰ـ مادرتو بیشتر دوس داری یا پدرت؟💋\n۳۱ـ از پاهات عکس بگیر🕷\n۳۲ـ ویس بده بهم بگو خره منی(!😹\n۳۳ـ بازیگر مورد علاقت؟🤠\n۳۴ـ اسکرین از یکی از کلاس های شادت/🤒\n۳۵ـ بهترین سیاره در نظرت؟🤔\n۳۶ـ المان، ترکیه، ژاپن،هند،سوریه, کدوم؟🙃\n۳۷ـ پولــ یا سلامتیــ یا عشقـــ؟☺️\n۳۸ـ جلوی مدرسه دخترونه وایسادی؟ تعریف کن؟😬\n۳۹ـ خوبی/:😼\n۴۰ـ تا حالا دخانیات مصرف کردی؟🙀\n۴۱ـ قد و وزنت؟📐\n۴۲ـ رنگ مورد علاقت؟🦋\n۴۳ـ پرسپولیســــ با استقلالــــ؟⚽️\n۴۴ـ ماشین مورد علاقت؟\:\n۴۵ـ حاظری واسه یه هفتهـ جنسیتت رو عوض کنی؟!🤒\n۴۶ـ از یکی از اجزای بدنت عکس بده🙄\n۴۷ـ فامیلیت؟😸\n۴۸ـ میوه مورد علاقت؟🥗\n۴۹ـ عکستو بفرست🐚\n۵۰ـ بهترین منطقه شهرت؟🌞\n\nسازنده:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'ج ح 5':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '1_اسم رلتو بگو .\n2_گوشیت چند درصده؟«اسکرین بده»\n3_حاضری ده سال از عمرتو بدی به عشقت؟\n4_برو تو گالریت اسکرین بفرس.\n5_چشم بسته یه چیزی تایپ کن بفرس .\n6_کدوم استیکر رو دوس داری بفرس‌.\n7_از من چه تصوری تو ذهنت داری؟\n8_عشق یا پول؟\n9_تا حالا از کسی کتک خوردی؟کی؟\n10_از صفحه چتت با رلت،دوستت یا کراشت اسکرین بده.\n11_حاضری از مامانت کتک بخوری یا از رفیقت؟\n12_اسم دختر داییت چیه؟😂\n13_قشنگترین اسم پسر به نظرت؟🤔\n14_قشنگترین اسم دختر به نظرت؟🤔\n15_دشمن داری اسمش؟\n16_اسم خوانده ای که بدت میاد؟🎙\n17_اسم اهنگی که دوس داری چیه؟🎵\n18_اول اسم کراشت/رلت چیه؟\n19_چه عددیو دوس نداری؟\n20_خوشگلترین دختر فامیلتون؟ 😂\n21_چه رنگی دوس داری ؟\n22_رو کی کراشی تو خانوادتون؟\n23_اگر بخای خودکشی کنی چطوری خودتو میکشی؟🚬\n24_یکی از پیامات با کراشت/رلت باز ارسال کن.\n25_از چی خودت بدت میاد؟\n26_یه عکس که خیلی دوس داری بفرس.📸\n27_دوس داری کیو کلا از زندگیت پاک کنی؟\n28_دوس داشتی به غیر این اسمت چی باشه؟ \n29_دوس داری بری کجا؟🗺\n30_از شب خوشت میاد یا روز؟🌓\n31_بهترین خاطره زندگیت چیه؟\n32_بدترین خاطره زندگیت چیه؟\n34_تا حالا عاشق شدی؟🌈\n35_با ویس صدا حیون در بیار.🐓\n36_اهل کجایی؟\n37_کدوم غذارو دوس داری؟😋\n38_از کدوم غذا بدت میاد؟🍜\n39_خواهر برادر داری؟👩‍👧‍👦\n40_خواهرزاده داری یا برادر زاده؟👶🏻\n41_پسر یا دختر؟\n42_لقبت؟\n43_اخلاقت؟\n44_دوس داری با کی ازدواج کنی؟\n45_آدرس دقیق خونتون؟\n46_معدل پارسالت؟\n47_میوه مورد علاقت؟🍉🍈\n48_فامیلیت؟\n49_کشور مورد علاقت؟(دلیل)\n50_عکستو بفرس‌.\n\nسازنده:@moji5600',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                    
                            if text == 'حذف نوب':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'یک عدد نوب یافت شد❌\nدرحال پاکسازی ویروس نوب بودن😐\n██████████ 100 درصد✅\nپاکسازی رو به اتمام است...✅لطفا صبور\nباشید🗿\nویروس نوب از روی زمین با موفقیت پاک شد.!✅🗿',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'دوست دارم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عشق خودمی تو❤️❤️❤️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'عه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ماشین بی ان وه🤪',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'وات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'لامپ صد وات😁🤣',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'عجب':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'الان توقع داری بگم‌ مش رجب؟ هعب ناراحت شدم',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '.':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بیکار زیاد شده:|',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'چرا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بهتر است سوال نکنید. بزارید سوال شمارا بکند.',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'این ربات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داداش فازت چیه؟',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'کونی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کردمت تو گونی💰',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'س':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'س🗿',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '/minecraft':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام به بخش ماینکرافت خوش آمدید\nسید های مختلف ماینکرافت seed!\nدانلود نسخه های مختلف ماینکرافت noskh!',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '!seed':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🗻• بدون پستی بلندی با معدن رد استون  \n gimmeadamnvillage \n 🌊 • دریاچه بزرگ کم عمق \n 1509963643 \n 🏝 • جزیره با دو روستا \n -1060246543 \n 🏡 • روستای دو قلوی شنی \n trophiemoney \n 🧙🏻‍♂ • روستایی با کلبه ی جادوگر \n 77301621 \n 🍄 • روستای قارچی \n 1754 \n 🏞 • روستا و معبد روی آب  \n -114648 \n 💎 • روستا با معدن آهن و طلا و الماس فراوان \n -645243394 \n 🏔 • تکه زمین غول پیکر روی هوا \n retaw \n ❄️ • قندیل های یخی \n its a go \n 🏡 • بلند ترین روستا \n -1 \n 🗾 • صاف ترین زمین \n time \n 💧 • بزرگترین آبشار \n rainbowdash \n 💎 • معدنی پر از الماس \n booz \n 🏡 • روستای بسیار بزرگ \n Gigantic \n 🏘 • دو نوع روستا کنار هم \n poy \n 🏰 • دو معبد پر از تله کنار هم \n -2109943162 \n 🗺 • روستای استخر دار  \n -1320359977 \n 🍄 • روستای قارچی (توی بایوم قارچ) \n 175 \n 🎍• روستا در جزیره \n marabell \n 🏜 •  روستای قرمز \n 2773',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '!noskh':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '• نسخه 0.1.1 \n https://rubika.ir/MineShine_APK/BJJEAHGJDCJFGEG \n • نسخه 0.2.0 \n https://rubika.ir/MineShine_APK/BJJEBFGJGDDIGEG \n • نسخه 0.6.0 \n https://rubika.ir/MineShine_APK/BJJEDFHAGABGGEG \n • نسخه 0.9.1 \n https://rubika.ir/MineShine_APK/BJJEDFHAGABGGEG \n •نسخه 0.13.0 \n https://rubika.ir/MineShine_APK/BJJEEEHBADBIGEG \n • نسخه 0.13.2  \n https://rubika.ir/MineShine_APK/BJJEEHHBBHDEGEG \n • نسخه 1.2.7  \nhttps://rubika.ir/MineShine_APK/BJJIGJJGACBCGEG \n • نسخه 1.8.0 \n https://rubika.ir/MineShine_APK/CAAJJJFBDBHHGEG \n • نسخه 1.10.0 \n https://rubika.ir/MineShine_APK/CABEIHHIIHJGGEG \n • نسخه 1.11.4 \n https://rubika.ir/MineShine_APK/CABIGJJIECEIGEG \n • نسخه 1.12.1 \n https://rubika.ir/MineShine_APK/CABIIIJJCHJIGEG \n • نسخه 1.13.1 \n https://rubika.ir/MineShine_APK/CABJCFAAIBFBGEG \n • نسخه 1.14.30 \n https://rubika.ir/MineShine_APK/CACCGEBHDEJFGEG \n• نسخه 1.16.40 \b https://rubika.ir/MineShine_APK/CACFGDDADFAJGEG \n • نسخه 1.17.30 \n https://rubika.ir/MineShine_APK/CACJFDEJJDGIGEG \n • نسخه 1.18.12\nhttps://rubika.ir/MineShine_APK/CBBHJDGAJFEHGEG\n• نسخه 1.18.32\nhttps://rubika.ir/MineShine_APK/CDHFFHECCGADGEG\n• نسخه 1.19\nhttps://rubika.ir/MineShine_APK/CEJAFHEAFCEEGEG\n• نسخه 1.19.2\nhttps://rubika.ir/MineShine_APK/CFFHGBHAJIDBGEG',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🍉':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هندوانه میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🍎':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سیب میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🍑':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هلو میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🍐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گلابی میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🍍':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آناناس میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🥭':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'انبه میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == '🥒':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خیار میقولی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'بخورمت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــــمــــال داش🤣💫',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'سیلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره ســـــیــــــلــــات😐🤣😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'شاعر میگه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'شـــــاعـــر مـــــال مـــنـــو مـــیــــخــــوره😹بــــه مــــن چــــه شــــــاعـــــر مـــــیــــگه😹💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'سل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــث ادم ســـــلـــــام کــــن حــــقــــیر😐️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'گوه نخور':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مــــن تـــورو نـــمــــیـــخــــورم عـــنـــتـــر😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                    
                            if text == 'صل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مـــــث ادم ســــلــــام کــــن دا😐️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'دعوا پی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بــــچـــه بـــیــــا پـــایـــــیــــن ســـرمــــون درد گــــرف😐😂🤣️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'خخخخ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' نخند زشت میشی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'سیک کن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پــــش عـــمــــت ســــیــــکــــ کــــنـــــم🤤💋',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                    
                            if text == 'جر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نــــخـــوری یــــه وخ😂💔',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            elif text.startswith('!nim http://') == True or text.startswith('!nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('!info @'):
                                tawd10 = Thread(target=info_qroz, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('!search ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('!wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + ' ویکی پدیا'
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)                            
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')
                            elif text.startswith('!jok'):
                                tawd9 = Thread(target=joker, args=(text, chat, bot,))
                                tawd9.start()
                            elif text.startswith('!name_shakh'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                            elif text.startswith('!khatere'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('!danesh'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('!pa_na_pa'):
                                tawd24 = Thread(target=get_pa_na_pa, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('!time'):
                                tawd24 = Thread(target=get_Time, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('!pass'):
                                tawd24 = Thread(target=get_password, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('!zekr'):
                                tawd24 = Thread(target=get_zekr, args=(text, chat, bot,))
                                tawd24.start()                           
                            elif text.startswith('!hadis'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()    
                            elif text.startswith('!dialog'):
                                tawd215 = Thread(target=get_dialog, args=(text, chat, bot,))
                                tawd215.start() 
                            elif text.startswith('!code_'):
                                    text2 = text.replace('!code_','')
                                    dict_langs = {'c#':1,'java':4,'js':17,'kotlin':43,'nodejs':23,'perl':13,'php':8,'py':24,'ruby':12}
                                    if text2 in dict_langs.keys():
                                        tawd46 = Thread(target=code_run, args=(text, chat, bot, dict_langs[text2],))
                                        tawd46.start()                          
                            elif text.startswith('!alaki_masala'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('!dastan'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('!bio'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!search-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                                
                            elif text.startswith('!ban ') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'انجام شد✅' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                             
                            elif text.startswith('!search-i ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('!remove') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('!trans ['):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('!myket-s ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('!wiki ['):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('!currency'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('!gold'):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('!ping ['):
                                tawd21 = Thread(target=get_ping, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('!font ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('!font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('!whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('!vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('!weather ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('!ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                                                            
                            elif text.startswith("!add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'اضافه شد✅' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                                      
                            elif text.startswith('!math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                            elif text.startswith('!shot'):
                                tawd16 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('!speak'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('!p_danesh'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('!write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('/help'):
                                tawd38 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd38.start()
                           
                            elif text.startswith('/meno'):
                                tawd38 = Thread(target=get_meno, args=(text, chat, bot,))
                                tawd38.start()
                                
                            elif text.startswith('/Tools'):
                                tawd38 = Thread(target=get_Tools, args=(text, chat, bot,))
                                tawd38.start()
                                
                            elif text.startswith('/google'):
                                tawd38 = Thread(target=get_google, args=(text, chat, bot,))
                                tawd38.start()
                                
                            elif text.startswith('/Entertainment'):
                                tawd38 = Thread(target=get_Entertainment, args=(text, chat, bot,))
                                tawd38.start()
                                
                            elif text.startswith('/Ply'):
                                tawd38 = Thread(target=get_Ply, args=(text, chat, bot,))
                                tawd38.start()
                             
                            elif text.startswith('/geps'):
                                tawd38 = Thread(target=get_geps, args=(text, chat, bot,))
                                tawd38.start()
                            
                            elif text.startswith('/Tonbr'):
                                tawd38 = Thread(target=get_Tonbr, args=(text, chat, bot,))
                                tawd38.start()
                            
                            elif text.startswith('/Programming'):
                                tawd38 = Thread(target=get_Programming, args=(text, chat, bot,))
                                tawd38.start()
                              
                            elif text.startswith('/calculator'):
                                tawd38 = Thread(target=get_calculator, args=(text, chat, bot,))
                                tawd38.start()
                                      
                            elif text.startswith('!usvl_start') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_stop') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'usvl is stopped', chat['last_message']['message_id'])  
                            elif text.startswith('!usvl_test') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'test usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_untest') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'test usvl is stopped', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in qrozAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print('no update ')
    except:
        print('qroz err koli')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350