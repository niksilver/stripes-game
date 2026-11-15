from PIL import Image

from gamehelper.pdf_sheets import PDFSheets

import card_images as cardims


cards_out_file = 'out/cards.pdf'
num_cards      = len(cardims.cards)


# Render the cards

sheet = PDFSheets(card_width  = 56,    ## mm
                  card_height = 88,    ## mm
                  gutter      = 4,
                  include_backs = False,
                  )

for crd in cardims.cards:
    sheet.add(crd)

sheet.output(cards_out_file)
print('Output to ' + cards_out_file)
