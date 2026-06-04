import pygame

from entities.player import Player
from levels.level_manager import LevelManager
from settings import BLACK, FPS, MAX_LEVEL, SCREEN_HEIGHT, SCREEN_WIDTH
from systems.collision import CollisionSystem
from systems.combat import CombatSystem
from systems.enemy_manager import EnemyManager
from systems.inventory import Inventory
from systems.pathfinding import Pathfinder
from ui.hud import HUD
from ui.menu import Menu
from utils.save_system import SaveSystem


MAIN_MENU = "MAIN_MENU"
PLAYING = "PLAYING"
PAUSED = "PAUSED"
GAME_OVER = "GAME_OVER"
VICTORY = "VICTORY"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Aster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MAIN_MENU

        self.level_manager = LevelManager()
        self.collision = CollisionSystem(self.level_manager)
        self.pathfinder = Pathfinder(self.level_manager)
        self.combat = CombatSystem()
        self.enemy_manager = EnemyManager()
        self.inventory = Inventory()
        self.hud = HUD()
        self.save_system = SaveSystem()
        self.projectiles = []
        self.player = None

        self.menus = {
            MAIN_MENU: Menu("Aster", [("New Game", "new"), ("Load Game", "load"), ("Quit", "quit")]),
            PAUSED: Menu("Paused", [("Resume", "resume"), ("Save Game", "save"), ("Main Menu", "menu")]),
            GAME_OVER: Menu("Game Over", [("Restart", "new"), ("Main Menu", "menu"), ("Quit", "quit")]),
            VICTORY: Menu("Victory", [("Play Again", "new"), ("Main Menu", "menu"), ("Quit", "quit")]),
        }

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            if self.state == PLAYING:
                self.update(dt)
            self.draw()

    def start_new_game(self):
        self.inventory.clear()
        self.projectiles.clear()
        self.load_level(1)
        self.state = PLAYING

    def load_level(self, level_number):
        self.level_manager.load_level(level_number)
        self.collision = CollisionSystem(self.level_manager)
        self.pathfinder = Pathfinder(self.level_manager)
        self.player = Player(self.level_manager.spawn)
        self.enemy_manager.spawn_enemies(self.level_manager, self.player)
        self.projectiles.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state == PLAYING:
                self._handle_playing_event(event)
            else:
                action = self.menus[self.state].handle_event(event)
                if action:
                    self._run_menu_action(action)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.collision)
        self.collision.collect_items(self.player, self.inventory)

        for projectile in self.projectiles:
            projectile.update(dt)
            if self.collision.projectile_hit_wall(projectile):
                projectile.alive = False
                continue
            for enemy in self.enemy_manager.get_active_enemies():
                if self.collision.projectile_hits_enemy(projectile, enemy):
                    self.combat.apply_damage(enemy, projectile.damage)
                    projectile.alive = False
                    break
        self.projectiles = [projectile for projectile in self.projectiles if projectile.alive]

        self.enemy_manager.update(dt, self.player, self.pathfinder, self.collision, self.combat)
        if self.player.health <= 0:
            self.state = GAME_OVER
        elif not self.enemy_manager.get_active_enemies() and self.level_manager.is_exit_reached(self.player):
            self._advance_level()

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == PLAYING:
            self.level_manager.draw(self.screen)
            for projectile in self.projectiles:
                projectile.draw(self.screen)
            self.enemy_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.hud.draw(
                self.screen,
                self.player,
                self.level_manager.level_number,
                len(self.enemy_manager.get_active_enemies()),
                self.inventory,
            )
        else:
            self.menus[self.state].draw(self.screen)
        pygame.display.flip()

    def _handle_playing_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.state = PAUSED
        elif event.key == pygame.K_SPACE:
            projectile = self.player.shoot()
            if projectile:
                self.projectiles.append(projectile)
        elif event.key == pygame.K_F5:
            self.save_system.save(self)
        elif event.key == pygame.K_F9:
            self.load_saved_game()

    def _run_menu_action(self, action):
        if action == "new":
            self.start_new_game()
        elif action == "load":
            self.load_saved_game()
        elif action == "quit":
            self.running = False
        elif action == "resume":
            self.state = PLAYING
        elif action == "save":
            if self.player:
                self.save_system.save(self)
            self.state = PLAYING
        elif action == "menu":
            self.state = MAIN_MENU

    def load_saved_game(self):
        data = self.save_system.load()
        if not data:
            self.start_new_game()
            return
        self.inventory.from_dict(data.get("inventory", {}))
        self.load_level(int(data.get("level", 1)))
        self.save_system.restore_player(self.player, data)
        self.state = PLAYING

    def _advance_level(self):
        next_level = self.level_manager.level_number + 1
        if next_level > MAX_LEVEL:
            self.state = VICTORY
            return
        previous_health = self.player.health
        previous_damage = self.player.damage
        previous_speed = self.player.speed
        self.load_level(next_level)
        self.player.health = min(self.player.max_health, previous_health + 20)
        self.player.damage = previous_damage
        self.player.speed = previous_speed
