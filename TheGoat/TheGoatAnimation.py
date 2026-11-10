import pygame
import random
import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bottom-Up ASCII Art Formation")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
FONT_SIZE = 10
font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)

class AsciiParticle:
    def __init__(self, target_x, target_y, char, color):
        self.target_x = target_x
        self.target_y = target_y
        self.text_surface = font.render(char, True, color)
        
        self.start_x = self.target_x + random.randint(-40, 40)
        self.start_y = HEIGHT + random.randint(50, 300) 
        self.x = self.start_x
        self.y = self.start_y
        
        self.current_frame = 0
        
        vertical_offset_delay = (HEIGHT - self.target_y) * 0.5

        self.start_delay = int(60 + vertical_offset_delay + random.randint(0, 15))
        

        self.total_frames = random.randint(120, 180) 
        
        self.is_active = False 
        self.is_settled = False 

    def update(self):
        self.current_frame += 1
        
        if self.current_frame < self.start_delay:
            return
            
        self.is_active = True
        movement_frame = self.current_frame - self.start_delay
        
        if movement_frame < self.total_frames:
            t = movement_frame / self.total_frames
            
            inv_t = 1.0 - t
            ease_t = 1.0 - (inv_t * inv_t * inv_t)
            
            self.x = self.start_x + (self.target_x - self.start_x) * ease_t
            self.y = self.start_y + (self.target_y - self.start_y) * ease_t
        else:
            self.x = self.target_x
            self.y = self.target_y
            self.is_settled = True

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.text_surface, (int(self.x), int(self.y)))

def load_ascii_particles(image_path):
    try:
        img = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")
        print("Make sure your Messi picture is in the same folder and named correctly.")
        sys.exit(1)

    max_size = 700
    img_rect = img.get_rect()
    if img_rect.width > max_size or img_rect.height > max_size:
        scale = min(max_size / img_rect.width, max_size / img_rect.height)
        img = pygame.transform.scale(img, (int(img_rect.width * scale), int(img_rect.height * scale)))

    img_rect = img.get_rect(center=(WIDTH//2, HEIGHT//2))
    particles = []
    
    step = FONT_SIZE - 2 

    for x in range(0, img.get_width(), step):
        for y in range(0, img.get_height(), step):
            color = img.get_at((x, y))
            
            if color.a < 50:
                continue
                
            brightness = (0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
            
            if brightness < 20:
                continue
                
            char_index = int((brightness / 255.0) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_index]
            
            screen_x = img_rect.x + x
            screen_y = img_rect.y + y
            
            particles.append(AsciiParticle(screen_x, screen_y, char, (color.r, color.g, color.b)))
    
    return particles

def main():
    image_path = "messi.jpg" 
    particles = load_ascii_particles(image_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for p in particles:
            p.update()
            p.draw(screen)

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()