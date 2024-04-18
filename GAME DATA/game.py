import sys
import math
import random
import os
import pygame

from scripts.utils import load_image, load_pngs, Animation
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

"""
Main game module that integrates various components like menu, gameplay
,and other game mechanics.
Utilizes pygame for rendering and managing game state, including entities,
tilemaps, and interactions.
"""


class Menu:
    """
    Represents the main menu of the game, providing options like starting
    the game, viewing tutorials,
    adjusting settings, or exiting the game.
    """

    def __init__(self):
        """
        Initializes the game's main menu, setting up the pygame window,
        loading fonts, setting up button colors,
        and loading background images and sounds.
        """
        pygame.init()
        pygame.display.set_caption("JUMPY")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()

        self.font_custom = pygame.font.Font(None, 70)
        self.white = (255, 255, 255)
        self.button_color = (155, 155, 155)
        self.hover_color = (130, 130, 130)
        self.quit_button_color = (255, 0, 0)
        self.quit_button_hover_color = (200, 0, 0)
        self.button_sound = pygame.mixer.Sound("data/sfx/click.wav")
        self.button_sound.set_volume(0.2)
        pygame.mixer.music.load("data/music.wav")
        self.bg_image = pygame.image.load(
            os.path.join("data", "pngs", "bg.png")
        ).convert_alpha()

    def draw_text(self, text, font, color, x, y):
        """
        Draws specified text on the screen at the given position.

        Parameters:
            text (str): The text to display.
            font (pygame.font.Font): The font used for the text.
            color (tuple): The color of the text.
            x (int): The x position of the text.
            y (int): The y position of the text.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, rect, color):
        """
        Draws a button with the specified text and color.

        Parameters:
            text (str): The text displayed on the button.
            rect (pygame.Rect): The rectangle defining the button's position
            and size.
            color (tuple): The color of the button.
        """
        # Vykreslení zaobleného obdélníku tlačítka
        pygame.draw.rect(self.screen, color, rect, border_radius=20)
        # Vykreslení textu na tlačítko
        self.draw_text(
            text, self.font_custom, self.white, rect.centerx, rect.centery
        )

    def level_selection(self):
        """
        Displays the level selection menu, allowing the player to choose a
        game level.

        Returns:
        int: The number of the selected level.
        """
        self.screen.blit(self.bg_image, (0, 0))
        button_width = 300
        button_height = 90

        level_1_button = pygame.Rect(
            1920 // 2 - button_width // 2, 400, button_width, button_height
        )
        level_2_button = pygame.Rect(
            1920 // 2 - button_width // 2, 500, button_width, button_height
        )
        level_3_button = pygame.Rect(
            1920 // 2 - button_width // 2, 600, button_width, button_height
        )

        running = True
        while running:
            mx, my = pygame.mouse.get_pos()

            self.draw_button(
                "Level 1",
                level_1_button,
                (
                    self.hover_color
                    if level_1_button.collidepoint((mx, my))
                    else self.button_color
                ),
            )
            self.draw_button(
                "Level 2",
                level_2_button,
                (
                    self.hover_color
                    if level_2_button.collidepoint((mx, my))
                    else self.button_color
                ),
            )
            self.draw_button(
                "Level 3",
                level_3_button,
                (
                    self.hover_color
                    if level_3_button.collidepoint((mx, my))
                    else self.button_color
                ),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if level_1_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        return 1
                    elif level_2_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        return 2
                    elif level_3_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        return 3
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.run()
            pygame.display.update()

    def run(self):
        """
        The main loop for the game menu, handling button interactions
        and transitioning to other game states like
        tutorial, settings, or starting the game.
        """
        button_width = 300
        button_height = 90

        while True:
            self.screen.blit(self.bg_image, (0, 0))
            self.draw_text(
                "Jumpy", self.font_custom, self.white, 1920 // 2, 300
            )
            mx, my = pygame.mouse.get_pos()

            play_button = pygame.Rect(
                1920 // 2 - button_width // 2, 400, button_width, button_height
            )
            tutorial_button = pygame.Rect(
                1920 // 2 - button_width // 2, 500, button_width, button_height
            )
            settings_button = pygame.Rect(
                1920 // 2 - button_width // 2, 600, button_width, button_height
            )
            quit_button = pygame.Rect(
                1920 // 2 - button_width // 2, 700, button_width, button_height
            )

            play_hovered = play_button.collidepoint((mx, my))
            tutorial_hovered = tutorial_button.collidepoint((mx, my))
            settings_hovered = settings_button.collidepoint((mx, my))
            quit_hovered = quit_button.collidepoint((mx, my))

            self.draw_button(
                "Play",
                play_button,
                self.hover_color if play_hovered else self.button_color,
            )
            self.draw_button(
                "Tutorial",
                tutorial_button,
                self.hover_color if tutorial_hovered else self.button_color,
            )
            self.draw_button(
                "Settings",
                settings_button,
                self.hover_color if settings_hovered else self.button_color,
            )
            self.draw_button(
                "Quit Game",
                quit_button,
                (
                    self.quit_button_hover_color
                    if quit_hovered
                    else self.quit_button_color
                ),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        selected_level = self.level_selection()
                        if selected_level is not None:
                            game = Game(start_level=selected_level - 1)
                            game.run()
                        self.state = "level_selection"
                    elif quit_button.collidepoint((mx, my)):
                        pygame.quit()
                        sys.exit()
                    elif tutorial_button.collidepoint((mx, my)):
                        self.show_tutorial()
                    elif settings_button.collidepoint((mx, my)):
                        self.show_settings()
            pygame.display.update()

    def show_tutorial(self):
        """
        Displays the game's tutorial, explaining controls and gameplay
          mechanics to the player.
        The tutorial screen features a grey background with text instructions,
        enhanced by a brown border around the text area.
        """
        self.screen.blit(self.bg_image, (0, 0))
        self.button_sound.play()
        button_width = 300
        button_height = 90
        tutorial_text = [
            "",
            "TUTORIAL:",
            "                                              ",
            "Arrow(UP)/Space - Jump",
            "  Arrows(L,R)/(A,D) - Movement  ",
            "X/(L-Shift) - Attack",
            "ESC - Exit",
        ]
        tutorial_font = pygame.font.Font(None, 40)
        tutorial_height = len(tutorial_text) * 40
        tutorial_width = max(
            [tutorial_font.size(line)[0] for line in tutorial_text]
        )
        tutorial_rect = pygame.Rect(
            1920 // 2 - tutorial_width // 2 - 10,
            1080 // 2 - tutorial_height // 2 - 10,
            tutorial_width + 20,
            tutorial_height + 20,
        )
        background_color = (128, 128, 128)
        border_color = (139, 69, 19)

        back_button = pygame.Rect(
            1920 // 2 - button_width // 2, 800, button_width, button_height
        )

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if back_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.button_sound.play()
                        running = False

            pygame.draw.rect(self.screen, border_color, tutorial_rect)
            inner_rect = tutorial_rect.inflate(-20, -20)
            pygame.draw.rect(self.screen, background_color, inner_rect)

            mx, my = pygame.mouse.get_pos()
            back_hovered = back_button.collidepoint((mx, my))
            self.draw_button(
                "Back",
                back_button,
                self.hover_color if back_hovered else self.button_color,
            )

            for i, line in enumerate(tutorial_text):
                self.draw_text(
                    line,
                    tutorial_font,
                    self.white,
                    1920 // 2,
                    1080 // 2 - tutorial_height // 2 + i * 40 + 10,
                )
            pygame.display.update()

    def adjust_sfx_volume(self, volume):
        """
        Adjusts the volume of sound effects (SFX) in the game.

        Parameters:
            volume (float): The desired volume level for SFX.
        """
        self.jump.set_volume(volume)
        self.dash.set_volume(volume)
        self.hit.set_volume(volume)
        self.shoot.set_volume(volume)
        self.ambience.set_volume(volume)

    def show_settings(self):
        """
        Displays the settings menu, allowing the player to adjust game
          settings such as sound volume.
        """
        self.button_sound.play()
        pygame.mixer.music.load("data/music.wav")
        pygame.mixer.music.play(loops=-1)
        self.jump = pygame.mixer.Sound("data/sfx/jump.wav")
        self.dash = pygame.mixer.Sound("data/sfx/dash.wav")
        self.hit = pygame.mixer.Sound("data/sfx/hit.wav")
        self.shoot = pygame.mixer.Sound("data/sfx/shoot.wav")
        self.ambience = pygame.mixer.Sound("data/sfx/ambience.wav")

        button_width, button_height = 300, 90
        volume_slider_width, volume_slider_height = 200, 20
        sfx_slider_width, sfx_slider_height = 200, 20
        volume_slider_x = 1920 // 2 - volume_slider_width // 2
        sfx_slider_x = 1920 // 2 - sfx_slider_width // 2
        volume_slider_y, sfx_slider_y = 400, 600

        music_volume, sfx_volume = 0.5, 0.5
        is_dragging_music, is_dragging_sfx = False, False

        hover_color = (130, 130, 130)
        volume_slider_rect = pygame.Rect(
            volume_slider_x,
            volume_slider_y,
            volume_slider_width,
            volume_slider_height,
        )
        sfx_slider_rect = pygame.Rect(
            sfx_slider_x, sfx_slider_y, sfx_slider_width, sfx_slider_height
        )

        running = True
        while running:
            self.screen.blit(self.bg_image, (0, 0))

            pygame.draw.rect(
                self.screen,
                self.button_color,
                (
                    volume_slider_x,
                    volume_slider_y,
                    volume_slider_width,
                    volume_slider_height,
                ),
            )
            pygame.draw.rect(
                self.screen,
                self.white,
                (
                    volume_slider_x + music_volume * volume_slider_width - 5,
                    volume_slider_y - 5,
                    10,
                    volume_slider_height + 10,
                ),
            )
            self.draw_text(
                "Music Volume", self.font_custom, self.white, 1920 // 2, 300
            )

            pygame.draw.rect(
                self.screen,
                self.button_color,
                (
                    sfx_slider_x,
                    sfx_slider_y,
                    sfx_slider_width,
                    sfx_slider_height,
                ),
            )
            pygame.draw.rect(
                self.screen,
                self.white,
                (
                    sfx_slider_x + sfx_volume * sfx_slider_width - 5,
                    sfx_slider_y - 5,
                    10,
                    sfx_slider_height + 10,
                ),
            )
            self.draw_text(
                "SFX Volume", self.font_custom, self.white, 1920 // 2, 500
            )

            mx, my = pygame.mouse.get_pos()
            back_button_rect = pygame.Rect(
                1920 // 2 - button_width // 2, 800, button_width, button_height
            )
            is_hovering_back = back_button_rect.collidepoint((mx, my))

            back_button_color = (
                hover_color if is_hovering_back else self.button_color
            )
            self.draw_button("Back", back_button_rect, back_button_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        self.button_sound.play()
                        pygame.mixer.music.stop()
                        running = False
                    elif volume_slider_rect.collidepoint(event.pos):
                        is_dragging_music = True
                    elif sfx_slider_rect.collidepoint(event.pos):
                        is_dragging_sfx = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    is_dragging_music = False
                    is_dragging_sfx = False
                elif event.type == pygame.MOUSEMOTION:
                    if is_dragging_music:
                        mouse_x, _ = event.pos
                        music_volume = max(
                            0,
                            min(
                                1,
                                (mouse_x - volume_slider_x)
                                / volume_slider_width,
                            ),
                        )
                        pygame.mixer.music.set_volume(music_volume)
                    if is_dragging_sfx:
                        mouse_x, _ = event.pos
                        sfx_volume = max(
                            0,
                            min(
                                1, (mouse_x - sfx_slider_x) / sfx_slider_width
                            ),
                        )
                        self.adjust_sfx_volume(sfx_volume)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.button_sound.play()
                        pygame.mixer.music.stop()
                        running = False
            pygame.display.update()


class Game:
    """
    Main game class, responsible for initializing the game environment,
    loading assets,
    and managing the game loop, including rendering and updating game states.
    """

    def __init__(self, start_level=0):
        """
        Initializes the game, setting up the display, loading assets,
        and preparing the game environment.
        """
        self.bg_image = pygame.image.load(
            os.path.join("data", "pngs", "bg.png")
        ).convert_alpha()
        self.font_custom = pygame.font.Font(None, 70)
        self.white = (255, 255, 255)
        self.button_color = (155, 155, 155)
        self.hover_color = (130, 130, 130)
        pygame.init()
        pygame.display.set_caption("JUMPY")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((640, 360))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.button_sound = pygame.mixer.Sound("data/sfx/click.wav")
        self.button_sound.set_volume(0.2)

        self.assets = {
            "decor": load_pngs("tiles/decor"),
            "grass": load_pngs("tiles/grass"),
            "sky": load_pngs("tiles/sky"),
            "large_decor": load_pngs("tiles/large_decor"),
            "stone": load_pngs("tiles/stone"),
            "player": load_image("entities/player.png"),
            "background": load_image("background.png"),
            "background2": load_image("background2.png"),
            "background3": load_image("background3.png"),
            "clouds": load_pngs("clouds"),
            "enemy/idle": Animation(
                load_pngs("entities/enemy/idle"), img_dur=6
            ),
            "enemy/run": Animation(load_pngs("entities/enemy/run"), img_dur=4),
            "player/idle": Animation(
                load_pngs("entities/player/idle"), img_dur=6
            ),
            "player/run": Animation(
                load_pngs("entities/player/run"), img_dur=4
            ),
            "player/jump": Animation(load_pngs("entities/player/jump")),
            "player/attack": Animation(
                load_pngs("entities/player/attack"), img_dur=1
            ),
            "player/attack2": Animation(
                load_pngs("entities/player/attack2"), img_dur=1
            ),
            "player/attack3": Animation(
                load_pngs("entities/player/attack3"), img_dur=1
            ),
            "player/wall_slide": Animation(
                load_pngs("entities/player/wall_slide")
            ),
            "particle/leaf": Animation(
                load_pngs("particles/leaf"), img_dur=20, loop=False
            ),
            "particle/drop": Animation(
                load_pngs("particles/drop"), img_dur=5, loop=True
            ),
            "particle/particle": Animation(
                load_pngs("particles/particle"), img_dur=6, loop=False
            ),
            "weapon1": load_image("weapon1.png"),
            "fireball": load_image("fireball.png"),
            "player/hit": Animation(
                load_pngs("entities/player/hit"), img_dur=5
            ),
        }
        self.sfx = {
            "jump": pygame.mixer.Sound("data/sfx/jump.wav"),
            "dash": pygame.mixer.Sound("data/sfx/dash.wav"),
            "hit": pygame.mixer.Sound("data/sfx/hit.wav"),
            "shoot": pygame.mixer.Sound("data/sfx/shoot.wav"),
            "ambience": pygame.mixer.Sound("data/sfx/ambience.wav"),
        }

        self.sfx["ambience"].set_volume(0.4)
        self.sfx["shoot"].set_volume(0.4)
        self.sfx["hit"].set_volume(0.15)
        self.sfx["dash"].set_volume(0.3)
        self.sfx["jump"].set_volume(0.4)

        pygame.mixer.music.load("data/music.wav")
        pygame.mixer.music.play(loops=-1)

        self.clouds = Clouds(self.assets["clouds"], count=16)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.level = 0
        self.load_level(self.level)
        self.fireball_hits = 0
        self.total_enemies = 0
        self.enemies_killed = 0
        self.lifes = 2
        self.level = start_level
        self.load_level(self.level)
        self.button_color = (155, 155, 155)
        self.exit_button_color = (255, 0, 0)
        self.exit_button_hover_color = (200, 0, 0)
        self.hover_color = (130, 130, 130)

    def draw_text(self, text, font, color, x, y):
        """
        Draws specified text on the screen at the given position.
        This method is needed for drawing button text.

        Parameters:
            text (str): The text to display.
            font (pygame.font.Font): The font used for the text.
            color (tuple): The color of the text.
            x (int): The x position of the text.
            y (int): The y position of the text.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, rect, color):
        """
        Draws a button with the specified text and color.
        This method mimics the one from the Menu class.

        Parameters:
            text (str): The text displayed on the button.
            rect (pygame.Rect): The rectangle defining the button's
            position and size.
            color (tuple): The color of the button.
        """
        pygame.draw.rect(self.screen, color, rect, border_radius=20)
        self.draw_text(
            text, self.font_custom, self.white, rect.centerx, rect.centery
        )

    def ingame_menu(self):
        """
        Displays the in-game menu, allowing the player to resume or exit to
        the main menu.
        """
        resume_button = pygame.Rect(1920 // 2 - 150, 400, 300, 90)
        exit_button = pygame.Rect(1920 // 2 - 150, 500, 300, 90)
        menu_active = True
        while menu_active:
            self.screen.blit(self.bg_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if resume_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        pygame.mixer.music.unpause()
                        return
                    elif exit_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        return "exit"

            mx, my = pygame.mouse.get_pos()

            button_width, button_height = 300, 90
            resume_button = pygame.Rect(
                1920 // 2 - button_width // 2, 400, button_width, button_height
            )
            exit_button = pygame.Rect(
                1920 // 2 - button_width // 2, 500, button_width, button_height
            )

            pygame.draw.rect(
                self.screen, self.button_color, resume_button, border_radius=20
            )
            pygame.draw.rect(
                self.screen,
                self.exit_button_color,
                exit_button,
                border_radius=20,
            )

            if resume_button.collidepoint((mx, my)):
                pygame.draw.rect(
                    self.screen,
                    self.hover_color,
                    resume_button,
                    border_radius=20,
                )
            if exit_button.collidepoint((mx, my)):
                pygame.draw.rect(
                    self.screen,
                    self.exit_button_hover_color,
                    exit_button,
                    border_radius=20,
                )

            self.draw_text(
                "Resume",
                self.font_custom,
                self.white,
                resume_button.centerx,
                resume_button.centery,
            )
            self.draw_text(
                "Exit to Menu",
                self.font_custom,
                self.white,
                exit_button.centerx,
                exit_button.centery,
            )

            pygame.display.flip()
            self.clock.tick(60)

    def game_over_screen(self):
        """
        Displays the game over screen and provides an option to return to the
        main menu.
        """
        running = True
        while running:
            self.screen.blit(self.bg_image, (0, 0))
            self.draw_text(
                "GAME OVER", self.font_custom, self.white, 1920 // 2, 400
            )

            mx, my = pygame.mouse.get_pos()

            button_width, button_height = 300, 90
            back_button = pygame.Rect(
                1920 // 2 - button_width // 2, 500, button_width, button_height
            )

            if back_button.collidepoint((mx, my)):
                pygame.draw.rect(
                    self.screen,
                    self.exit_button_hover_color,
                    back_button,
                    border_radius=20,
                )
                self.draw_text(
                    "EXIT",
                    self.font_custom,
                    self.white,
                    back_button.centerx,
                    back_button.centery,
                )
            else:
                self.button_sound.play()
                pygame.draw.rect(
                    self.screen,
                    self.exit_button_color,
                    back_button,
                    border_radius=20,
                )
                self.draw_text(
                    "EXIT",
                    self.font_custom,
                    self.white,
                    back_button.centerx,
                    back_button.centery,
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint((mx, my)):
                        self.button_sound.play()
                        return
            pygame.display.flip()
            self.clock.tick(60)

    def load_level(self, map_id):
        """
        Loads a game level based on the specified map ID, setting up the
        environment, entities, and objects.

        Parameters:
            map_id (int): The identifier for the map to load.
        """
        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.enem = []

        self.leaf_spawnerss = []
        for tree in self.tilemap.extract(
            [
                ("large_decor", 1),
                ("large_decor", 8),
                ("large_decor", 9),
                ("large_decor", 10),
                ("large_decor", 11),
                ("large_decor", 12),
                ("large_decor", 18),
                ("large_decor", 19),
                ("large_decor", 20),
            ],
            keep=True,
        ):
            self.leaf_spawnerss.append(
                pygame.Rect(1 + tree["pos"][0], 4 + tree["pos"][1], 30, 10)
            )

        self.drop_spawnerss = []
        for rock in self.tilemap.extract(
            [
                ("large_decor", 4),
                ("large_decor", 5),
                ("large_decor", 6),
                ("large_decor", 7),
            ],
            keep=True,
        ):
            self.drop_spawnerss.append(
                pygame.Rect(1 + rock["pos"][0], 4 + rock["pos"][1], 30, 10)
            )

        self.enem = []
        for spawners in self.tilemap.extract(
            [("spawners", 0), ("spawners", 1)]
        ):
            if spawners["variant"] == 0:
                self.player.pos = spawners["pos"]
                self.player.air_time = 0
            else:
                self.enem.append(Enemy(self, spawners["pos"], (8, 11)))
                self.total_enemies = len(self.enem)
                self.enemies_killed = 0
        print(f"Total enemies loaded for level {map_id}: {len(self.enem)}")

        self.fireball = []
        self.particles = []

        self.scroll = [0, 0]
        self.dead = 0

    def run(self):
        """
        Main game loop, handling events, updating game states, rendering the
        game world, and managing transitions.
        """
        self.sfx["ambience"].play(-1)
        pygame.mixer.music.play(loops=-1)
        while True:

            if self.level == 0:
                self.display.blit(self.assets["background"], (0, 0))
            elif self.level == 1:
                self.display.blit(self.assets["background2"], (0, 0))
            elif self.level == 2:
                self.display.blit(self.assets["background3"], (0, 0))

            if not len(self.enem):
                if self.level < 2:
                    self.level += 1
                    self.total_enemies = len(self.enem)
                    self.load_level(self.level)
                else:
                    pygame.mixer.music.stop()
                    self.game_over_screen()
                    break

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawnerss:
                if random.random() * 19999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            velocity=[-0.1, 0.2],
                            frame=random.randint(0, 15),
                        )
                    )

            for rect in self.drop_spawnerss:
                if random.random() * 19999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(self, "drop", pos, velocity=[0, 1])
                    )
            self.clouds.update()

            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enem.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enem.remove(enemy)
                    self.enemies_killed += 1

            if not self.dead:
                self.player.update(
                    self.tilemap, (self.movement[1] - self.movement[0], 0)
                )
                self.player.render(self.display, offset=render_scroll)

            for fireball in self.fireball.copy():
                fireball[0][0] += fireball[1]
                fireball[2] += 1
                img = self.assets["fireball"]
                self.display.blit(
                    img,
                    (
                        fireball[0][0]
                        - img.get_width() / 2
                        - render_scroll[0],
                        fireball[0][1]
                        - img.get_height() / 2
                        - render_scroll[1],
                    ),
                )
                if self.tilemap.solid_check(fireball[0]):
                    self.fireball.remove(fireball)
                elif fireball[2] > 360:
                    self.fireball.remove(fireball)
                if abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(fireball[0]):
                        self.fireball.remove(fireball)
                        self.fireball_hits += 1
                        self.lifes -= 1
                        self.sfx["hit"].play()
                        self.player.set_action("hit")

                        if self.fireball_hits >= 2:
                            self.dead = True
                            self.lifes = 2
                            self.fireball_hits = 0
                            for i in range(30):
                                angle = random.random() * 3.14 * 2
                                speed = random.random() * 5
                                self.particles.append(
                                    Particle(
                                        self,
                                        "particle",
                                        self.player.rect().center,
                                        velocity=[
                                            math.cos(angle + 3.14)
                                            * speed
                                            * 0.5,
                                            math.sin(angle + 3.14)
                                            * speed
                                            * 0.5,
                                        ],
                                        frame=random.randint(0, 7),
                                    )
                                )

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf" or "drop":
                    particle.pos[0] += (
                        math.sin(particle.animation.frame * 0.1) * 0.3
                    )
                if kill:
                    self.particles.remove(particle)

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0),
            )

            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        action = self.ingame_menu()
                        if action == "exit":
                            return
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        if self.player.jump():
                            self.sfx["jump"].play()
                    if event.key == pygame.K_x or event.key == pygame.K_LSHIFT:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False

            font = pygame.font.Font(None, 72)
            enemy_status = f"Kills: {self.enemies_killed}/{self.total_enemies}"
            text_surface = font.render(enemy_status, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(1880, 10))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 72)
            life_info_text = f"Lives: {self.lifes}/2"
            text_surface = font.render(life_info_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(1880, 80))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 72)
            life_info_text = f"LEVEL: {self.level + 1}"
            text_surface = font.render(life_info_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(230, 10))
            self.screen.blit(text_surface, text_rect)
            if self.dead == 1:
                self.lifes = 2
                self.fireball_hits = 0
            if self.enemies_killed + 1:
                pygame.display.update()
            else:
                pass


"""
Entry point of the game. This script initializes the main menu and the game
itself. The game loop continues to
execute, allowing the player to return to the main menu and restart the game
as often as desired. The loop
terminates only when a specific 'action' (e.g., 'exit') is returned from the
game, signaling the script to end.
The loop follows these steps:
1. Initializes and displays the game's main menu.
2. Waits for the user to navigate the menu and start the game.
3. Initializes the game and starts the game loop.
4. The game loop runs until an 'exit' action is returned.
5. If 'exit' is not returned, the loop starts over from step 1, allowing the
 player to play again or quit.
"""
if __name__ == "__main__":
    while True:
        menu = Menu()
        menu.run()
        game = Game()
        action = game.run()
        if action != "exit":
            break
