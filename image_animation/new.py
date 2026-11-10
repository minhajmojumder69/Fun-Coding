import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Image Formation")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Particle:
    def __init__(self, target_x, target_y, color):
        self.target_x = target_x
        self.target_y = target_y
        
        # --- SWIRL MATH (Polar Coordinates) ---
        cx, cy = WIDTH // 2, HEIGHT // 2
        dx = self.target_x - cx
        dy = self.target_y - cy
        self.target_radius = math.hypot(dx, dy)
        self.target_angle = math.atan2(dy, dx)
        
        self.start_radius = random.uniform(800, 1200)
        self.start_angle = math.pi + random.uniform(-0.5, 0.5) 
        
        while self.target_angle <= self.start_angle:
            self.target_angle += math.pi * 2
            
        self.target_angle += math.pi * 2 
        
        self.x = cx + math.cos(self.start_angle) * self.start_radius
        self.y = cy + math.sin(self.start_angle) * self.start_radius
        
        self.base_color = color
        self.color_diff = (
            min(255, color[0] + 150) - color[0],
            min(255, color[1] + 150) - color[1],
            min(255, color[2] + 150) - color[2]
        )
        self.color = self.base_color
        self.size = 1 
        
        self.current_frame = 0
        
        # --- THE FIX: TIGHTER TIMERS ---
        # Particles now wait a maximum of 0.5 seconds to start (was 1.5)
        self.start_delay = random.randint(0, 30) 
        # Travel time reduced to 1.0 - 1.6 seconds (was up to 2.5)
        self.total_frames = random.randint(60, 100) 
        
        self.shine_timer = random.randint(0, 300)
        self.shine_step = 0
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
            
            current_radius = self.start_radius + (self.target_radius - self.start_radius) * ease_t
            current_angle = self.start_angle + (self.target_angle - self.start_angle) * ease_t
            
            self.x = (WIDTH // 2) + math.cos(current_angle) * current_radius
            self.y = (HEIGHT // 2) + math.sin(current_angle) * current_radius
        else:
            self.x = self.target_x
            self.y = self.target_y
            self.is_settled = True
            
            # Optimized Diamond Shine
            self.shine_timer -= 1
            if self.shine_timer <= 0:
                self.shine_step += 1
                if self.shine_step < 30:
                    intensity = (self.shine_step / 30.0)
                    intensity *= intensity
                elif self.shine_step < 60:
                    intensity = (60 - self.shine_step) / 30.0
                    intensity *= intensity
                else:
                    self.shine_timer = random.randint(120, 360) 
                    self.shine_step = 0
                    self.color = self.base_color
                    return
                
                self.color = (
                    int(self.base_color[0] + self.color_diff[0] * intensity),
                    int(self.base_color[1] + self.color_diff[1] * intensity),
                    int(self.base_color[2] + self.color_diff[2] * intensity)
                )

    def draw(self, surface):
        if self.is_active:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))

def load_particles_from_image(image_path, sample_rate=1):
    """
    sample_rate=1 creates maximum density (1 particle per pixel).
    Applies a vertical pink-to-blue gradient matching the video.
    """
    try:
        image_path = "image_animation/replace.png"
        img = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")
        import sys
        sys.exit(1)

    img_rect = img.get_rect(center=(WIDTH//2, HEIGHT//2))
    particles = []
    
    # The gradient colors from the video
    top_color = (255, 255, 255)    # Vivid Pink
    bottom_color = (100, 150, 255) # Light Blue

    for x in range(0, img.get_width(), sample_rate):
        for y in range(0, img.get_height(), sample_rate):
            color = img.get_at((x, y))
            
            is_dark = color.r < 100 and color.g < 100 and color.b < 100
            is_not_transparent = color.a > 50
            
            if is_dark and is_not_transparent:
                screen_x = img_rect.x + x
                screen_y = img_rect.y + y
                
                # Calculate how far down the image this pixel is (0.0 to 1.0)
                ratio = y / img.get_height()
                
                # Blend the top and bottom colors based on the Y position
                r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
                g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
                b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
                gradient_color = (r, g, b)
                
                particles.append(Particle(screen_x, screen_y, gradient_color))
    
    return particles

def main():
    # Load particles from the source image
    image_path = "target_image.png" 
    particles = load_particles_from_image(image_path, sample_rate=1)
    
    # Setup for the final text fade-in
    font = pygame.font.SysFont("georgia", 36, italic=True)
    text_str = ""
    text_surface = font.render(text_str, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))
    text_alpha = 0 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Flag to check if all particles have reached their targets
        all_settled = True

        for p in particles:
            p.update()
            p.draw(screen)
            
            # If any particle is more than 1 pixel away, they aren't settled
            if not p.is_settled:
                all_settled = False

        # If the image has finished forming, fade in the text
        if all_settled:
            if text_alpha < 255:
                text_alpha += 2
            
            # Create a temporary surface to apply alpha (transparency) to the text
            alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            alpha_surface.blit(text_surface, (0, 0))
            alpha_surface.set_alpha(text_alpha)
            screen.blit(alpha_surface, text_rect)

        pygame.display.flip()
        clock.tick(60) # Lock to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()