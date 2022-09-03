enc = open("./secretMessage.enc", "rb")
raw = open("./secretMessage.raw", "wb")

enc_image = bytes(enc.read())
secretMessage = b""
print(enc_image)

width = 500
height = 50
size = width * height

prv_pixel = -1
checked = False
for idx in range(len(enc_image)):
	if checked:
		checked = False
		prv_pixel = -1
		continue
	cnt_pixel = enc_image[idx].to_bytes(1, 'little')
	secretMessage += cnt_pixel
	if idx > 0 and prv_pixel == cnt_pixel:
		count = enc_image[idx+1]
		for num in range(count):
        		secretMessage += cnt_pixel
		checked = True
	prv_pixel = cnt_pixel

print(secretMessage)
print(len(secretMessage))

raw.write(secretMessage)

enc.close()
raw.close()
