import qrcode

img = qrcode.make("https://github.com/thanthtooaung-coding")
img.save("qr.png", "PNG")
 