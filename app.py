from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import currencySearch #幣值查詢
from engine.OWM import OWMLonLatsearch #天氣查詢
from engine.AQI import AQImonitor #空氣品質
from engine.gamma import gammamonitor #輻射值
from engine.SpotifyScrap import scrapSpotify #Spotify隨機音樂

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Okinawa.json',scope)

client = gspread.authorize(creds)

LineBotSheet = client.open('OkinawaLineBot')
usersSheet = LineBotSheet.worksheet('users')

app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('zknqXxugyIjpP1UIPsdERJadGThSBvX7vKru4ksunu+G1qsmhHVxwWYiNBYTwShOflNrjskpaclPKYMKWlFrur8neiGuXTkxvXZvt/Wo5yx/llBQtjvRimSRV6pe9r6HqN9rLnSyIK32UgZLfexVYAdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('209a19c4d186a1651036b90a40f95d1a')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@app.route("/web")
def showWeb():
	return '<h1>Hello Every one</h1>'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	print('執行TextMessage')

	userSend = event.message.text
	userID = event.source.user_id
	try:
		cell = usersSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = usersSheet.cell(cell.row,2).value
	except:
		usersSheet.append_row([userID])
		cell = usersSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = ''

	if userSend == '你好':
		message = TextSendMessage(text='Hello, ' + userID)

	elif userSend == '天氣':
		usersSheet.update_cell(userRow,2,'天氣查詢')
		message = TextSendMessage(text='請傳送你的座標')
	
	#幣值查詢
	elif userSend == '日幣':
		message = TextSendMessage(text=currencySearch('JPY'))
	elif userSend in ['CNY', 'THB', 'SEK', 'USD', 'IDR', 'AUD', 'NZD', 'PHP', 'MYR', 'GBP', 'ZAR', 'CHF', 'VND', 'EUR', 'KRW', 'SGD', 'JPY', 'CAD', 'HKD']:
		message = TextSendMessage(text=currencySearch(userSend))

	#Buttons template
	elif userSend == '國際通':
		message = TemplateSendMessage(
			alt_text='這是一個按鈕選單',
			template=ButtonsTemplate(
				thumbnail_image_url='https://www.japanyokoso.com/pac_dir/spot/2017/L01387_A_01_ypb.jpg',
				title='沖繩國際通',
				text='請選擇動作',
				actions=[
					MessageAction(
						label='美金',
						text='USD'
					),
					MessageAction(
						label='日幣',
						text='JPY'
					),
					MessageAction(
						label='你好',
						text='你好'
					),
					URIAction(
						label='帶我去國際通',
						uri='http://tc.tabirai.net/sightseeing/article/okinawa-kokusaidori-tourist/'
					)
				]
			)
		)
	elif userSend in ['spotify','音樂','music']:
		columnReply,textReply = TemplateSendMessage(
			alt_text=textReply,
			template=ImageCarouselTemplate(
				columns=columnReply
			)
		)
	else:
		message = TextSendMessage(text=userSend) #應聲蟲
		#print('使用者傳的訊息{}:'.format(event.message.text))
		#message = TextSendMessage(text=event.message.text) #應聲蟲
	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
	userID = event.source.user_id

	try:
		cell = usersSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = usersSheet.cell(cell.row,2).value
	except:
		usersSheet.append_row([userID])
		cell = usersSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = ''
	if status == '天氣查詢':
		userAddress = event.message.address
		userLat = event.message.latitude
		userLon = event.message.longitude

		weatherResult = OWMLonLatsearch(userLon,userLat) #天氣查詢
		AQIResult = AQImonitor(userLon,userLat) #空氣品質
		gammaResult = gammamonitor(userLon,userLat) #輻射值
		usersSheet.update_cell(userRow,2,'天氣查詢')
		message = TextSendMessage(text='💨天氣狀況：\n{}\n📣空氣品質：{}\n\n💥輻射值：\n{}'.format(weatherResult,AQIResult,gammaResult))
		#message = TextSendMessage(text='地址：{}\n經度：{}\n緯度：{}'.format(userAddress,userLat,userLon))
	else:
		message = TextSendMessage(text='傳遞地址幹嘛? (請傳送：天氣)')
	line_bot_api.reply_message(event.reply_token, message)

#回覆貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
	print('執行StickerMessage')
	message = TextSendMessage(text='嗚嗚~我看不懂貼圖')
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
