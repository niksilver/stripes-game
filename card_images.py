import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from   gamehelper.card_maker import CardMaker
import gamehelper.utils      as gameutils


palette_basic = {'magenta': (212,   0, 212, 220),
                 'yellow':  (212, 212,   0, 220),
                 'green':   (  0, 192,   0, 220),
                 'blue':    ( 96,  96, 255, 220),
                 'cyan':    (  0, 212, 212, 220),
                 }
palette_nik_colourblind = {
        'red':    (216,  27,  96, 245),
        'blue':   ( 30, 136, 229, 245),
        'yellow': (255, 193,   7, 245),
        'brown':  (175,  88,  10, 245),
        'green':  (101, 181,   4, 245),
        }

COL_COUNT      = None    # Set in the scheme


# Base card

base_maker = CardMaker(width    = 58,
                       height   = 85,
                       unit     = 'mm',
                       width_px = 360,
                       gutter   = 4,
                       )

mid_mm         = (base_maker.height_mm / 2) + 9     # Middle of stripes (main)
mid_top_mm     = 10                                 # Middle of stripes (top)


# Fonts

base_maker.font_family('DejaVu Sans',
                       file = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                       )
base_maker.font_name('Number',     family = 'DejaVu Sans', size = 40)
base_maker.font_name('Number top', family = 'DejaVu Sans', size = 8)


# Make card include mappings


def sign(n: int) -> int:
    """
    Return 1, 0, or -1 as the sign of n.
    """
    if n == 0:
        return 0
    elif n < 0:
        return -1
    else:
        return 1


def make_stripe_includes() -> list[list[list[bool]]]:
    """
    Return a list of stripe includes.  Result[n] is a list `c` such that
    each element is a unique list[bool] which contains exactly
    `n` True values.
    E.g. Result[2] is every list[bool] where exactly two elements are True.
    """
    out = [[] for i in range(COL_COUNT + 1)]

    for i in range(1, 2**COL_COUNT):
        stripes = 0
        pattern = []

        for power in range(0, COL_COUNT):
            digit = sign(i & (2 ** power))   # Binary digit in column `power`
            stripes = stripes + digit        # Count of 1s in binary form
            pattern.append(digit == 1)       # Building the list[bool]
        
        out[stripes].append(pattern)

    return out


# Make cards and their images

def make_card(text: str, include: list[bool]) -> CardMaker:
    """
    Make a card image with the given text and each stripe included or not.
    """
    maker = base_maker.copy()

    # Create each stripe

    for idx, include in enumerate(include):
        paste_stripes(maker, idx, include)


    text_closer(maker = maker,
                text   = text,    # Main
                center = maker.width / 2,
                middle = mid_mm,
                font   = 'Number',
                offset = 11,
                )
    text_closer(maker = maker,
                text   = text,    # Top right
                center = 7,
                middle = mid_top_mm,
                font   = 'Number top',
                offset = 2.5,
                )
    text_closer(maker = maker,
                text   = text,    # Top left
                center = maker.width - 7,
                middle = mid_top_mm,
                font   = 'Number top',
                offset = 2.5,
                )

    return maker


def text_closer(maker: CardMaker,
                text: str,
                center: float,
                middle: float,
                font: str,
                offset: float,
                ):
    """
    Add centred text, but apply closer kerning of two-character strings.
    - offset: For a two character string, how much to shift each
      character closer to the intended centre of the pair.
    """
    text_colour = (0, 0, 0, 255)

    if len(text) == 2:
        maker.text(text   = text[0],
                   center = center - offset,
                   middle = middle,
                   font   = font,
                   fill   = text_colour,
                   )
        maker.text(text   = text[1],
                   center = center + offset,
                   middle = middle,
                   font   = font,
                   fill   = text_colour,
                   )
    else:
        maker.text(text   = text,
                   center = center,
                   middle = middle,
                   font   = font,
                   fill   = text_colour,
                   )
    

def paste_stripes(maker: CardMaker, idx: int, include: bool):
    """
    Paste the stripes of a given index onto the card.
    Will include the main (larger) and top (smaller) stripes.
    A stripe that's not included will get a thin line.
    """

    mid_offset = (COL_COUNT - 1) / 2

    # The main stripe

    mid_separation_mm = 10.0
    y_mm              = (idx - mid_offset) * mid_separation_mm + mid_mm

    im = visuals.empty_ims[0]
    if include:
        im = visuals.ims[idx][0]

    maker.paste(im,
                center = maker.width_mm / 2,
                middle = y_mm,
                )

    # The top stripe

    im = visuals.empty_ims[1]
    if include:
        im = visuals.ims[idx][1]

    mid_separation_mm = 2.5
    y_mm              = (idx - mid_offset) * mid_separation_mm + mid_top_mm

    maker.paste(im,
                center = maker.width_mm / 2,
                middle = y_mm,
                )


def get_visuals(palette: dict[str, tuple[int,int,int,int]],
                shape_colour: list[tuple[str, str]]) -> tuple[
                        tuple[int,int,int,int],
                        dict[str, str]]:
    """
    - `palette`: Map of colour name (string) to a 4-tuple RGBA value.
    - `shape_colour`: List of pairs: shape name and colour. The shape
      name will transform to `assets/NAME.png`.

    Returns an object with these properties:
    - `colours`: A list of RGBA values, with index 0 being the colour of the top stripe.
    - `filenames`: A list of filenames (strings), with index 0 being the image asset
      of the top stripe.
    - `ims`: A list of pairs. Each pair is an Image. The first is the image to use in
      the main body of the card for that stripe index; the second is the image for the
      top of the card.
    - `empty_ims`: A pair of empty images to use when an index has no stripe.
    """

    class Visuals:
        colours   = []
        filenames = []
        ims       = []
        empty_ims = ()
    out = Visuals()

    for (shape_name, colour_name) in shape_colour:
        colour   = palette[colour_name]
        filename = f'assets/{shape_name}.png'
        out.colours.append(colour)
        out.filenames.append(filename)
        out.ims.append(pattern_stripe_images(filename, colour))

    out.empty_ims = no_stripe_images()

    return out


def pattern_stripe_images(filename: str, colour: (int,int,int,int)) -> (Image, Image):
    """
    Make two plain stripe images - a main one and a top one.
    """
    thickness_px     = int(base_maker.to_px(6.5))
    thickness_top_px = int(base_maker.to_px(1.2))

    im       = Image.open(filename).convert('RGBA')
    col_im   = Image.new('RGBA',
                       size  = (im.width, im.height),
                       color = colour,
                       )
    im.paste(col_im, mask = im)

    # Main stripe image

    width_px  = base_maker.width_with_gutters_px
    height_px = int(thickness_px * 1.2)

    im0 = im.resize(size = (width_px, height_px))

    # Small top stripe image

    im_canvas = gameutils.repeat(im, 4)

    rescale = 0.25
    width_px  = int(im_canvas.width * rescale)
    height_px = int(im_canvas.height * rescale)
    im1 = im_canvas.resize(size = (width_px, height_px))

    return (im0, im1)


# Alternative ways of showing 'no stripes'.


def no_stripe_images() -> (Image, Image):
    """
    Make two no-stripe images for any index - a main one and a top one.
    This is just empty space.
    """
    thickness_px     = int(base_maker.to_px(0.18))
    thickness_top_px = int(base_maker.to_px(0.17))

    im0 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_px),
                    color = (128, 128, 128, 0),    # Entirely transparent
                    )
    im1 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_top_px),
                    color = (128, 128, 128, 0),    # Entirely transparent
                    )
    return (im0, im1)


def pin_stripe_images() -> (Image, Image):
    """
    Make two no-stripe images for any index - a main one and a top one.
    This is just a thin line.
    """
    thickness_px     = int(base_maker.to_px(0.18))    # Very thin
    thickness_top_px = int(base_maker.to_px(0.17))    # Very thin

    im0 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_px),
                    color = (128, 128, 128, 220),    # Grey
                    )
    im1 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_top_px),
                    color = (128, 128, 128, 220),    # Grey
                    )
    return (im0, im1)


def grey_stripe_images() -> (Image, Image):
    """
    Make two no-stripe images for any index - a main one and a top one.
    This is the same as a stripe, but light grey.
    """
    thickness_px     = int(base_maker.to_px(6.5))    # Same thickness as coloured stripes
    thickness_top_px = int(base_maker.to_px(1.4))    # Same thickness as coloured stripes

    im0 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_px),
                    color = (128, 128, 128, 64),    # Grey
                    )
    im1 = Image.new(mode = 'RGBA',
                    size = (base_maker.width_with_gutters_px, thickness_top_px),
                    color = (128, 128, 128, 64),    # Grey
                    )
    return (im0, im1)


# Scheme to put the scores on the cards


class SingleSequenceScheme_5Stripes:
    """
    When the cards are all in a single sequence from 1 to 45.
    Five stripes.
    """

    COL_COUNT = 5

    def one_stripe_scores(include: list[bool]) -> str:
        """
        Given a 1-stripe pattern, return the scores that such a card
        would have.
        """
        idx = include.index(True)
        scores = [idx+21, idx+21+5, idx+21+5+5, 45-5-idx, 45-idx]
        return [str(s) for s in scores]


    def two_stripe_scores(include: list[bool]) -> str:
        """
        Given a 2-stripe pattern, return the scores that such a card
        would have.
        For details see design diary of 2026-07-15 (new numbering).
        """
        lookup = [[  [0, 0], [1, 20], [5, 16], [8, 13], [11, 12]],
                  [  [0, 0], [0,  0], [2, 19], [6, 15], [ 9, 10]],
                  [  [0, 0], [0,  0], [0,  0], [3, 18], [ 7, 14]],
                  [  [0, 0], [0,  0], [0,  0], [0,  0], [ 4, 17]],
                 ]
        row = include.index(True)
        col = include.index(True, row + 1)
        scores = lookup[row][col]
        return [str(s) for s in scores]


class PerColourScheme_5Stripes_Problem:
    """
    Five stripes. There is an error here. It doesn't work like 4-strip cards.

    When every colour is numbered 1-13 (and the two-stripe cards overlap).
    - Every suit has a card 1-13.
    - Two-stripe cards are low ones, one-stripe cards are numbered 9+
    - Numbers work like this:

    ```
        A        B        C        D        E
    A:          1,2      3,4      5,6      7,8
    B:                   5,6      7,8      1,2
    C:                            1,2      3,4
    D:                                     5,6
    E:
    ```
    The pattern is:
    - For the first suit (A), go across 1,2 then 3,4 etc.
    - For each subsequent suit start on the first line, continue the
      pattern down and then across.
	  - E.g. Suit D starts on the first line (5,6) goes down with 7,8
        then loops back to 1,2, and then has to go across with 3,4.

    This is from design diary 2026-08-18.
    """

    COL_COUNT = 5

    def one_stripe_scores(include: list[bool]) -> str:
        """
        Given a 1-stripe pattern, return the scores that such a card
        would have.
        """
        scores = [9, 10, 11, 12, 13]
        return [str(s) for s in scores]


    def two_stripe_scores(include: list[bool]) -> str:
        """
        Given a 2-stripe pattern, return the scores that such a card
        would have.
        For details see design diary of 2026-07-15 (new numbering).
        """
        lookup = [[  [0, 0], [1, 2], [3, 4], [5, 6], [7, 8]],
                  [  [0, 0], [0, 0], [5, 6], [7, 8], [1, 2]],
                  [  [0, 0], [0, 0], [0, 0], [1, 2], [3, 4]],
                  [  [0, 0], [0, 0], [0, 0], [0, 0], [5, 6]],
                 ]
        row = include.index(True)
        col = include.index(True, row + 1)
        scores = lookup[row][col]
        return [str(s) for s in scores]


class PerColourScheme_4Stripes_4Doubles:
    """
    Four stripes, with four of each 2-stripe card. 44 cards total.

    When every colour is numbered from 1 to 17 (and the two-stripe cards overlap).
    - Every suit has a card 1, 2, 3, etc.
    - Two-stripe cards are low ones, one-stripe cards are numbered beyond those.
    - Numbers work like this:

    ```
        A        B        C        D
    A:       1,2,3,4  5,6,7,8   9,10,11,12
    B:               9,10,11,12  5,6,7,8
    C:                           1,2,3,4
    D:
    ```
    The pattern is:
    - For the first suit (A), go across 1,2,3,4 then 5,6,7,8 etc.
    - For each subsequent suit start on the first line, continue the pattern
      down until you get to (n, n). Go into that cell but don't fill it.
      Then go across. We have to fill in numbers we don't yet see.
    """

    COL_COUNT = 4

    def one_stripe_scores(include: list[bool]) -> str:
        """
        Given a 1-stripe pattern, return the scores that such a card
        would have.
        """
        scores = [13, 14, 15, 16, 17]
        return [str(s) for s in scores]


    def two_stripe_scores(include: list[bool]) -> str:
        """
        Given a 2-stripe pattern, return the scores that such a card
        would have.
        For details see design diary of 2026-07-15 (new numbering).
        """
        _ = 0
        lookup = [[  [_,_,_,_], [1,2,3,4], [5,6,  7, 8], [9,10,11,12]],
                  [  [_,_,_,_], [_,_,_,_], [9,10,11,12], [5, 6, 7, 8]],
                  [  [_,_,_,_], [_,_,_,_], [_, _, _, _], [1, 2, 3, 4]],
                 ]
        row = include.index(True)
        col = include.index(True, row + 1)
        scores = lookup[row][col]
        return [str(s) for s in scores]


class PerColourScheme_4Stripes_3Doubles:
    """
    Four stripes, with three of each 2-stripe card. 38 cards total.
    Algorithm otherwise like PerColourScheme_4Stripes_4Doubles
    """

    COL_COUNT = 4

    def one_stripe_scores(include: list[bool]) -> str:
        """
        Given a 1-stripe pattern, return the scores that such a card
        would have.
        """
        scores = [10, 11, 12, 13, 14]
        return [str(s) for s in scores]


    def two_stripe_scores(include: list[bool]) -> str:
        """
        Given a 2-stripe pattern, return the scores that such a card
        would have.
        For details see design diary of 2026-07-15 (new numbering).
        """
        _ = 0
        lookup = [[  [_,_,_], [1,2,3], [4,5,6], [7,8,9]],
                  [  [_,_,_], [_,_,_], [7,8,9], [4,5,6]],
                  [  [_,_,_], [_,_,_], [_,_,_], [1,2,3]],
                 ]
        row = include.index(True)
        col = include.index(True, row + 1)
        scores = lookup[row][col]
        return [str(s) for s in scores]


# Define our card scheme and visual style

scheme    = PerColourScheme_4Stripes_3Doubles
COL_COUNT = scheme.COL_COUNT
visuals   = get_visuals(palette_nik_colourblind,
                        [('ribbon', 'red'),
                         ('rope',   'yellow'),
                         ('waves',  'blue'),
                         ('dots',   'green'),
                         ])

# Assemble all the cards

stripe_includes = make_stripe_includes()
cards           = []

# 1-stripe cards

for include in stripe_includes[1]:
    for score in scheme.one_stripe_scores(include):
        card = make_card(score, include)
        cards.append(card)

# 2-stripe cards

for include in stripe_includes[2]:
    for score in scheme.two_stripe_scores(include):
        card = make_card(score, include)
        cards.append(card)
