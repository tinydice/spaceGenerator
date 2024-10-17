from world import World
from world_drawer import *
from config import *

def test_generate_world(weights, random_seed):
    world_drawer = WorldDrawer()
    world = World(WORLD_X, WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(weights)
    world_drawer.draw(tile_map, wait_for_key = True)