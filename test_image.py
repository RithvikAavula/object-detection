from PIL import Image, ImageDraw
img = Image.new('RGB', (640, 480), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((10,10), "TEST FRAME", fill=(255,255,0))
img.save(r"e:\object detection\test.jpg")
print('Saved test image at e:\\object detection\\test.jpg')
