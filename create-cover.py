from PIL import Image, ImageOps
from urllib.request import urlopen
url = "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1589286085i/48677123.jpg"
img = Image.open(urlopen(url))

ImageOps.contain(img, (600, 600)).show()

# img.show()