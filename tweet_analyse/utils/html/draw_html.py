from __future__ import absolute_import
import subprocess

from bs4 import BeautifulSoup
from wordcloud import WordCloud


class HtmlDraw:
    def __init__(self):
        self.soup = BeautifulSoup('<div style="position:relative;font-family: monospace;"></div>', 'html5lib')

    def draw_text(self, pos, word, font_size, fill, orientation):
        if orientation: return
        orientation = "transform: rotate(270deg);" if orientation else ""
        span = self.soup.new_tag("span", id=word,
                                 style=f'font-size:{font_size}pt; color:{fill}; position: absolute;'
                                       f' top: {pos[1]}pt; left:{pos[0]}pt;{orientation};transform-origin: left;')
        span.string = str(pos)
        self.soup.div.append(span)

    def show(self, cloud):
        open('test.htm', 'w').write(str(self.soup))
        subprocess.call(('xdg-open', 'test.htm'))
        import matplotlib.pyplot as plt
        plt.figure(figsize=(15, 8))
        plt.axis('off')
        plt.imshow(a, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        img = open('test.png', 'wb')
        plt.savefig(img, bbox_inches='tight', format='png', transparent=True)
        img.close()
        # subprocess.call(('xdg-open', 'test.png'))


if __name__ == '__main__':
    h = HtmlDraw()  # .draw_text((40, 40), "wrfghtfhtord", fill="#00ff22", orientation=Image.ROTATE_90)
    a = WordCloud().generate(open('a.txt').read())
    for (word, count), font_size, position, orientation, color in a.layout_:
        font_size = int(font_size * a.scale)
        pos = (int(position[1] * a.scale),
               int(position[0] * a.scale))
        print(font_size)
        h.draw_text(pos, word, font_size=font_size, fill=color, orientation=orientation)
    h.show(a)
