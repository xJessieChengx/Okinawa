import imgkit
from qrcode_generator import QRCodeGenerator
import cloudinary.upload
import cloudinary

name = input('請輸入姓名：')
seat = input('請輸入座位：')
time = input('請輸入時間：')

def booking(name,time,seat):
	QRCodeGenerator(name, time, seat)
	htmlDoc = '''<!DOCTYPE html>
	<html>
	<head>
		<link href="https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap" rel="stylesheet">
		<link rel="stylesheet" type="text/css" href="bootstrap.css">
		<meta charset="utf-8">
	</head>
	<body style="font-family: 'Noto Sans TC', sans-serif;">
		<div class="card border-info bg-ticket" style="width: 18rem;">
	  		<img class="card-img-top" alt="..." src="C:\\Users\\Jessie\\Desktop\\NKNU-LineBot\\產生門票\\background.png">
			<div class="card-body">
				<h5 class="card-title text-center">Okinawa</h5>
				<p class="card-text">Okinawa is the portal between Japan and the tropics. Learn more about Okinawa and plan your trip.</p>
			</div>
			<ul class="list-group list-group-flush">
				<li class="list-group-item bg-ticket">持有人：'''+name+'''</li>
				<li class="list-group-item bg-ticket">時間：'''+time+'''</li>
				<li class="list-group-item bg-ticket">座位：'''+seat+'''</li>
			</ul>
			<div class="text-center">
				<img class="card-img-bottom rounded" alt="..." src="C:\\Users\\Jessie\\Desktop\\NKNU-LineBot\\產生門票\\qrcode.png">
			</div>
			<button type="button" class="btn btn-info text-center">立即前往規劃</button>
	</div>
	</body>
	</html>
	'''
	css = '/app/engine/bootstrap.css'

	config = imgkit.config(wkhtmltoimage='./bin/wkhtmltoimage')

	imgkit.from_string(htmlDoc, 'ticket.jpg', config=config,css=css, options={'quality':'100','width':'280','encoding':'UTF-8'})

	cloudinary.uploader.upload()