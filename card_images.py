from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from gamehelper.card_maker import CardMaker


stripe_colours = [(212,   0, 212),    # Magenta
                  (212, 212,   0),    # Yellow
                  (  0, 192,   0),    # Green
                  ( 96,  96, 255),    # Blue
                  ]
COL_COUNT      = len(stripe_colours)


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
base_maker.font_name('Number', family = 'DejaVu Sans', size = 48)


# Make cards and their images

def card(num: int, colours: list[bool]) -> CardMaker:
    """
    Make a card image with the given number and each stripe present or not.
    """
    maker = base_maker.copy()

    # Create each stripe

    distance_mm = 12

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

    return maker


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


def one_stripe_cards(count_of_each: int) -> list[Image]:
    """
    Return a list of images of one-stripe cards.
    """
    ims = []

    # Create one image of each card

    for col in range(0, COL_COUNT):
        cols = [(i == col) for i in range(0, COL_COUNT)]
        crd  = card(4, cols)
        im   = add_corners(crd).image()
        ims.append(im)

    return ims * count_of_each


def two_stripe_cards(count_of_each: int) -> list[Image]:
    """
    Return a list of images of two-stripe cards.
    """
    ims = []

    # Create one image of each card

    for col1 in range(0, COL_COUNT - 1):
        for col2 in range(col1 + 1, COL_COUNT):
            cols = [(i == col1 or i == col2) for i in range(0, COL_COUNT)]
            crd  = card(2, cols)
            im   = add_corners(crd).image()
            ims.append(im)

    return ims * count_of_each


def three_stripe_cards(count_of_each: int) -> list[Image]:
    """
    Return a list of images of three-stripe cards.
    """
    ims = []

    # Create one image of each card

    for col in range(0, COL_COUNT):
        cols = [(i != col) for i in range(0, COL_COUNT)]
        crd  = card(1, cols)
        im   = add_corners(crd).image()
        ims.append(im)

    return ims * count_of_each


def four_stripe_cards(count_of_each: int) -> list[Image]:
    """
    Return a list of images of four-stripe cards.
    """

    # Create the iamge

    crd = card(-1, [True] * COL_COUNT)
    im  = add_corners(crd).image()

    return [im] * count_of_each


def add_corners(card: CardMaker) -> CardMaker:
    """
    Take a card and add into the top corners a smaller version of itself.
    """
    x = int(card.width_px / 6)
    y = int(card.height_px / 6)
    small_im = card.image().resize((x, y))
    card.paste(small_im,
               left = card.gutter_mm,
               top  = card.gutter_mm,
               )
    card.paste(small_im,
               right = card.width_mm - card.gutter_mm,
               top   = card.gutter_mm,
               )

    return card

# Assemble all the card images

card_images = []
card_images.extend(one_stripe_cards(4))
card_images.extend(two_stripe_cards(3))
card_images.extend(three_stripe_cards(2))
card_images.extend(four_stripe_cards(4))
