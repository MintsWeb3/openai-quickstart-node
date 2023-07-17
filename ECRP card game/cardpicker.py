import pygame
import random
import time
import threading

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 900  # Modified the height to better fit your screen
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Color to show when a match is made
CARD_WIDTH, CARD_HEIGHT = 150, 200  # Adjust these values according to your card images
GAP = 20  # Gap between cards

# This is the structure of your game items
items = {
    'weapon': ['bucket', 'rock', 'bottle', 'racket', 'tv', 'pistol', 'hammer', '8ball', 'pipe'],
    'suspect': ['rival', 'degen', 'hacker', 'lover', 'employee'],
    'location': ['park', 'aquarium', 'market', 'street', 'pikeplace', 'pier', 'waterfront', '1st', 'alley']
}

class Card:
    def __init__(self, category, name):
        self.category = category
        self.name = name
        image_file = f"{category}_{name.replace(' ', '_')}.jpg"
        self.face_up_image = pygame.image.load(image_file).convert_alpha()
        self.face_up_image = pygame.transform.scale(self.face_up_image, (CARD_WIDTH, CARD_HEIGHT))
        self.face_down_image = pygame.image.load('character_detective.jpg').convert_alpha()
        self.face_down_image = pygame.transform.scale(self.face_down_image, (CARD_WIDTH, CARD_HEIGHT))
        self.face_up = False
        self.rect = self.face_down_image.get_rect()

    def draw(self, surface):
        if self.face_up:
            surface.blit(self.face_up_image, self.rect)
        else:
            surface.blit(self.face_down_image, self.rect)

    def flip(self):
        self.face_up = not self.face_up

def create_deck(items):
    deck = []
    for category, names in items.items():
        for name in names:
            deck.append(Card(category, name))
            deck.append(Card(category, name))
    random.shuffle(deck)
    return deck

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("guilty.mp3")  # Use your music file here

    deck = create_deck(items)
    current_card = deck.pop()
    current_card.face_up = True

    # Create a 4x5 grid of cards
    card_grid = [[None for _ in range(5)] for _ in range(4)]
    for i in range(4):
        for j in range(5):
            card = deck.pop()
            card.rect.topleft = (j * (CARD_WIDTH + GAP), i * (CARD_HEIGHT + GAP) + CARD_HEIGHT + 3 * GAP)  # Change position of face-down cards
            card_grid[i][j] = card

    clicked_card = None
    running = True
    match_made = False
    while running:
        screen.fill(GREEN if match_made else WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not match_made:
                # Get card clicked
                x, y = pygame.mouse.get_pos()
                for i in range(4):
                    for j in range(5):
                        if card_grid[i][j].rect.collidepoint(x, y):
                            clicked_card = card_grid[i][j]
                            clicked_card.flip()

                            if clicked_card.category == current_card.category and clicked_card.name == current_card.name:
                                # Replace matched cards
                                current_card = deck.pop()
                                current_card.face_up = True
                                card_grid[i][j] = deck.pop()
                                card_grid[i][j].rect.topleft = (j * (CARD_WIDTH + GAP), i * (CARD_HEIGHT + GAP) + CARD_HEIGHT + 3 * GAP)
                                clicked_card = None
                                match_made = True
                                pygame.mixer.music.play()  # Play music
                                threading.Timer(3.0, lambda: setattr(match_made, "False")).start()  # End celebration after 3 seconds
                            else:
                                # Flip the card back after 3 seconds
                                threading.Timer(3.0, clicked_card.flip).start()

        # Draw current card
        current_card.rect.topleft = (2 * (CARD_WIDTH + GAP), GAP)
        current_card.draw(screen)

        # Draw card grid
        for i in range(4):
            for j in range(5):
                card_grid[i][j].draw(screen)

        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()

if __name__ == '__main__':
    main()
