from pprint import pprint
import pygame as pg
import easyocr
from gtts import gTTS
from playsound import playsound
from deep_translator import GoogleTranslator


class app:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.root = pg.display.set_mode((864, 816))
        pg.display.set_caption("Pygame App")
        self.root.fill((255, 255, 255))
        self.clock = pg.time.Clock()
        self.running = True
        self.last_tick = pg.time.get_ticks()
        self.reader = easyocr.Reader(['ch_sim'])
        self.cleared = True
        # Rendering glitter
        pg.font.init()
        self.font = pg.font.Font("./Resource/NotoSerifSC-Regular.otf", 64)
        self.cache = "Super Idol的笑容" # Text in memory
        self.rendertext(self.cache, (0, 0), self.font, (0, 0, 0))
    def run(self) -> None:
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[1] > 132:
                    # Draw
                    pg.draw.circle(self.root, (0, 0, 0), pg.mouse.get_pos(), 10)
                    self.last_tick = pg.time.get_ticks()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.root.fill((255, 255, 255))
                        self.cache = self.cache[:-1]
                        self.rendertext(self.cache, (0, 0), self.font, (0, 0, 0))
                    elif event.key == pg.K_SPACE:
                        self.readtext(self.cache)
                    elif event.key == pg.K_RETURN:
                        self.playtext(self.cache)
                        # render text transtlation
                        self.rendertext(self.translate(self.cache), (0, 64), self.font, (0, 0, 0))
                        self.last_tick = pg.time.get_ticks()
                        self.cleared = False
            if pg.time.get_ticks() - self.last_tick > 3000 and not self.cleared:
                self.root.fill((255, 255, 255))
                self.cleared = True
                self.cache = ""
            pg.display.flip()
        pg.quit()                  
    def readtext(self, text: str) -> None:
        # Read and Clear
        rect = pg.Rect(0, 96, 800, 720)
        sub = self.root.subsurface(rect)
        pg.image.save(sub, "./Resource/temp/t.png")
        result = self.reader.readtext("./Resource/temp/t.png")
        pprint(result)
        try: # If there is no text
            text = result[0][1]
            if len(self.cache) > 15 and False: # Feature removed
                self.cache = self.cache[len(self.cache) - 15:] + text
            else:
                self.cache += text
        except IndexError:
            pass
        self.root.fill((255, 255, 255))
        self.rendertext(self.cache, (0, 0), self.font, (0, 0, 0))
        pprint(self.cache)
        self.playtext(self.cache)
        self.last_tick = pg.time.get_ticks()
    def playtext(self, text: str) -> None:
        # Read text
        tts = gTTS(self.cache, lang="zh-CN")
        # Play audio
        tts.save("./Resource/temp/t.mp3")
        # Play audio
        playsound("./Resource/temp/t.mp3")
    def translate(self, text: str) -> str:
        return GoogleTranslator(source='zh-CN', target='en').translate(text)  # output -> Weiter so, du bist großartig
    def rendertext(self, text: str, pos: tuple, font: pg.font.Font, color: tuple) -> None:
        text = font.render(text, True, color)
        self.root.blit(text, pos)
a = app()
a.run()