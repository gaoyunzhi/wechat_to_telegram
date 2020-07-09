#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
import itchat
from telegram_util import log_on_fail
from common import getFile
import time

tele = Updater(getFile('credential')['bot_token'], use_context=True)
bot = tele.bot
debug_group = bot.get_chat(420074357)
feminism_private_group = bot.get_chat(-428192067)
wechat_feminism_group_name = '女性会客厅'

last_login_time = 0

def sendMsg(name, text):
	users = (itchat.search_friends(name)
		or itchat.search_friends(remarkName = name)
		or itchat.search_friends(nickName = name))
	if not users:
		debug_group.send_message('No user name: %s' % name)
		return
	itchat.send(text, toUserName=users[0]['UserName'])
	debug_group.send_message('success')

def sendToFeminismPrivateGroup(msg):
	print(msg.from_user.firstname)
	if msg.from_user.firstname != 'yunz':
		prefix = 'From ' + msg.from_user.firstname + ': '
	chatroom_id = itchat.search_chatrooms(wechat_feminism_group_name)[0].id
	if msg.text:
		itchat.send(prefix + msg.text, chatroom_id)
		return
	os.system('mkdir tmp2 > /dev/null 2>&1')
	if msg.photo:
		fn = msg.photo[0].get_file().download('tmp2/')
		itchat.send_image(fn, toUserName=chatroom_id) 
		return
	if msg.document:
		fn = document.get_file().download('tmp2/')
		itchat.send_file(fn, toUserName=chatroom_id) 
		return

@log_on_fail(debug_group)
def replyGroup(update, context):
	msg = update.message
	if not msg:
		return
	if msg.chat_id == feminism_private_group.id:
		sendToFeminismPrivateGroup(msg)

@log_on_fail(debug_group)
def reply(update, context):
	msg = update.message
	if not msg:
		return
	if msg.chat_id != debug_group.id or not msg.text:
		return
	r_msg = msg.reply_to_message
	if not r_msg:
		return
	cap = r_msg.text or r_msg.caption
	if not cap:
		return
	name = cap.split(':')[0].lstrip('from').lstrip('to').strip()
	global last_login_time
	if time.time() - last_login_time > 60 * 60:
		itchat.auto_login(enableCmdQR=2, hotReload=True)
		last_login_time = time.time()
	sendMsg(name, msg.text)

tele.dispatcher.add_handler(MessageHandler(Filters.private, reply), group = 3)
tele.dispatcher.add_handler(MessageHandler(Filters.group, replyGroup), group = 4)
tele.start_polling()
tele.idle()