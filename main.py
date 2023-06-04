#!/home/victor/python_projects/generic/venv/bin/python3

from PIL import Image, ImageDraw, ImageFont
from os import listdir
from os.path import isfile, join
import random
import re
import copy

def get_random_images(dict_images, used_images):
    keys = list(dict_images.keys())
    if len(keys) == len(used_images):

        print('used all images!')
        return True, used_images, 'error'
    while True:
        x = random.choice(keys)
        if dict_images[x]['used']:
            continue
        else:
            dict_images[x]['used'] = True
            img = dict_images[x]['image']
            text = dict_images[x]['text']
            used_images.append(x)
            return img, used_images, text
def reset_imgs_dict(img_dict):
    for k in img_dict.keys():
        img_dict[k]['used'] = False
def set_text_image(image, text, font_size=30):
    draw = ImageDraw.Draw(image)
    arial = ImageFont.truetype("arial.ttf", font_size)

    # get the size of the image
    w,h = image.size
    # get the size of the text
    wt, ht = arial.getsize(text)
    # place the text
    draw.text((w/2, h-ht), text, font=arial, fill="white",stroke_width=2, stroke_fill='black', anchor='mm')
def get_boards(num_boards, img_dir, rows = 4, columns = 4, paper_size_mm = [210, 297] ):
    paper_size_px = [int(paper_size_mm[0]*3.77//1) ,int(paper_size_mm[1]*3.77//1)  ] #convert mm to pixels
    imgs = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]

    # new image sizes for the 'thumbnails'
    length = int(paper_size_px[0]//rows)
    height = int(paper_size_px[1]//columns)

    # create a list of Image instances of all the images.
    pil_imgs = [Image.open(img_dir+'/'+img_name) for img_name in imgs ]

    # resize the images so that they fit perfectly to the paper as value. Also save the text of the filename as key
    imgs_dict = {}
    # regex for getting the name
    regex = ('/([a-zñ_]*).png$')
    for img in pil_imgs:
        name = img.filename
        name = re.findall(regex, name)[0]
        imgs_dict[name] = {}
        imgs_dict[name]['original'] = copy.deepcopy(img)
        imgs_dict[name]['image'] = img.resize((length, height), resample=Image.Resampling.BOX)
        imgs_dict[name]['used'] = False
        imgs_dict[name]['text'] = name.replace('_', ' ')
    # print(imgs_dict)
    # thumbs = [x.resize((length, height), resample=Image.Resampling.BOX) for x in pil_imgs]
    # names = [re.findall(regex,x.filename)[0]for x in pil_imgs]

    # print(names)

    # create an empty canvas to place the images
    canvas = Image.new('RGB', tuple(paper_size_px),color=(255,255,255))

    # list to keep track of the used images so that we dont repeat ourselves in the same sheet
    used_images = []
    # list to save the images to make a singe PDF file
    boards = []
    # populate the canvas with the images and place their names on them
    for i in range(num_boards):
        for row in range(rows):
            for column in range(columns):
                # get the info from a randomly selected image from the dictionary
                x , used_images, text = get_random_images(imgs_dict, used_images)
                # if x == True means that the image has already been used. 
                if x != False and x != True:
                    set_text_image(x, text)
                    canvas.paste(x, (column*length, row*height))
        # set all the images 'used' key to False
        reset_imgs_dict(imgs_dict)
        boards.append(canvas)
        print(imgs_dict)
        # canvas.save('board'+str(i)+'.pdf')
        canvas = Image.new('RGB', tuple(paper_size_px),color=(255,255,255))
        used_images = []
    boards[0].save(f'boards{num_boards}.pdf', save_all=True, append_images=boards[1:])
def get_cards(img_dir, paper_size_mm = [210, 297]):
    paper_size_px = [int(paper_size_mm[0]*3.77//1) ,int(paper_size_mm[1]*3.77//1)  ] #convert mm to pixels
    imgs = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]

    # create a list of Image instances of all the images.
    pil_imgs = [Image.open(img_dir+'/'+img_name) for img_name in imgs ]

    # resize the images so that they fit perfectly to the paper as value. Also save the text of the filename as key
    imgs_dict = {}
    # list of images to convert to PDF
    cards = []
    # regex for getting the name
    regex = ('/([a-zñ_]*).png$')
    for img in pil_imgs:
        name = img.filename
        name = re.findall(regex, name)[0]
        imgs_dict[name] = {}
        imgs_dict[name]['original'] = img.copy()
        imgs_dict[name]['image'] = img.resize(tuple(paper_size_px), resample=Image.Resampling.BOX)
        imgs_dict[name]['text'] = name.replace('_', ' ')
        # imgs_dict[name]['original'].show()
    for img in imgs_dict:
        set_text_image(imgs_dict[img]['image'], imgs_dict[img]['text'], font_size=100)
        print(imgs_dict[img]['original'])
        cards.append(imgs_dict[img]['image'])
    cards[0].save(f'cards.pdf', save_all=True, append_images=cards[1:])

if __name__ == "__main__":
    get_boards(num_boards=30, img_dir='/home/victor/python_projects/generic/bingo/images_animals')
    get_cards(img_dir='/home/victor/python_projects/generic/bingo/images_animals')
