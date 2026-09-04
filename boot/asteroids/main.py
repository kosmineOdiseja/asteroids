import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from logger import log_event
import sys
from shot import Shot

def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable, )
	Shot.containers = (shots, updatable, drawable)
	asteroid_field = AsteroidField()

	Player.containers = (updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

	dt = 0.0

	while True:
		log_state()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black")

		# collision detection
		updatable.update(dt)

		for asteroid in asteroids:
			if player.collides_with(asteroid):
				log_event("player_hit")
				print("Game over!")
				sys.exit()
			for shot in shots:
				if shot.collides_with(asteroid):
					log_event("asteroid_shot")
					shot.kill()
					# asteroid.kill()
					asteroid.split()

		for obj in drawable:
			obj.draw(screen)

		pygame.display.flip()

		# limit the framerate to 60 FPS
		dt = clock.tick(60) / 1000

if __name__ == "__main__":
	main()
