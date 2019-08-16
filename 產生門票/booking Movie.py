import imgkit
from qrcode_generator import QRCodeGenerator

name = input('請輸入姓名：')
seat = input('請輸入座位：')
time = input('請輸入時間：')

QRCodeGenerator(name,time,seat)

htmlDoc = '''<!DOCTYPE html>
<html>
<head>
	<link href="https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="bootstrap.css">
	<meta charset="utf-8">
</head>
<body style="font-family: 'Noto Sans TC', sans-serif;">
	<div class="card border-info bg-ticket" style="width: 18rem;">
  		<img class="card-img-top" alt="..." src="C:\\Users\\Jessie\\Desktop\\NKNU-LineBot\\產生門票\\The Matrix.jpg">
		<div class="card-body">
			<h5 class="card-title text-center">駭客任務 The Matrix</h5>
			<p class="card-text">《駭客任務》是一部1999年的好萊塢科幻電影，由華卓斯基姐妹執導，基努·李維、勞倫斯·菲什伯恩、凱莉·安摩絲及雨果·威明等人主演，並由香港電影界的袁和平擔任武術指導。</p>
		</div>
		<ul class="list-group list-group-flush">
			<li class="list-group-item bg-ticket">持有人：'''+name+'''</li>
			<li class="list-group-item bg-ticket">時間：'''+time+'''</li>
			<li class="list-group-item bg-ticket">座位：'''+seat+'''</li>
		</ul>
		<div class="text-center">
			<img class="card-img-bottom rounded" alt="..." src="C:\\Users\\Jessie\\Desktop\\NKNU-LineBot\\產生門票\\qrcode.png">
		</div>
		<button type="button" class="btn btn-info text-center">立即前往訂票</button>
</div>
</body>
</html>
'''
css = 'bootstrap.css'

config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')

imgkit.from_string(htmlDoc, 'ticket.jpg', config=config,css=css, options={'quality':'100','width':'280','encoding':'UTF-8'})