from PIL import Image, ImageOps
from urllib.request import urlopen
from colorthief import ColorThief
import io

def get_dominant_color(url):
    file_data = urlopen(url)
    f = io.BytesIO(file_data.read())
    color_thief = ColorThief(f)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def image_to_bytes(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return image_bytes.getvalue()

def create_cover(url):
    cover_color = get_dominant_color(url)
    img = Image.open(urlopen(url))
    padded_img = ImageOps.pad(img, (1500, 600), color=cover_color)
    return image_to_bytes(padded_img)

# url = "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1589286085i/48677123.jpg"
# create_cover(url).show()