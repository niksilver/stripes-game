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
                       width_px = 480,
                       gutter   = 4,
                       )

border_size_mm = 3
mid_mm         = (base_maker.height_mm / 2) + 10    # Middle of stripes (main)
mid_top_mm     = 12                                 # Middle of stripes (top)


# Fonts

base_maker.font_family('DejaVu Sans',
                       file = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                       )
base_maker.font_name('Number',     family = 'DejaVu Sans', size = 48)
base_maker.font_name('Number top', family = 'DejaVu Sans', size = 12)


# Make cards and their images

def card(num: int, colours: list[bool]) -> CardMaker:
    """
    Make a card image with the given number and each stripe present or not.
    """
    maker = base_maker.copy()

    # Create each stripe

    for idx, include in enumerate(colours):
        if not(include): continue
        paste_stripes(maker, idx)


    maker.text(text   = str(num),    # Main
               center = maker.width / 2,
               middle = mid_mm,
               font   = 'Number',
               )
    maker.text(text   = str(num),    # Top left
               center = 8,
               middle = mid_top_mm,
               font   = 'Number top',
               )
    maker.text(text   = str(num),    # Top left
               center = maker.width - 8,
               middle = mid_top_mm,
               font   = 'Number top',
               )

    return maker


def paste_stripes(maker: CardMaker, idx: int):
    """
    Paste the stripes of a given index onto the card.
    Will include the main (larger) and top (smaller) stripes.
    """

    # The main stripe

    mid_separation_mm = 13
    y_mm              = (idx - 1.5) * mid_separation_mm + mid_mm

    maker.paste(stripe_ims[idx][0],
                center = maker.width_mm / 2,
                middle = y_mm,
                )

    # The top stripe

    mid_separation_mm = 4
    y_mm              = (idx - 1.5) * mid_separation_mm + mid_top_mm

    maker.paste(stripe_ims[idx][1],
                center = maker.width_mm / 2,
                middle = y_mm,
                )


def stripe_images(idx: int) -> (Image, Image):
    """
    Make two stripe image for this index - a main one and a top one.
    """
    thickness_px     = int(base_maker.to_px(8))
    thickness_top_px = int(base_maker.to_px(2.3))

    im0 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_px),
                    color = stripe_colours[idx],
                    )
    im1 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_top_px),
                    color = stripe_colours[idx],
                    )
    return (im0, im1)


# Assemble the cards


stripe_ims = [stripe_images(0),    # [main_image, top_image]
              stripe_images(1),
              stripe_images(2),
              stripe_images(3),
              ]


def one_stripe_cards(count_of_each: int) -> list[CardMaker]:
    """
    Return a list of one-stripe cards.
    """
    cards = []

    # Create one of each card

    for col in range(0, COL_COUNT):
        cols = [(i == col) for i in range(0, COL_COUNT)]
        crd  = card(4, cols)
        cards.append(crd)

    return cards * count_of_each


def two_stripe_cards(count_of_each: int) -> list[CardMaker]:
    """
    Return a list of two-stripe cards.
    """
    cards = []

    # Create one of each card

    for col1 in range(0, COL_COUNT - 1):
        for col2 in range(col1 + 1, COL_COUNT):
            cols = [(i == col1 or i == col2) for i in range(0, COL_COUNT)]
            crd  = card(2, cols)
            cards.append(crd)

    return cards * count_of_each


def three_stripe_cards(count_of_each: int) -> list[CardMaker]:
    """
    Return a list of three-stripe cards.
    """
    cards = []

    # Create one of each card

    for col in range(0, COL_COUNT):
        cols = [(i != col) for i in range(0, COL_COUNT)]
        crd  = card(1, cols)
        cards.append(crd)

    return cards * count_of_each


def four_stripe_cards(count_of_each: int) -> list[CardMaker]:
    """
    Return a list of four-stripe cards.
    """

    # Create the card

    crd = card(-1, [True] * COL_COUNT)

    return [crd] * count_of_each


# Assemble all the cards

cards = []
cards.extend(one_stripe_cards(4))
cards.extend(two_stripe_cards(3))
cards.extend(three_stripe_cards(2))
cards.extend(four_stripe_cards(4))


# Make sides of a die

die_side_ims = []
for i, col in enumerate(stripe_colours):
    length_px = base_maker.width_px // 2
    im = Image.new(mode = 'RGBA',
                   size = (length_px, length_px),
                   color = col,
                   )
    die_side_ims.append(im)
