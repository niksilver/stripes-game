from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from gamehelper.card_maker import CardMaker


asset_dir      = 'assets/'

stripe_colours  = [(212,   0, 212),    # Magenta
                   (212, 212,   0),    # Yellow
                   (  0, 192,   0),    # Green
                   ( 96,  96, 255),    # Blue
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
                       file = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                       )
base_maker.font_name('Number', family = 'DejaVu Sans', size = 64)


# Make card images

def card_image(num: int, colours: list[bool]):
    """
    Make a card image with the given number and each stripe present or not.
    """
    maker = base_maker.copy()

    # Create each stripe

    distance_mm = 20

    for idx, include in enumerate(colours):
        if not(include): continue

        height_mm = (idx - 1.5) * distance_mm + (maker.height_mm / 2)
        maker.paste(strip_ims[idx],
                    center = maker.width_mm / 2,
                    middle = height_mm,
                    )

    maker.text(text   = str(num),
               center = maker.width / 2,
               middle = maker.height / 2,
               font   = 'Number',
               )

    return maker.image()


def strip_image(idx: int):
    """
    Make a stripe image for this index.
    """
    thickness_px = int(base_maker.to_px(8))

    im = Image.new(mode = 'RGBA',
                   size = (base_maker.width_with_gutters_px, thickness_px),
                   color = stripe_colours[idx],
                   )
    return im


# Assemble the cards


strip_ims = [strip_image(0),
             strip_image(1),
             strip_image(2),
             strip_image(3),
             ]

card_images = [card_image(2, [True, True, True, True]),
               ]
