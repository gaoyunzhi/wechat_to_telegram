#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import itchat
import time
from itchat.content import *
import yaml
from telegram_util import matchKey, log_on_fail

def getFile(name):
	with open(name) as f:
		return yaml.load(f, Loader=yaml.FullLoader)

bot = Updater(getFile('credential')['bot_token'], use_context=True).bot
debug_group = bot.get_chat(-1001198682178)
channel = bot.get_chat('@web_record')
link_status = {}

@log_on_fail(debug_group)
def handle_group(msg):
	if not msg.Url:
		return
	link_status[msg.FileName] = link_status.get(msg.FileName, 0)
	if link_status[msg.FileName] >= 1:
		return # sent before
	if matchKey(msg.User.NickName, ['女权', '平权', 'hardcore', 'dykes']):
		link_status[msg.FileName] += 1
	else:
		link_status[msg.FileName] += 0.5
	if link_status[msg.FileName] >= 1:
		channel.send_message(msg.Url)

@itchat.msg_register(SHARING, isGroupChat=True)
def group(msg):
	handle_group(msg)

@itchat.msg_register([TEXT, SHARING], isFriendChat=True)
def friend(msg):
	# TODO: muted friend don't send
	print(msg)
	debug_group.send_message('%s: %s' % (msg.User.NickName, msg.Url or msg.text))

@itchat.msg_register([PICTURE])
def pic(msg):
	print(msg)
    msg.download(msg.fileName)
    debug_group.send_photo(msg.fileName, cap=msg.User.NickName)
    os.system('rm ' + msg.fileName)

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def file(msg):
	print(msg)
    msg.download(msg.fileName)
    debug_group.send_document(msg.fileName, cap=msg.User.NickName)
    os.system('rm ' + msg.fileName)

itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run(True)