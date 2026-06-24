from PIL import Image

from gamehelper.image_sheet import ImageSheet

import card_images as cardims


cards_out_file = 'out/cards.png'
num_cards      = len(cardims.card_images)


# Render the cards

sheet = ImageSheet(card_width  = cardims.base_maker.width_px,
                   card_height = cardims.base_maker.height_px,
                   columns     = 8,
                   cards       = num_cards,
                   )

for card_im in cardims.card_images:
    sheet.add(card_im)

sheet.save(cards_out_file)
print('Output to ' + cards_out_file)
