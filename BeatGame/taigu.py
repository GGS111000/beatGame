import pygame
import sys
import random
import time
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
HIT_OBJECT_SIZE = 20
HIT_OBJECT_COLOR = (255, 0, 0)
HIT_OBJECT_SPEED = 3
LINE_X = 100
LINE_Y = SCREEN_HEIGHT // 2 - HIT_OBJECT_SIZE // 2
LINE_WIDTH = 10
LINE_COLOR = (0, 255, 0)
SCORE_POS = (10, 10)
FONT_SIZE = 32
BPM = 83
WIN_AREA_WIDTH = 30
HIT_OBJECT_SCORED_COLOR = (255, 255, 0)

# Load assets
music_file = "far.ogg"
pygame.mixer.music.load(music_file)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Initialize font
font = pygame.font.Font(None, FONT_SIZE)

# Calculate the time interval between beats
beat_interval = 60 / BPM


class HitObject:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.counted = False
        self.scored = False

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        color = self.color if not self.scored else HIT_OBJECT_SCORED_COLOR
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)

    def clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return (dx * dx + dy * dy) <= self.size * self.size


class Firework:
    def __init__(self, x, y, size, color, duration):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.duration = duration
        self.particles = []

    def generate_particles(self):
        angle_step = 360 // self.size
        for angle in range(0, 360, angle_step):
            dx = self.size * math.cos(math.radians(angle))
            dy = self.size * math.sin(math.radians(angle))
            self.particles.append([self.x + dx, self.y + dy, dx / 10, dy / 10])

    def update(self):
        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(
                surface, self.color, (int(particle[0]), int(particle[1])), 2
            )


def main():
    clock = pygame.time.Clock()
    hit_objects = []
    score = 0
    fireworks = []

    pygame.mixer.music.play(-1)
    last_beat_time = time.time()

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in hit_objects:
                    if (
                        obj.clicked(event.pos)
                        and abs(obj.x - LINE_X) <= WIN_AREA_WIDTH // 2
                        and not obj.counted
                    ):
                        score += 10
                        obj.counted = True
                        obj.scored = True
                        firework = Firework(
                            obj.x,
                            obj.y,
                            20,
                            (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                            ),
                            50,
                        )
                        firework.generate_particles()
                        fireworks.append(firework)

        # Create new hit objects
        current_time = time.time()
        if current_time - last_beat_time >= beat_interval:
            new_hit_object = HitObject(
                SCREEN_WIDTH,
                LINE_Y,
                HIT_OBJECT_SIZE,
                HIT_OBJECT_COLOR,
                HIT_OBJECT_SPEED,
            )
            hit_objects.append(new_hit_object)
            last_beat_time = current_time

        # Update and draw hit objects
        for obj in hit_objects[:]:
            obj.update()
            obj.draw(screen)
            if obj.x < -obj.size:
                hit_objects.remove(obj)

        # Update and draw fireworks
        for firework in fireworks[:]:
            firework.update()
            firework.draw(screen)
            firework.duration -= 1
            if firework.duration <= 0:
                fireworks.remove(firework)

        # Draw the line
        pygame.draw.rect(
            screen, LINE_COLOR, (LINE_X, LINE_Y, LINE_WIDTH, HIT_OBJECT_SIZE )
        )

        # Draw the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, SCORE_POS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
