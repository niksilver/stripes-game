from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from gamehelper.card_maker import CardMaker


asset_dir      = 'assets/'

stripe_colours  = [(212,   0, 212),    # Magenta
                   (212, 212,   0),    # Yellow
                   (  0, 192,   0),    # Green
                   ]


# Base card

base_maker = CardMaker(width    = 62,
                       height   = 87,
                       unit     = 'mm',
                       width_px = 560,
                       gutter   = 4,
                       )

border_size_mm = 3


# Fonts

base_maker.font_family('DejaVu Sans',
                       file = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                       )
base_maker.font_name('Number', family = 'DejaVu Sans', size = 64)


# Make one card image

def card_image(num: int, cols: list[bool]):
    """
    Make a card image with the given number and each stripe present or not.
    """
    maker = base_maker.copy()

    maker.text(text   = str(num),
               center = maker.width / 2,
               middle = maker.height / 2,
               font   = 'Number',
               )

    return maker.image()


card_images = [card_image(2, []),
               ]
