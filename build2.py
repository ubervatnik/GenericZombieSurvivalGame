import random

# Chunk size, you can set whatever you want but some bugs may occur if you go more than 25.
chunk_size = 20

# Player's starting position
player_x, player_y = chunk_size // 2, chunk_size // 2

# Inventory
inventory = {'█': 5}

# List entities
enemies = []
survivors = []

# ANSI codes for colors, do not mess around.
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

# doesn't work [2]
def generate_chunk():
    return [['░' for _ in range(chunk_size)] for _ in range(chunk_size)]

# doesn't work 
world = generate_chunk()

# to spawn_entities
def spawn_entities(num, entity_list, symbol):
    for _ in range(num):
        while True:
            x, y = random.randint(0, chunk_size - 1), random.randint(0, chunk_size - 1)
            if world[y][x] == '░' and (x, y) != (player_x, player_y):
                entity_list.append({'x': x, 'y': y, 'symbol': symbol})
                break

# World
def print_world():
    for y in range(chunk_size):
        for x in range(chunk_size):
            if x == player_x and y == player_y:
                print(f'{RED}P{RESET}', end=' ')
            elif any(e['x'] == x and e['y'] == y for e in enemies):
                print(f'{GREEN}Z{RESET}', end=' ')
            elif any(s['x'] == x and s['y'] == y for s in survivors):
                print(f'{BLUE}S{RESET}', end=' ')
            else:
                print(world[y][x], end=' ')
        print()
    print(f"Inventory: {inventory}")

# Movement
def move_player(direction):
    global player_x, player_y, world
    new_x, new_y = player_x, player_y
    if direction == 'w':
        new_y -= 1
    elif direction == 's':
        new_y += 1
    elif direction == 'a':
        new_x -= 1
    elif direction == 'd':
        new_x += 1

    # this exists so you can't walk through the blocks.
    if 0 <= new_x < chunk_size and 0 <= new_y < chunk_size and world[new_y][new_x] == '░':
        player_x, player_y = new_x, new_y

    # again, things about chunks, DOESN'T WORK YET, there's some issues im trying to fix
    if player_x < 0 or player_x >= chunk_size or player_y < 0 or player_y >= chunk_size:
        player_x %= chunk_size
        player_y %= chunk_size
        world = generate_chunk()
        add_houses_and_roads()
        spawn_entities(5, enemies, 'Z')
        spawn_entities(3, survivors, 'S')

# Block placement
def place_block():
    if inventory['█'] > 0:
        world[player_y][player_x] = '█'
        inventory['█'] -= 1
    else:
        print("no solid blocks left in inventory!")

# To remove blocks
def remove_block():
    if world[player_y][player_x] != '░':
        inventory['█'] += 1
        world[player_y][player_x] = '░'

# enemies movement
def move_enemies():
    for enemy in enemies:
        direction = random.choice(['w', 'a', 's', 'd'])
        new_x, new_y = enemy['x'], enemy['y']
        if direction == 'w' and new_y > 0:
            new_y -= 1
        elif direction == 's' and new_y < chunk_size - 1:
            new_y += 1
        elif direction == 'a' and new_x > 0:
            new_x -= 1
        elif direction == 'd' and new_x < chunk_size - 1:
            new_x += 1

        if world[new_y][new_x] == '░':
            enemy['x'], enemy['y'] = new_x, new_y

# to see if you got killed by a zombie
def check_for_attacks():
    for enemy in enemies:
        if enemy['x'] == player_x and enemy['y'] == player_y:
            print("you've been killed by a zombie!")
            return True
    return False

# shooting
def shoot_zombie():
    global enemies
    direction = input("enter direction to shoot at (w/a/s/d): ")
    bullet_x, bullet_y = player_x, player_y
    while True:
        if direction == 'w':
            bullet_y -= 1
        elif direction == 's':
            bullet_y += 1
        elif direction == 'a':
            bullet_x -= 1
        elif direction == 'd':
            bullet_x += 1

        if bullet_x < 0 or bullet_x >= chunk_size or bullet_y < 0 or bullet_y >= chunk_size:
            break

        if any(enemy['x'] == bullet_x and enemy['y'] == bullet_y for enemy in enemies):
            enemies = [enemy for enemy in enemies if not (enemy['x'] == bullet_x and enemy['y'] == bullet_y)]
            print("Zombie killed!")
            break

# to add houses and roads
def add_houses_and_roads():
    for _ in range(3):  # Add 3 houses
        house_x, house_y = random.randint(0, chunk_size - 1), random.randint(0, chunk_size - 1)
        for i in range(house_y, min(house_y + 3, chunk_size)):
            for j in range(house_x, min(house_x + 3, chunk_size)):
                world[i][j] = '█'
    for _ in range(2):  # Add 2 roads
        road_x, road_y = random.randint(0, chunk_size - 1), random.randint(0, chunk_size - 1)
        if random.choice([True, False]):
            for i in range(road_y, min(road_y + 10, chunk_size)):
                world[i][road_x] = '▓'
        else:
            for j in range(road_x, min(road_x + 10, chunk_size)):
                world[road_y][j] = '▓'

# Add some initial blocks to the world
world[2][2] = '█'

# Add houses and roads
add_houses_and_roads()

# Spawn initial enemies and survivors
spawn_entities(5, enemies, 'Z')
spawn_entities(3, survivors, 'S')

# Main game
while True:
    print_world()
    command = input("press a key (w/a/s/d to move, p to place block, r to remove block, f to shoot, q to quit): ")
    if command in ['w', 'a', 's', 'd']:
        move_player(command)
        move_enemies()
        if check_for_attacks():
            break
    elif command == 'p':
        place_block()
    elif command == 'r':
        remove_block()
    elif command == 'f':
        shoot_zombie()
    elif command == 'q':
        break
    else:
        print("Invalid command!")

    # zombie spawn 
    if random.random() < 0.1:  # 10% chance to spawn a new zombie each turn
        spawn_entities(1, enemies, 'Z')
        
    # made by ubervatnik on GitHub, report bugs to game's GitHub.