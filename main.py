import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

# Cài đặt font chữ
FONT = pygame.font.SysFont(None, 36)

# Màu sắc
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Hệ số tốc độ
SPEED_FACTOR = 0.3

class Word:
    def __init__(self, x, y, word):
        self.x = x
        self.y = y
        self.text = word
        self.colors = [BLACK] * len(self.text)
        # Tính toán tốc độ dựa trên số lượng chữ cái trong từ
        self.speed = 5 - len(self.text) * SPEED_FACTOR

    def update_color(self, user_input):
        for i in range(len(self.text)):
            if i < len(user_input) and user_input[i] == self.text[i]:
                self.colors[i] = GREEN
            elif i < len(user_input):
                self.colors[i] = RED
            else:
                self.colors[i] = BLACK

    def draw(self):
        x_pos = self.x
        for i, char in enumerate(self.text):
            text_surface = FONT.render(char, True, self.colors[i])
            win.blit(text_surface, (x_pos, self.y))
            x_pos += text_surface.get_width() + 2  # Để khoảng cách giữa các ký tự

# Hàm để tạo từ ngẫu nhiên từ tệp words.txt
def generate_word():
    with open("words.txt", "r") as file:
        data = file.read().replace(",", " ").split()
    return random.choice(data).lower()  # Loại bỏ dấu cách và chuyển thành chữ thường

# Vẽ button
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(win, color, (x, y, width, height))
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    win.blit(text_surface, text_rect)

# Hàm chính của trò chơi
def main():
    clock = pygame.time.Clock()

    # Load ảnh nền và thay đổi kích thước
    background_image = pygame.image.load("background_image.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Tạo tọa độ ban đầu của từ
    x = random.randrange(0, WIDTH - 400)
    y = 0

    word = Word(x, y,generate_word())
    user_input = ""

    # Phát nhạc nền
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)  # -1 để phát lại liên tục

    # Màn hình bắt đầu
    game_started = False
    start_button = Word(WIDTH / 2 - 40, HEIGHT / 2, "start")
    while not game_started:
        win.blit(background_image, (0, 0))  # Vẽ ảnh nền
        start_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if user_input == start_button.text[:len(user_input)]:
                        if len(user_input) < len(start_button.text):
                            user_input += event.unicode
                        else:
                            game_started = True
                    else:
                        user_input = ""
                elif event.unicode or event.key == pygame.K_SPACE:
                    user_input += event.unicode
        start_button.update_color(user_input)

        pygame.display.update()
        clock.tick(30)

    game_over = False    
    user_input = ""
    # Khởi tạo tốc độ ban đầu
    speed_mutilplier = 0.01

    # Định nghĩa biến để xác định thời gian giữa mỗi lần tăng tốc độ
    start_time = pygame.time.get_ticks()
    # Trong vòng lặp chính
    while not game_over:
        # Cập nhật thời gian hiện tại
        word.speed += speed_mutilplier
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 1000:
            speed_mutilplier += 0.005  # Tăng 0.1% tốc độ
            start_time = current_time
        

        win.blit(background_image, (0, 0))  # Vẽ ảnh nền
        word.draw()

        # Di chuyển từ xuống dưới
        word.y += word.speed

        # Kiểm tra nếu từ chạm vào đáy màn hình
        if word.y >= HEIGHT:
            game_over = True

        # Xử lý sự kiện từ bàn phím
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if user_input == word.text[:len(user_input)]:
                        if len(user_input) < len(word.text):
                            user_input += event.unicode
                        else:
                            word = Word(random.randrange(0, WIDTH - 60), 0, generate_word())
                            user_input = ""
                    else:
                        user_input = ""
                elif event.unicode or event.key == pygame.K_SPACE:
                    user_input += event.unicode

        word.update_color(user_input)

        pygame.display.update()
        clock.tick(30)

    # Vẽ nút replay và thoát
    win.fill((255, 255, 255))  # Fill màn hình thành màu trắng để vẽ nút
    draw_button("Replay", 150, 200, 100, 50, GREEN)
    draw_button("Exit", 550, 200, 100, 50, RED)
    pygame.display.update()

    # Xử lý sự kiện nút
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 150 <= mouse_pos[0] <= 250 and 200 <= mouse_pos[1] <= 250:
                    main()
                elif 550 <= mouse_pos[0] <= 650 and 200 <= mouse_pos[1] <= 250:
                    pygame.quit()
                    sys.exit()

# Chạy trò chơi
if __name__ == "__main__":
    main()
