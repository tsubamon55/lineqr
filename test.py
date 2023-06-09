import qrcode
import uuid

img = qrcode.make('hello world')
print(type(img))
png = img.save(f'images/img-{uuid.uuid4()}.png')
