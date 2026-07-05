# Work out 1-stripe cards are more or less valuable than 2-stripe cards.

NUM_STRIPES = 5

def create_deck():
    """Create a deck of cards."""
    deck = []

    # 1-stripe cards
    
    for i in range(0, NUM_STRIPES):
        card = [False] * NUM_STRIPES
        card[i] = True
        deck.extend([card] * 5)    # How mamy of each 1-stripe card

    # 2-stripe cards
    for i in range(0, NUM_STRIPES - 1):
        for j in range(i, NUM_STRIPES):
            card = [False] * NUM_STRIPES
            card[i] = True
            card[j] = True
            deck.extend([card] * 2)    # How mamy of each 2-stripe card

    return deck

if __name__ == '__main__':
    deck = create_deck()
    print(f'We have a deck of {len(deck)} cards')

else:
    print('Run this like a script')
