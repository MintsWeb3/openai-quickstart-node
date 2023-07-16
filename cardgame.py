import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# This is the structure of your game items
items = {
    'weapons': ['knife', 'rock', 'bottle', 'tennis racket', 'tv', 'pistol', 'pipe', 'bucket', 'hammer', '8ball'],
    'suspects': ['Rival', 'Degen', 'Hacker', 'Lover', 'Employee'],
    'locations': ['park', 'aquarium', 'market', 'street', 'waterfront', 'alley', 'pikeplace', '1st', 'pier']
}

# This is a basic representation of a card in your game
class Card:
    def __init__(self, category, name):
        self.category = category
        self.name = name
        self.image = pygame.image.load('rock.png')  # Replace with your own image file
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# This creates a deck of cards based on your items, with two of each card
def create_deck(items):
    deck = []
    for category, names in items.items():
        for name in names:
            deck.append(Card(category, name))
            deck.append(Card(category, name))
    random.shuffle(deck)
    return deck

# Main game function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Create a deck and define the current card
    deck = create_deck(items)
    current_card = None

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(deck) > 0:
                    current_card = deck.pop()

        # Draw the current card
        if current_card is not None:
            current_card.draw(screen)

        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()

if __name__ == '__main__':
    main()
