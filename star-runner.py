from designer import *
from dataclasses import dataclass
from random import randint
import math
import time


class Rocks(Emoji):
    speed: float
    direction: int
    x: int
    y: int
    creation_time: float


@dataclass
class Game:
    '''
    Represents the game state with various attributes.
    '''
    character: DesignerObject
    character_speed: int
    character_speed_y: int
    stars: list[DesignerObject]
    comets: list[DesignerObject]
    lightning: list[DesignerObject]
    frenzy_list: list[DesignerObject]
    reset_powerup: list[DesignerObject]
    score: int
    rocks_list: list[Rocks]
    counter: DesignerObject
    speed_boost_active: bool
    speed_boost_start_time: float
    speed_boost_duration: float
    frenzy_active: bool
    frenzy_start_time: float
    frenzy_duration: float
    last_comet_scale_factor: float
    last_rock_speed_factor: float
    comet_scale_interval: int
    rock_speed_interval: int


def create_character() -> DesignerObject:
    '''
    Creates a character that is controlled by the user
    Returns:
        DesignerObject: The created character
    '''
    character = emoji('🛸')
    character.scale_x = 1.2
    character.scale_y = 1.2
    character.flip_x = True
    character.y = get_height() * (2 / 3)
    return character


def move_character(game: Game):
    '''
    Moves the character based on the game state.
    Args:
        game (Game): The game state
    '''
    if game.speed_boost_active and (time.time() - game.speed_boost_start_time) < game.speed_boost_duration:
        game.character.x += game.character_speed * 2  # Double speed during boost
    else:
        game.character.x += game.character_speed


def move_character_y(game: Game):
    '''
    Moves the character vertically based on the game state.
    Args:
        game (Game): The game state
    '''
    game.character.y -= game.character_speed_y


def move_left(game: Game):
    '''
    Moves the character to the left.
    Args:
        game (Game): The game state.
    '''
    characterspeed = 10
    game.character_speed = -characterspeed
    game.character.flip_x = True


def move_right(game: Game):
    '''
    Move the character to the right.
    Args:
        game (Game): The game state.
    '''
    characterspeed = 10
    game.character_speed = characterspeed
    game.character.flip_x = False


def move_up(game: Game):
    '''
    Move the character upwards.
    Args:
        game (Game): The game state.
    '''
    characterspeed_y = 10
    game.character_speed_y = characterspeed_y


def move_down(game: Game):
    '''
    Move the character downwards.
    Args:
        game (Game): The game state.
    '''
    characterspeed_y = -10
    game.character_speed_y = characterspeed_y


def change_direction(game: Game, key: str):
    '''
    Change the character's direction based on the provided key.
    Args:
        game (Game): The game state.
        key (str): The key representing the direction change.
    '''
    if key == 'left':
        move_left(game)
    if key == 'right':
        move_right(game)
    if key == 'up':
        move_up(game)
    if key == 'down':
        move_down(game)


def stop_character_movement(game: Game, key: str):
    '''
    Stop the character's movement based on the provided key.
    Args:
        game (Game): The game state.
        key (str): The key representing the movement direction to stop.
    '''
    if key == 'right' or key == 'left' or key == 'up' or key == 'down':
        game.character_speed = 0
        game.character_speed_y = 0


def opposite_entrance(game: Game):
    '''
    Teleport the character to the opposite side of the screen if it goes out of bounds.
    Args:
        game (Game): The game state.
    '''
    if game.character.x > get_width():
        game.character.x = 0
    elif game.character.x < 0:
        game.character.x = get_width()


def create_star() -> DesignerObject:
    '''
    Create a star object.
    Returns:
        DesignerObject: The created star object.
    '''
    star = emoji('🌟')
    star.scale_x = 1
    star.anchor = 'midtop'
    star.x = randint(0, get_width())
    star.y = 0
    return star


def create_reset_powerup() -> DesignerObject:
    '''
    Create a reset power-up object.
    Returns:
        DesignerObject: The created reset power-up object.
    '''
    reset = emoji('🔄')
    reset.x = randint(0, get_width())
    reset.y = 0
    return reset


def make_reset_powerup(game: Game):
    '''
    Create a reset power-up and add it to the game if conditions are met.
    Args:
        game (Game): The game state.
    '''
    limited_amt_of_resets = len(game.reset_powerup) < 3
    random_chance = randint(1, 600) == 300
    if random_chance and limited_amt_of_resets:
        game.reset_powerup.append(create_reset_powerup())


def make_star(game: Game):
    '''
    Create a star and add it to the game if conditions are met.
    Args:
        game (Game): The game state.
    '''
    limited_amt_of_stars = len(game.stars) < 9
    random_chance = randint(1, 75) == 50
    if random_chance and limited_amt_of_stars:
        game.stars.append(create_star())


def create_frenzy_powerup() -> DesignerObject:
    '''
    Create a frenzy power-up object.
    Returns:
        DesignerObject: The created frenzy power-up object.
    '''
    frenzy = emoji('💵')
    frenzy.scale_x = 1
    frenzy.anchor = 'midtop'
    frenzy.x = randint(0, get_width())
    frenzy.y = 0
    return frenzy


def make_frenzy_powerup(game: Game):
    '''
    Create a frenzy power-up and add it to the game if conditions are met.
    Args:
        game (Game): The game state.
    '''
    limited_amt_of_frenzies = len(game.frenzy_list) < 3
    random_chance = randint(1, 750) == 375
    if random_chance and limited_amt_of_frenzies:
        game.frenzy_list.append(create_frenzy_powerup())


def destroy_stars_on_ground(game: Game):
    '''
    Remove stars that have reached the bottom of the screen.
    Args:
        game (Game): The game state.
    '''
    kept_stars = []
    for star in game.stars:
        if star.y < get_height():
            kept_stars.append(star)
        else:
            destroy(star)
    game.stars = kept_stars


def create_comet() -> DesignerObject:
    '''
    Create a comet object.
    Returns:
        DesignerObject: The created comet object.
    '''
    comet = emoji('comet')
    comet.scale_x = 1.3
    comet.scale_y = 1.3
    comet.anchor = 'midtop'
    comet.x = randint(0, get_width())
    comet.y = 0
    return comet


def make_comet(game: Game):
    '''
    Create a comet and add it to the game if conditions are met.
    Args:
        game (Game): The game state.
    '''
    limited_amt_of_comets = len(game.stars) < 14
    random_chance = randint(1, 40) == 25
    if random_chance and limited_amt_of_comets:
        game.comets.append(create_comet())


def destroy_reset_on_ground(game: Game):
    '''
    Remove reset power-ups that have reached the bottom of the screen.
    Args:
        game (Game): The game state.
    '''
    kept_resets = []
    for reset in game.reset_powerup:
        if reset.y < get_height():
            kept_resets.append(reset)
        else:
            destroy(reset)
    game.reset_powerup = kept_resets


def destroy_lightning_on_ground(game: Game):
    '''
    Remove lightning objects that have reached the bottom of the screen.
    Args:
        game (Game): The game state.
    '''
    kept_lightning = []
    for lightning in game.lightning:
        if lightning.y < get_height():
            kept_lightning.append(lightning)
        else:
            destroy(lightning)
    game.lightning = kept_lightning


def destroy_comets_on_ground(game: Game):
    '''
    Remove comets that have reached the bottom of the screen.
    Args:
        game (Game): The game state.
    '''
    kept_comets = []
    for comet in game.comets:
        if comet.y < get_height():
            kept_comets.append(comet)
        else:
            destroy(comet)
    game.comets = kept_comets


def destroy_frenzy_on_ground(game: Game):
    '''
    Remove frenzy power-ups that have reached the bottom of the screen.
    Args:
        game (Game): The game state.
    '''
    kept_frenzies = []
    for frenzy in game.frenzy_list:
        if frenzy.y < get_height():
            kept_frenzies.append(frenzy)
        else:
            destroy(frenzy)
    game.frenzy_list = kept_frenzies


def generate_mass_stars(game: Game):
    '''
    Generate stars in mass during a frenzy period.
    Args:
        game (Game): The game state.
    '''
    if game.frenzy_active and (time.time() - game.frenzy_start_time) < game.frenzy_duration:
        game.stars.append(create_star())
    else:
        game.frenzy_active = False


def create_lightning() -> DesignerObject:
    '''
    Create a lightning object.
    Returns:
        DesignerObject: The created lightning object.
    '''
    lightning = emoji('⚡')
    lightning.x = randint(0, get_width())
    lightning.y = 0
    return lightning


def make_lightning(game: Game):
    '''
    Create lightning and add it to the game if conditions are met.
    Args:
        game (Game): The game state.
    '''
    limited_amt_of_lightning = len(game.lightning) < 2
    random_chance = randint(1, 300) == 100
    if random_chance and limited_amt_of_lightning:
        game.lightning.append(create_lightning())


def make_objects_drop(game: Game):
    '''
    Move game objects (stars, comets, lightning, frenzy power-ups, resets) downward.
    Args:
        game (Game): The game state.
    '''
    for star in game.stars:
        star.y += 8
    for comet in game.comets:
        comet.y += 8
    for lightning in game.lightning:
        lightning.y += 11
    for frenzy in game.frenzy_list:
        frenzy.y += 11
    for reset in game.reset_powerup:
        reset.y += 11


def collide_character_with_star(game: Game):
    '''
    Handle collisions between the character and stars.
    Args:
        game (Game): The game state.
    '''
    destroyed_stars = []
    for star in game.stars:
        if colliding(game.character, star):
            destroyed_stars.append(star)
            game.score += 1
    game.stars = filter_stars(game.stars, destroyed_stars)


def collide_character_with_lightning(game: Game):
    '''
    Handle collisions between the character and lightning.
    Args:
        game (Game): The game state.
    '''
    destroyed_lightning = []
    for lightning in game.lightning:
        if colliding(game.character, lightning):
            game.speed_boost_active = True
            game.speed_boost_start_time = time.time()
            destroyed_lightning.append(lightning)
    game.lightning = filter_lightning(game.lightning, destroyed_lightning)


def collide_character_with_comet(game: Game) -> bool:
    '''
    Check if the character collides with any comets.
    Args:
        game (Game): The game state.
    Returns:
        bool: True if a collision occurs, False otherwise.
    '''
    comet_collision = False
    for comet in game.comets:
        if colliding(game.character, comet):
            comet_collision = True
    return comet_collision


def collide_character_with_rock(game: Game) -> bool:
    '''
    Check if the character collides with any rocks.

    Args:
        game (Game): The game state.

    Returns:
        bool: True if a collision occurs, False otherwise.
    '''
    rock_collision = False
    for rock in game.rocks_list:
        if colliding(game.character, rock):
            rock_collision = True
    return rock_collision


def collide_character_with_frenzy(game: Game):
    '''
    Handle collisions between the character and frenzy power-ups.
    Args:
        game (Game): The game state.
    '''
    destroyed_frenzy = []
    for frenzy in game.frenzy_list:
        if colliding(game.character, frenzy):
            game.frenzy_active = True
            game.frenzy_start_time = time.time()
            destroyed_frenzy.append(frenzy)
    game.frenzy_list = filter_frenzies(game.frenzy_list, destroyed_frenzy)


def collide_character_with_reset(game: Game):
    '''
    Handle collisions between the character and reset power-ups.
    Args:
        game (Game): The game state.
    '''
    destroyed_resets = []
    for reset in game.reset_powerup:
        if colliding(game.character, reset):
            destroyed_resets.append(reset)
            game.last_comet_scale_factor = 1.3
            game.last_rock_speed_factor = 3.0
            for comet in game.comets:
                comet.scale_x = 1.3
                comet.scale_y = 1.3
            for rock in game.rocks_list:
                rock.speed = 3
    game.reset_powerup = filter_resets(game.reset_powerup, destroyed_resets)


def filter_resets(reset_list: list[DesignerObject], resets_not_to_keep: list[DesignerObject]) -> list[DesignerObject]:
    '''
    Filter out resets that should not be kept based on a list of resets not to keep.
    Args:
        reset_list (list[DesignerObject]): List of reset power-ups.
        resets_not_to_keep (list[DesignerObject]): List of resets that should be filtered out.
    Returns:
        list[DesignerObject]: New list of resets after filtering.
    '''
    new_reset_list = []
    for reset in reset_list:
        if reset in resets_not_to_keep:
            destroy(reset)
        else:
            new_reset_list.append(reset)
    return new_reset_list


def filter_lightning(lightning_list: list[DesignerObject], lightning_not_to_keep: list[DesignerObject]) -> list[
    DesignerObject]:
    '''
    Filter out lightning objects that should not be kept based on a list of lightning objects not to keep.
    Args:
        lightning_list (list[DesignerObject]): List of lightning objects.
        lightning_not_to_keep (list[DesignerObject]): List of lightning objects that should be filtered out.
    Returns:
        list[DesignerObject]: New list of lightning objects after filtering.
    '''
    new_lightning_list = []
    for lightning in lightning_list:
        if lightning in lightning_not_to_keep:
            destroy(lightning)
        else:
            new_lightning_list.append(lightning)
    return new_lightning_list


def filter_stars(stars_list: list[DesignerObject], stars_not_to_keep: list[DesignerObject]) -> list[DesignerObject]:
    '''
    Filter out stars that should not be kept based on a list of stars not to keep.
    Args:
        stars_list (list[DesignerObject]): List of stars.
        stars_not_to_keep (list[DesignerObject]): List of stars that should be filtered out.
    Returns:
        list[DesignerObject]: New list of stars after filtering.
    '''
    new_star_list = []
    for star in stars_list:
        if star in stars_not_to_keep:
            destroy(star)
        else:
            new_star_list.append(star)
    return new_star_list


def filter_frenzies(frenzy_list: list[DesignerObject], frenzy_not_to_keep: list[DesignerObject]) -> list[
    DesignerObject]:
    '''
    Filter out frenzy power-ups that should not be kept based on a list of frenzies not to keep.
    Args:
        frenzy_list (list[DesignerObject]): List of frenzy power-ups.
        frenzy_not_to_keep (list[DesignerObject]): List of frenzy power-ups that should be filtered out.
    Returns:
        list[DesignerObject]: New list of frenzy power-ups after filtering.
    '''
    new_frenzy_list = []
    for frenzy in frenzy_list:
        if frenzy in frenzy_not_to_keep:
            destroy(frenzy)
        else:
            new_frenzy_list.append(frenzy)
    return new_frenzy_list


def make_comets_bigger(game: Game):
    '''
    Make comets bigger based on the game score.
    Args:
        game (Game): The game state.
    '''
    base_comet_scale_factor = 1.05

    if game.score >= game.comet_scale_interval and game.score % game.comet_scale_interval == 0:
        game.last_comet_scale_factor = base_comet_scale_factor * (1 + game.score // game.comet_scale_interval)

    for comet in game.comets:
        comet.scale_x = game.last_comet_scale_factor
        comet.scale_y = game.last_comet_scale_factor


def create_rocks(character: DesignerObject) -> Rocks:
    '''
    Create rocks based on the character position.
    Args:
        character (DesignerObject): The character object.
    Returns:
        Rocks: The created rocks object.
    '''
    return Rocks('🪨', speed=3.0, direction=0, x=randint(0, get_width()), y=0, creation_time=time.time())


def move_rocks(game: Game):
    '''
    Move rocks based on the character's position.
    Args:
        game (Game): The game state.
    '''
    current_time = time.time()
    for rock in game.rocks_list:
        angle = get_angle(game.character, rock)
        delta_x = rock.speed * math.cos(math.radians(angle))
        delta_y = rock.speed * math.sin(math.radians(angle))
        rock.x -= delta_x
        rock.y -= delta_y

        # Check if the rock has existed for more than 10 seconds (adjust the threshold as needed)
        if current_time - rock.creation_time > 10:
            destroy(rock)
            game.rocks_list.remove(rock)


def make_rocks(game: Game):
    '''
    Generate rocks in the game based on certain conditions.
    Args:
        game (Game): The game state.
    '''
    if game.score > 15:
        limited_amt_of_rocks = len(game.rocks_list) < 6
        random_chance = randint(1, 100) == 25
        if random_chance and limited_amt_of_rocks:
            game.rocks_list.append(create_rocks(game.character))


def get_angle(first_object, second_object):
    '''
    Calculate the angle between two objects.
    Args:
        first_object: The first object.
        second_object: The second object.
    Returns:
        float: The angle between the two objects.
    '''
    delta_y = second_object.y - first_object.y
    delta_x = second_object.x - first_object.x
    return math.degrees(math.atan2(delta_y, delta_x)) % 360


def update_score(game: Game):
    '''
    Update the game score display.
    Args:
        game (Game): The game state.
    '''
    game.counter.text = "Score: " + str(game.score)


def set_background():
    '''
    Set the game background.
    '''
    background = background_image(
        "https://images.pexels.com/photos/957061/milky-way-starry-sky-night-sky-star-957061.jpeg?cs=srgb&dl=pexels-felix-mittermeier-957061.jpg&fm=jpg")


def flash_game_over(game: Game):
    '''
    Displays a game-over message based on the player's score.
    Args:
        game (Game): The game state
    '''
    if game.score < 10:
        game.counter.text = "Really? Thats the best you can do? FINAL SCORE: " + str(game.score)
    elif game.score < 30:
        game.counter.text = "Solid effort, but I know people who can do better. FINAL SCORE: " + str(game.score)
    elif game.score < 60:
        game.counter.text = "Not bad... for a rookie. FINAL SCORE: " + str(game.score)
    elif game.score < 70:
        game.counter.text = "Impressive. FINAL SCORE: " + str(game.score)
    elif game.score < 80:
        game.counter.text = "You are blowing my expectations. FINAL SCORE: " + str(game.score)
    elif game.score < 100:
        game.counter.text = "WOW! FINAL SCORE: " + str(game.score)
    elif game.score < 120:
        game.counter.text = "You are one of the greatest players this game has seen. FINAL SCORE" + str(game.score)


def create_game() -> Game:
    '''
    Creates the initial game state.
    Returns:
        Game: The initial game state
    '''
    return Game(create_character(), 0, 0, [], [], [], [], [], 0, [], text("white", 'Score:', 25, 400, 50), False, 0.0,
                7.0,
                False, 0.0, 3.0, 1.3, 3.0, 20, 30, )


when('starting', create_game)
when('updating', move_character)
when('updating', move_character_y)
when('updating', make_objects_drop)
when('updating', destroy_stars_on_ground)
when('updating', destroy_comets_on_ground)
when('updating', destroy_frenzy_on_ground)
when('updating', destroy_lightning_on_ground)
when('updating', destroy_reset_on_ground)
when('updating', opposite_entrance)
when('updating', make_star)
when('updating', make_comet)
when('updating', make_lightning)
when('updating', make_frenzy_powerup)
when('updating', make_rocks)
when('updating', make_reset_powerup)
when('starting', set_background)
when('updating', move_rocks)
when('updating', make_comets_bigger)
when('updating', collide_character_with_star)
when('updating', collide_character_with_lightning)
when('updating', collide_character_with_frenzy)
when('updating', collide_character_with_reset)
when('updating', generate_mass_stars)
when('done typing', stop_character_movement)
when('updating', update_score)
when('typing', change_direction)
when(collide_character_with_comet, flash_game_over, pause)
when(collide_character_with_rock, flash_game_over, pause)

start()






