import random
import pygame
from pygame.locals import *
import time

# Initialize Pygame
pygame.init()

# Set up the window dimensions
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 640  # Increased height to accommodate the header

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
BLUE = (106, 159, 181)
GREEN = (136, 170, 119)

# Set up fonts
FONT_SIZE = 18
font = pygame.font.Font(None, FONT_SIZE)

def get_user_info():
    name = input("What's your name? ")
    return name

def load_taught_responses():
    try:
        with open("taught_responses.txt", "r") as file:
            lines = file.readlines()
            taught_responses = {}
            for line in lines:
                keyword, responses = line.strip().split(":")
                taught_responses[keyword] = [response.strip() for response in responses.split(",")]
    except FileNotFoundError:
        taught_responses = {}
    return taught_responses

def save_taught_responses(taught_responses):
    with open("taught_responses.txt", "w") as file:
        for keyword, responses in taught_responses.items():
            response_str = ", ".join(responses)
            file.write(f"{keyword}:{response_str}\n")

def get_time_in_london():
    # The same as before (omitted for simplicity)
    pass

def respond_bot(name, user_input, taught_responses):
    responses = {
        "hello": ["Hey there! Hiiii! How's it going? 😄","Hello, hello! What's up? Need anything?","Heya! I'm here to chat. What's your name?","Hey, hey, hey! How can I help you today?","Hi! waves What's your favorite game?","Um, hello! giggles What's your fave color?","Hey! Do you like ice cream? I love it! 🍦","Hi there! Wanna hear a joke? Knock-knock!","Heeey! Let's be friends! What do you say? 🤗","Hi! I'm bored, let's talk about something fun!"],
        "hi": ["Hey there! Hiiii! How's it going? 😄","Hello, hello! What's up? Need anything?","Heya! I'm here to chat. What's your name?","Hey, hey, hey! How can I help you today?","Hi! waves What's your favorite game?","Um, hello! giggles What's your fave color?","Hey! Do you like ice cream? I love it! 🍦","Hi there! Wanna hear a joke? Knock-knock!","Heeey! Let's be friends! What do you say? 🤗","Hi! I'm bored, let's talk about something fun!"],
        "how are you": ["Good and you?", "I'm doing fine, thank you!", "Pretty good, how about you?"],
        "thanks": ["You're welcome!", "No problem!", "My pleasure!", "Anytime!", "Glad I could help!", "You got it!", "Not a problem!", "No worries!", "Happy to assist!", "Sure thing!"],
        "what is the time": [get_time_in_london()],
        "what are you doing": ["I'm just relaxing at home.", "Currently, I'm working on a project.", "Just catching up on some reading.", "I'm chatting with friends online.", "Preparing dinner for tonight.", "Watching my favorite TV show.", "Taking a walk in the park.", "Practicing my hobbies, like painting.", "Attending an online class.", "Planning my weekend activities."],
        "who are you": ["I am a simple friend to talk to.", "I am a python chatbot who learns to speak from others."],
        "nice": ["Thank you!", "I'm glad you think so.", "Appreciate it!", "Thanks a lot!", "I thought you might like it.", "It's always nice to hear that.", "I put some effort into it.", "I'm pleased with the result.", "Glad you think so.", "It's one of my favorites."],
        "your such a monkey": ["Shut up", "Be quiet before I sell you to Abraham Lincon", "Fuck off you black orangatan"],
        "what you want to talk about": ["Um, let's talk about cool video games!","What's your favorite movie or TV show? Let's chat about that!","I wanna talk about funny memes and jokes!","Do you like sports? Let's talk about our favorite teams!","Have you ever been to an amusement park? Let's talk about roller coasters!","Let's discuss the latest trends and popular YouTubers!","Do you believe in aliens or ghosts? Let's talk about spooky stuff!","Have you read any awesome books lately? Let's share recommendations!","Wanna talk about our dream superpowers? That would be so cool!"],
        "master got me working": ["All Through The Summer"],
        "Some day": ["Master set me freeeeee"],
        "cool": ["Anyways..."],
        "Anyways": ["Anyways"],
        "what does mean": ["I dont know go ask google"],
        }

    user_input_lower = user_input.lower()  # Convert user input to lowercase

    chosen_response = ""  # Initialize chosen_response to an empty string

    # Check if the user input matches any of the responses
    for text, response in responses.items():
        if text in user_input_lower:
            # Randomly select a response
            chosen_response = random.choice(response)
            return chosen_response

    # Check if the user input matches any of the taught responses
    if user_input_lower in taught_responses:
        chosen_response = random.choice(taught_responses[user_input_lower])
    else:
        # If the input doesn't match any responses or taught responses, ask for user input
        print(f"Bot: I don't have the knowledge of that word. Could you help me, {name}? (y/n)")
        choice = input("You: ")
        if choice.lower() == "y":
            new_response = input("You: Please write a response for that: ")
            taught_responses[user_input_lower] = [response.strip() for response in new_response.split(',')]
            chosen_response = random.choice(taught_responses[user_input_lower])

    if not chosen_response:
        chosen_response = f"I'm sorry, I don't have a specific response to that, {name}."

    return chosen_response

def display_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_your_bubble(screen, text, x, y):
    # Draw a blue speech bubble for your message
    padding = 8
    text_width, text_height = font.size(text)
    bubble_rect = pygame.Rect(x - text_width - padding * 2, y - padding, text_width + padding * 2, text_height + padding * 2)
    pygame.draw.rect(screen, BLUE, bubble_rect, border_radius=10)
    display_text(screen, text, font, WHITE, x - text_width - padding, y)

def draw_bot_bubble(screen, text, x, y):
    # Draw a green speech bubble for the bot's message
    padding = 8
    text_width, text_height = font.size(text)
    bubble_rect = pygame.Rect(x + padding, y - padding, text_width + padding * 2, text_height + padding * 2)
    pygame.draw.rect(screen, GREEN, bubble_rect, border_radius=10)
    display_text(screen, text, font, WHITE, x + padding, y)


def draw_chat_history(screen, chat_history, your_name):
    message_box_height = 40
    header_height = 170  # Height of the header containing profile image and title
    chat_area_height = WINDOW_HEIGHT - message_box_height - header_height
    y_offset = header_height + chat_area_height - (len(chat_history) + 1) * (FONT_SIZE + 5)

    for text in chat_history:
        if text.startswith("You:"):
            # Draw your message bubble on the right
            draw_your_bubble(screen, text[5:], WINDOW_WIDTH - 10, y_offset)
        else:
            # Draw bot's message bubble on the left
            draw_bot_bubble(screen, text[5:], 10, y_offset)

        y_offset += FONT_SIZE + 5

def draw_discord_header(screen, user_name):
    # Draw grey box for the header
    header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 170)
    pygame.draw.rect(screen, LIGHT_GRAY, header_rect)

    # Load profile image
    profile_image = pygame.image.load("profile_image.jpg")
    profile_image = pygame.transform.scale(profile_image, (100, 100))

    # Create a circular mask for the profile image
    circle_mask = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(circle_mask, (255, 255, 255, 255), (50, 50), 50)
    circle_mask.blit(profile_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Draw circular profile image in the grey box
    circle_center = (WINDOW_WIDTH // 2, 120)
    screen.blit(circle_mask, (circle_center[0] - 50, circle_center[1] - 50))

    # Draw title inside the grey box
    title_text = "Friendly bot"
    title_font = pygame.font.Font(None, 36)
    title_color = BLACK
    title_surface = title_font.render(title_text, True, title_color)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
    screen.blit(title_surface, title_rect)

    small_text = "Made By Verlox.xy#2735. In association with Bothub server."
    small_font = pygame.font.Font(None, 14)
    small_color = BLACK
    small_surface = small_font.render(small_text, True, small_color)
    small_rect = small_surface.get_rect(center=(WINDOW_WIDTH // 2, 70))
    screen.blit(small_surface, small_rect)

def main():
    # Set up the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Texting Game")

    name = get_user_info()
    taught_responses = load_taught_responses()

    chat_history = []
    user_input = ""
    placeholder_text = "Type Message Here"
    text_color = (194, 193, 193)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input:
                        chat_history.append("You: " + user_input)
                        bot_response = "Bot: " + respond_bot(name, user_input, taught_responses)
                        chat_history.append(bot_response)
                        user_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                else:
                    # Change the text color and remove the placeholder text when the user starts typing
                    if placeholder_text in user_input:
                        user_input = ""
                        text_color = BLACK
                    user_input += event.unicode

        # Clear the screen
        screen.fill(WHITE)

        # Draw Discord-like header
        draw_discord_header(screen, name)

        # Draw chat history with your name
        draw_chat_history(screen, chat_history, name)

        # Draw message box
        pygame.draw.rect(screen, (95, 93, 93), (0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40))

        # Draw user input
        user_input_text = "You: " + user_input
        display_text(screen, user_input_text, font, text_color, 10, WINDOW_HEIGHT - 30)

        # Handle placeholder text
        if not user_input and chat_history:
            display_text(screen, placeholder_text, font, (194, 193, 193), 10, WINDOW_HEIGHT - 30)

        # Update the display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()