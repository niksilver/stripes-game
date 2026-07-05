import random


# Work out 1-stripe cards are more or less valuable than 2-stripe cards.

# A card is a list[bool], where list[i] == True iff it has a stripe of colour i.


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


def display_line(line: list[list[bool]]):
    """Print out a line of cards."""
    for i in range(0, NUM_STRIPES):
        for card in line:
            print('=' if card[i] else '.', end = '')
        print()


def add_to_line(line, deck) -> bool:
    """
    Given the line and the deck, add the next card onto the line
    that matches one of the stripes.
    onto the line. Will update both of these.
    Returns success Boolean.
    """
    target = line[-1]
    index  = 0
    match = False

    print(f'Testing {target}')
    for i, card in enumerate(deck):
        index = i
        for j in range(0, len(target)):
            if target[j] == card[j] == True:
                match = True
                break
        if match:
            break

    if match:
        card = deck.pop(index)
        line.append(card)
        print(f'matched with {card}')
        return True

    return False


if __name__ == '__main__':
    deck = create_deck()
    print(f'We have a deck of {len(deck)} cards')
    random.shuffle(deck)
    line = []
    line.append(deck.pop(0))
    display_line(line)
    add_to_line(line, deck)
    display_line(line)

else:
    print('Run this like a script')
