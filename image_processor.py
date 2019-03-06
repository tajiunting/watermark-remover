import urllib.request, urllib.error
import random, os
from PIL import Image, ImageDraw, ImageFont


def file_read(fname, nlines):
    urls = []
    from itertools import islice
    with open(fname, encoding="utf8") as f:
        for line in islice(f, nlines):
            url = line.split()
            if "flickr" in url[1]:
                urls.append(url[1])
    return urls


def download_raw_images(number):
    urls = file_read('fall11_urls.txt', min(10*number, 10000000))
    random.shuffle(urls)
    urls = urls[:number]
    i = 1
    for url in urls:
        try:
            filename = "./raw_images/" + str(i) + ".jpg"
            response = urllib.request.urlopen(url)
            url = response.geturl()
            if "unavailable" not in url:
                urllib.request.urlretrieve(url, filename)
                i += 1
        except urllib.error.HTTPError:
            pass


def resize(path, newpath):
    owd = os.getcwd()
    os.chdir(newpath)
    widepath = os.getcwd()+"/wide"
    tallpath = os.getcwd()+"/tall"
    os.chdir(owd)
    os.chdir(path)
    files = os.listdir('.')
    for file in files:
        im = Image.open(file)
        width, height = im.size
        if width > height >= 300 and width >= 500:
            crop = im.crop((0, 0, 500, 300))
            crop.save(widepath+"/"+file)
        elif width >= 300 and height >= 500:
            crop = im.crop((0, 0, 300, 500))
            crop.save(tallpath + "/" + file)


def watermark_text(input_path, output_path, texts=None, random_pos=False):
    if not texts:
        texts = ["hello world", "watermark remover", "do not copy", "APS360", "University of Toronto", "Watermark"]
    owd = os.getcwd()
    output_path = owd + output_path
    input_path = owd + input_path
    os.chdir(input_path)
    files = os.listdir('.')
    for i, text in enumerate(texts, 1):
        os.chdir(output_path)
        os.mkdir(str(i))
        out = os.getcwd()+"/"+str(i)
        os.chdir(input_path)

        pos = (random.randint(0, 400), random.randint(0, 250))
        font = ImageFont.truetype("arial.ttf", random.randint(20, 40))
        colour = (240, 240, 240, random.randint(100, 200))
        for file in files:
            im = Image.open(file).convert("RGBA")
            txt = Image.new('RGBA', im.size, (255, 255, 255, 0))

            if random_pos:
                pos = (random.randint(0, 350), random.randint(0, 250))

            drawing = ImageDraw.Draw(txt)
            drawing.text(pos, text, fill=colour, font=font)

            combined = Image.alpha_composite(im, txt)
            # combined.show()
            file = file.replace(".jpg", ".png")
            # print(file)
            combined.save(out + "/" + file)


def watermark_with_transparency(input_path, output_path, watermark_path, random_position=False):
    owd = os.getcwd()
    output_path = owd + output_path
    input_path = owd + input_path
    watermark_path = owd + watermark_path
    os.chdir(watermark_path)
    watermarks = [watermark_path+"/"+file for file in os.listdir('.')]
    os.chdir(input_path)
    files = os.listdir('.')

    for i, watermark_path in enumerate(watermarks, 1):
        watermark = Image.open(watermark_path).convert("RGBA")
        width, height = watermark.size
        ratio = 100 / width
        size = (int(width*ratio), int(height*ratio))
        print(size)
        watermark = watermark.resize(size)
        watermask = watermark.convert("L").point(lambda x: min(x, random.randint(100, 200)))
        watermark.putalpha(watermask)

        os.chdir(output_path)
        os.mkdir(str(i))
        out = os.getcwd() + "/" + str(i)
        os.chdir(input_path)
        pos = (random.randint(0, 400), random.randint(0, 200))

        for file in files:
            base_image = Image.open(file).convert("RGBA")
            width, height = base_image.size

            if random_position:
                pos = (random.randint(0, 400), random.randint(0, 200))

            transparent = Image.new('RGBA', (width, height), (255, 255, 255, 128))
            transparent.paste(base_image, (0, 0))
            transparent.paste(watermark, pos, mask=watermark)
            # transparent.show()
            file = file.replace(".jpg", ".png")
            # print(file)
            transparent.save(out + "/" + file)


if __name__ == "__main__":
    # scale_watermarks("./watermarks")
    watermark_with_transparency("./resized_images/wide", "./watermarked_image/diffPos", "./watermarks", random_position=True)
