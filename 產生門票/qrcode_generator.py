import qrcode

def QRCodeGenerator(name,time,seat):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=1,
	)
	qr.add_data('name:{}\ntime:{}\nseat{}'.format(name,time,seat))
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	img.save('qrcode.png')