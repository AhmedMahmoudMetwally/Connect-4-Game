import numpy as np
import pygame
import sys
import math
import time
from copy import deepcopy

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 0, 150)
LIGHT_BLUE = (173, 216, 230)

# Game constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BOARD_WIDTH = COLUMN_COUNT * SQUARESIZE
INFO_PANEL_WIDTH = 400
WINDOW_WIDTH = BOARD_WIDTH + INFO_PANEL_WIDTH
WINDOW_HEIGHT = (ROW_COUNT + 1) * SQUARESIZE + 50

# AI constants
AI_PLAYER = 2
HUMAN_PLAYER = 1


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
    return False


def evaluate_window(window, piece):
    score = 0
    opp_piece = HUMAN_PLAYER if piece == AI_PLAYER else AI_PLAYER

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, HUMAN_PLAYER) or winning_move(board, AI_PLAYER) or len(get_valid_locations(board)) == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax(board, depth, maximizingPlayer, alpha=-math.inf, beta=math.inf, use_alpha_beta=False):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PLAYER):
                return (None, 100000000000000)
            elif winning_move(board, HUMAN_PLAYER):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PLAYER))

    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = deepcopy(board)
            drop_piece(b_copy, row, col, AI_PLAYER)
            new_score = minimax(b_copy, depth - 1, False, alpha, beta, use_alpha_beta)[1]
            if new_score > value:
                value = new_score
                column = col
            if use_alpha_beta:
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = deepcopy(board)
            drop_piece(b_copy, row, col, HUMAN_PLAYER)
            new_score = minimax(b_copy, depth - 1, True, alpha, beta, use_alpha_beta)[1]
            if new_score < value:
                value = new_score
                column = col
            if use_alpha_beta:
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return column, value


def draw_board(board, screen, ai_info=None):
    # Draw the game board
    pygame.draw.rect(screen, DARK_BLUE, (0, 0, BOARD_WIDTH, WINDOW_HEIGHT))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # Draw the pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), WINDOW_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2) - 50),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), WINDOW_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2) - 50),
                                   RADIUS)

    # Draw the info panel
    pygame.draw.rect(screen, LIGHT_BLUE, (BOARD_WIDTH, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT))

    if ai_info:
        font = pygame.font.SysFont("Arial", 22, bold=True)
        title_font = pygame.font.SysFont("Arial", 26, bold=True)

        # AI Thinking Title
        title = title_font.render("AI Thinking Process", 1, DARK_BLUE)
        screen.blit(title, (BOARD_WIDTH + 20, 20))

        # Draw a divider line
        pygame.draw.line(screen, DARK_BLUE, (BOARD_WIDTH + 10, 60), (WINDOW_WIDTH - 10, 60), 2)

        y_pos = 80
        for line in ai_info:
            # Highlight key information
            if "Algorithm:" in line or "Depth:" in line or "Move Selected:" in line:
                text = font.render(line, 1, DARK_BLUE)
            else:
                text = font.render(line, 1, BLACK)

            screen.blit(text, (BOARD_WIDTH + 20, y_pos))
            y_pos += 30

        # Draw move evaluation visualization
        if "Move Evaluations:" in ai_info:
            eval_start = y_pos + 20
            eval_title = font.render("Move Evaluations:", 1, DARK_BLUE)
            screen.blit(eval_title, (BOARD_WIDTH + 20, eval_start))

            # Get the evaluations
            eval_text = ai_info[ai_info.index("Move Evaluations:") + 1]
            evaluations = eval_text.split(", ")

            # Draw bars for each column evaluation
            bar_start = eval_start + 40
            for i, eval_str in enumerate(evaluations):
                if i >= COLUMN_COUNT:
                    break

                try:
                    col, score = eval_str.split(": ")
                    score = float(score)
                except:
                    continue

                # Normalize score for display (assuming scores between -10 and 10)
                bar_length = min(max(score * 10, -150), 150)

                # Draw bar
                if bar_length >= 0:
                    pygame.draw.rect(screen, GREEN,
                                     (BOARD_WIDTH + 50 + i * 40, bar_start + 20, 20, -bar_length))
                else:
                    pygame.draw.rect(screen, RED,
                                     (BOARD_WIDTH + 50 + i * 40, bar_start + 20, 20, -bar_length))

                # Draw column number
                col_text = font.render(str(i + 1), 1, BLACK)
                screen.blit(col_text, (BOARD_WIDTH + 50 + i * 40, bar_start + 50))

    pygame.display.update()


def draw_button(screen, rect, text, font, color, hover_color, text_color=WHITE):
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color

    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)  # Border

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return rect.collidepoint(mouse_pos)


def draw_game_setup(screen):
    screen.fill(LIGHT_BLUE)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    button_font = pygame.font.SysFont("Arial", 28)

    # Title
    title = title_font.render("Connect Four", 1, DARK_BLUE)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

    # Game mode selection title
    mode_title = button_font.render("Select Game Mode:", 1, DARK_BLUE)
    screen.blit(mode_title, (WINDOW_WIDTH // 2 - mode_title.get_width() // 2, 120))

    # Buttons
    button_width, button_height = 300, 60
    button_x = WINDOW_WIDTH // 2 - button_width // 2

    hvh_button = pygame.Rect(button_x, 180, button_width, button_height)
    hvc_button = pygame.Rect(button_x, 260, button_width, button_height)
    cvh_button = pygame.Rect(button_x, 340, button_width, button_height)
    cvc_button = pygame.Rect(button_x, 420, button_width, button_height)

    # Draw buttons
    buttons = []
    buttons.append(draw_button(screen, hvh_button, "Human vs Human", button_font, BLUE, DARK_BLUE))
    buttons.append(draw_button(screen, hvc_button, "Human vs AI", button_font, BLUE, DARK_BLUE))
    buttons.append(draw_button(screen, cvh_button, "AI vs Human", button_font, BLUE, DARK_BLUE))
    buttons.append(draw_button(screen, cvc_button, "AI vs AI", button_font, BLUE, DARK_BLUE))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]:
                    return "hvh", None
                elif buttons[1]:
                    return "hvc", select_ai_difficulty(screen)
                elif buttons[2]:
                    return "cvh", select_ai_difficulty(screen)
                elif buttons[3]:
                    return "cvc", select_ai_difficulty(screen)

        # Update button hover effects
        buttons = []
        buttons.append(draw_button(screen, hvh_button, "Human vs Human", button_font, BLUE, DARK_BLUE))
        buttons.append(draw_button(screen, hvc_button, "Human vs AI", button_font, BLUE, DARK_BLUE))
        buttons.append(draw_button(screen, cvh_button, "AI vs Human", button_font, BLUE, DARK_BLUE))
        buttons.append(draw_button(screen, cvc_button, "AI vs AI", button_font, BLUE, DARK_BLUE))

        pygame.display.update()


def select_ai_difficulty(screen):
    screen.fill(LIGHT_BLUE)
    title_font = pygame.font.SysFont("Arial", 32, bold=True)
    button_font = pygame.font.SysFont("Arial", 24)

    # Title
    title = title_font.render("Select AI Difficulty Level", 1, DARK_BLUE)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

    # Buttons
    button_width, button_height = 250, 50
    button_x = WINDOW_WIDTH // 2 - button_width // 2

    easy_button = pygame.Rect(button_x, 130, button_width, button_height)
    medium_button = pygame.Rect(button_x, 200, button_width, button_height)
    hard_button = pygame.Rect(button_x, 270, button_width, button_height)
    expert_button = pygame.Rect(button_x, 340, button_width, button_height)

    # Draw buttons
    buttons = []
    buttons.append(draw_button(screen, easy_button, "Easy", button_font, GREEN, (0, 200, 0), WHITE))
    buttons.append(draw_button(screen, medium_button, "Medium", button_font, YELLOW, (200, 200, 0), BLACK))
    buttons.append(draw_button(screen, hard_button, "Hard", button_font, (255, 165, 0), (200, 100, 0), WHITE))
    buttons.append(draw_button(screen, expert_button, "Expert", button_font, RED, (200, 0, 0), WHITE))

    # Difficulty descriptions
    desc_font = pygame.font.SysFont("Arial", 16)
    descriptions = [
        "Depth: 2 - Basic AI with limited lookahead",
        "Depth: 4 - Moderate AI with decent strategy",
        "Depth: 6 - Strong AI with good planning",
        "Depth: 8 - Expert AI with deep lookahead"
    ]

    for i, desc in enumerate(descriptions):
        text = desc_font.render(desc, 1, DARK_BLUE)
        screen.blit(text, (button_x, 130 + (i * 70) + button_height + 5))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]:
                    return select_ai_algorithm(screen, 2)  # Easy
                elif buttons[1]:
                    return select_ai_algorithm(screen, 4)  # Medium
                elif buttons[2]:
                    return select_ai_algorithm(screen, 6)  # Hard
                elif buttons[3]:
                    return select_ai_algorithm(screen, 8)  # Expert

        # Update button hover effects
        buttons = []
        buttons.append(draw_button(screen, easy_button, "Easy", button_font, GREEN, (0, 200, 0), WHITE))
        buttons.append(draw_button(screen, medium_button, "Medium", button_font, YELLOW, (200, 200, 0), BLACK))
        buttons.append(draw_button(screen, hard_button, "Hard", button_font, (255, 165, 0), (200, 100, 0), WHITE))
        buttons.append(draw_button(screen, expert_button, "Expert", button_font, RED, (200, 0, 0), WHITE))

        pygame.display.update()


def select_ai_algorithm(screen, depth):
    screen.fill(LIGHT_BLUE)
    title_font = pygame.font.SysFont("Arial", 32, bold=True)
    button_font = pygame.font.SysFont("Arial", 24)
    desc_font = pygame.font.SysFont("Arial", 18)

    # Title
    title = title_font.render("Select AI Algorithm", 1, DARK_BLUE)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

    # Buttons
    button_width, button_height = 300, 60
    button_x = WINDOW_WIDTH // 2 - button_width // 2

    minimax_button = pygame.Rect(button_x, 150, button_width, button_height)
    alphabeta_button = pygame.Rect(button_x, 250, button_width, button_height)

    # Draw buttons
    buttons = []
    buttons.append(draw_button(screen, minimax_button, "Minimax", button_font, BLUE, DARK_BLUE))
    buttons.append(draw_button(screen, alphabeta_button, "Alpha-Beta Pruning", button_font, BLUE, DARK_BLUE))

    # Algorithm descriptions
    minimax_desc = [
        "Standard Minimax algorithm",
        "Evaluates all possible moves",
        "Slower but thorough"
    ]

    alphabeta_desc = [
        "Optimized Minimax with pruning",
        "Skips irrelevant branches",
        "Faster but same results as Minimax"
    ]

    for i, line in enumerate(minimax_desc):
        text = desc_font.render(line, 1, DARK_BLUE)
        screen.blit(text, (button_x, 150 + button_height + 10 + i * 25))

    for i, line in enumerate(alphabeta_desc):
        text = desc_font.render(line, 1, DARK_BLUE)
        screen.blit(text, (button_x, 250 + button_height + 10 + i * 25))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]:
                    return {"depth": depth, "use_alpha_beta": False}
                elif buttons[1]:
                    return {"depth": depth, "use_alpha_beta": True}

        # Update button hover effects
        buttons = []
        buttons.append(draw_button(screen, minimax_button, "Minimax", button_font, BLUE, DARK_BLUE))
        buttons.append(draw_button(screen, alphabeta_button, "Alpha-Beta Pruning", button_font, BLUE, DARK_BLUE))

        pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enhanced Connect Four")

    # Game setup
    game_mode, ai_settings = draw_game_setup(screen)

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0  # 0 for player 1 (human), 1 for player 2 (human or AI)

    # Font for messages
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    smallfont = pygame.font.SysFont("Arial", 20)

    # Clear the screen
    screen.fill(BLACK)
    draw_board(board, screen)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse motion for human players
            if (game_mode == "hvh" or
                    (game_mode == "hvc" and turn == 0) or
                    (game_mode == "cvh" and turn == 1)):

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, BOARD_WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if posx < BOARD_WIDTH:  # Only show piece if over the board
                        if turn == 0:
                            pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                        else:
                            pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < BOARD_WIDTH:
                    pygame.draw.rect(screen, BLACK, (0, 0, BOARD_WIDTH, SQUARESIZE))

                    # Human move
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, turn + 1)

                        if winning_move(board, turn + 1):
                            label = myfont.render(f"Player {turn + 1} wins!!", 1, RED if turn == 0 else YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                        print_board(board)
                        draw_board(board, screen)

                        turn += 1
                        turn %= 2

        # AI move
        if not game_over and ((game_mode == "hvc" and turn == 1) or
                              (game_mode == "cvh" and turn == 0) or
                              (game_mode == "cvc")):

            # Display thinking message
            thinking_text = smallfont.render("AI is thinking...", 1, DARK_BLUE)
            screen.blit(thinking_text, (BOARD_WIDTH + 20, WINDOW_HEIGHT - 50))
            pygame.display.update()

            # Get AI move with evaluation of all possible moves
            start_time = time.time()

            # First evaluate all possible moves to show in the UI
            valid_locations = get_valid_locations(board)
            evaluations = []
            for col in valid_locations:
                row = get_next_open_row(board, col)
                temp_board = deepcopy(board)
                drop_piece(temp_board, row, col, AI_PLAYER if (turn == 1 or game_mode == "cvc") else HUMAN_PLAYER)
                score = score_position(temp_board, AI_PLAYER if (turn == 1 or game_mode == "cvc") else HUMAN_PLAYER)
                evaluations.append(f"{col}: {score}")

            # Then get the actual move using minimax
            col, minimax_score = minimax(
                board,
                ai_settings["depth"],
                True if (turn == 1 and game_mode == "hvc") or (turn == 0 and game_mode == "cvh") or (
                            game_mode == "cvc" and turn == 1) else False,
                use_alpha_beta=ai_settings["use_alpha_beta"]
            )
            thinking_time = time.time() - start_time

            if is_valid_location(board, col):
                # Prepare AI info to display
                ai_info = [
                    f"AI Player: {'Yellow' if turn == 1 else 'Red'}",
                    f"Algorithm: {'Alpha-Beta' if ai_settings['use_alpha_beta'] else 'Minimax'}",
                    f"Search Depth: {ai_settings['depth']}",
                    f"Thinking Time: {thinking_time:.2f} seconds",
                    "",
                    f"Move Selected: Column {col + 1}",
                    f"Move Score: {minimax_score}",
                    "",
                    "Move Evaluations:",
                    ", ".join(evaluations)
                ]

                pygame.time.wait(1000)  # Pause to show thinking

                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn + 1)

                if winning_move(board, turn + 1):
                    winner_text = f"AI Player {turn + 1} wins!!" if game_mode == "cvc" else f"AI wins!!"
                    label = myfont.render(winner_text, 1, RED if turn == 0 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board, screen, ai_info)

                turn += 1
                turn %= 2

        if game_over:
            pygame.time.wait(3000)


if __name__ == "__main__":
    main()