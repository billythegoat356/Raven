from pystyle import Colorate, Colors, System, Center, Write, Anime
from requests import get
from imgsearch import pony

from random import shuffle, randint
from PIL import Image, ImageEnhance
from os import listdir, remove, mkdir
from os.path import isdir, isfile
from shutil import copy




ascii_art = r"""
__________                            
\______   \_____ ___  __ ____   ____  
 |       _/\__  \\  \/ // __ \ /    \ 
 |    |   \ / __ \\   /\  ___/|   |  \
 |____|_  /(____  /\_/  \___  >___|  /
        \/      \/          \/     \/ 
"""[1:]


banner = r'''
  ██                                                    
░░████░░                                                
▒▒  ▒▒████                                            ▒▒
  ██    ██████▒▒                                      ██
    ██████░░▒▒████████▓▓░░                          ▓▓▒▒
  ██  ▒▒████████████████████                ▒▒▓▓░░████▒▒
  ░░████  ██████████████████              ██████████████
      ████████████████████████          ██████████████  
    ▒▒░░  ████████████████████        ██████████████▒▒  
      ████████████████████████░░    ▒▒██████████████    
              ██████████████████    ██████████████      
              ░░██████████████████████████              
                ░░████████████████████████              
                  ██████████████████████████            
                    ▒▒████████████████████████          
                        ██████████████████████░░        
                          ████████████    ██▓▓▒▒        
                        ▒▒██████████        ████        
                        ██████████          ░░▒▒        
                    ▒▒████████    ▒▒                    
                    ██████████  ▓▓░░██░░▒▒              
                      ████████  ▒▒▒▒                    
                      ▒▒████▒▒                          
                      ░░██▓▓                            
                        ██'''[1:]

                

class Raven:

    def __init__(self, text: str) -> None:

    
        self.createdir()

        self.dir = 'raven/'+text

        
        while isdir(self.dir):
            self.dir += str(randint(0, 9))

        mkdir(self.dir)
        wprint(f"Creating directory to stock the files '{self.dir}'...")

        wprint("Searching for images on Google...")
        links = self.search(text=text)

        wprint("Downloading the images...")
        self.files = self.download(links=links)

        wprint("Shuffling the images...")
        shuffle(self.files)

        wprint("Blending every image into another...")
        blended = self.blendall()

        wprint("Deleting the unnecessary images...")
        self.clean()

        wprint("Executing the final image...")
        blended.show()
        return None

    def createdir(self) -> None:
        if not isdir('raven'):
            mkdir('raven')

    def clean(self) -> None:
        for file in self.files:
            remove(file)
        return None

    def search(self, text: str) -> list:
        l = pony(query=text, num_result=100)
        shuffle(l)
        if len(l) >= 5:
            l = l[:5]
        return l
    
    def download(self, links: list) -> list:
        for link in links:
            c = get(link).content
            name = links.index(link)
            if name == 0:
                name = 'font'
            with open(f"{self.dir}/{name}.jpg", 'wb') as f:
                f.write(c)
        return [f"{self.dir}/{links.index(f)}.jpg" for f in links][1:]

    def blendall(self) -> object:
        for file in self.files:
            try:
                x = self.blend(img=file)
            except Exception as e:
                pass
        return x

    def blend(self, img:str) -> object:

        img1 = Image.open(self.dir + '/font.jpg')
        img2 = Image.open(img)

        img1 = self.size(img1)
        img2 = self.size(img2)

        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")


        img = Image.blend(img1, img2, alpha=0.3)
        img = img.convert('RGB')

        bright = ImageEnhance.Brightness(img)
        contrast = ImageEnhance.Contrast(img)
        sharp = ImageEnhance.Sharpness(img)
        color = ImageEnhance.Color(img)


        img = bright.enhance(0.4)
        img = contrast.enhance(1.8)
        img = sharp.enhance(1.5)
        img = color.enhance(1.3)

        self.save(img)

        return img

    def save(self, img: str) -> None:
        return img.save(f"{self.dir}/font.jpg")

    def size(self, img: object, maxw: int = 800, maxh: int = 500) -> object:
        return img.resize((int(maxw/img.size[0]*img.size[0]), int(maxh/img.size[1]*img.size[1])))





def wprint(text: str, color: list = Colors.purple_to_red):
    return Write.Print(text=text + '\n', color=color, interval=0.005)


def init():
    System.Clear()
    System.Size(160, 50)
    System.Title("Raven")

    Anime.Fade(Center.Center(banner), Colors.purple_to_blue,
            Colorate.Vertical, enter=True)


def main():
    System.Clear()

    print("\n"*2)
    print(Colorate.DiagonalBackwards(Colors.purple_to_blue, Center.XCenter(ascii_art)))
    print("\n"*5)

    text = Write.Input("Imagine something... -> ", Colors.purple_to_blue, interval=0.005)
    print('\n')
    wprint(text="Starting generation...", color=Colors.blue_to_purple)
    print()

    try:
        Raven(text=text)
    except Exception as e:
        print('\n')
        Colorate.Error(f"Oops! An error occured: [{e}]")
        return

    print('\n')


    Write.Input("Here you go!", Colors.purple_to_blue, interval=0.005)
    return exit()


if __name__ == '__main__':
    init()
    while True:
        main()
