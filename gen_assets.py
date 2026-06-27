from PIL import Image

from gamehelper.image_sheet import ImageSheet

import card_images as cardims


cards_out_file = 'out/cards.png'
die_out_file   = 'out/die.png'
num_cards      = len(cardims.cards)
COL_COUNT      = cardims.COL_COUNT


# Render the cards

sheet = ImageSheet(card_width  = cardims.base_maker.width_px,
                   card_height = cardims.base_maker.height_px,
                   columns     = 8,
                   cards       = num_cards,
                   )

for crd in cardims.cards:
    sheet.add(crd)

sheet.save(cards_out_file)
print('Output to ' + cards_out_file)


# Render the die

sheet = ImageSheet(card_width  = cardims.die_side_ims[0].width,
                   card_height = cardims.die_side_ims[0].height,
                   columns     = COL_COUNT,
                   rows        = 1,
                   )

for side_im in cardims.die_side_ims:
    sheet.add(side_im)

sheet.save(die_out_file)
print('Output to ' + die_out_file)
