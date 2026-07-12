from PIL import Image

from gamehelper.image_sheet import ImageSheet

import card_images as cardims


cards_out_file = 'out/cards.png'
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
