from perlin_noise import PerlinNoise
from config import *
import pygame

def generate_world(weights, random_seed):
    world_drawer = WorldDrawer()
    world = World(WORLD_X, WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(weights)
    world_drawer.draw(tile_map, wait_for_key = True)

class World():
    def __init__(self, size_x, size_y, random_seed):
        self.generate_noisemap(size_x, size_y, random_seed)

        flat_list = [item for sublist in self.noise_map for item in sublist]
        self.min_value = min(flat_list)
        self.max_value = max(flat_list)


    def generate_noisemap(self, size_x, size_y, random_seed):
        self.noise_map = []

        noise1 = PerlinNoise(octaves=3, seed=random_seed)
        noise2 = PerlinNoise(octaves=6, seed=random_seed)
        noise3 = PerlinNoise(octaves=12, seed=random_seed)
        noise4 = PerlinNoise(octaves=24, seed=random_seed)

        xpix, ypix = size_x + 1, size_y + 1
        for j in range(ypix):
            row = []
            for i in range(xpix):
                noise_val = noise1([i/xpix, j/ypix])
                noise_val += 0.5 * noise2([i/xpix, j/ypix])
                noise_val += 0.25 * noise3([i/xpix, j/ypix])
                noise_val += 0.125 * noise4([i/xpix, j/ypix])
                row.append(noise_val)
            self.noise_map.append(row)
    
    def get_tiled_map(self, weights):
        total_weights = sum(weights)
        total_range = self.max_value - self.min_value

        max_terrain_heights = []
        previous_height = self.min_value
        for terrain_type in ALL_TERRAIN_TYPES:
            height = total_range * (weights[terrain_type] / total_weights) + previous_height
            max_terrain_heights.append(height)
            previous_height = height
        max_terrain_heights[SNOW] = self.max_value

        map_int = []

        for row in self.noise_map:
            map_row = []
            for value in row:
                for terrain_type in ALL_TERRAIN_TYPES:
                    if value <= max_terrain_heights[terrain_type]:
                        map_row.append(terrain_type)
                        break

            map_int.append(map_row)

        return map_int

class WorldDrawer:

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.tilesheet = pygame.image.load(TILESHEET_PATH)

        self.terrain_tiles = []
        for terrain_type in ALL_TERRAIN_TYPES:
            tile_types = []
            for tile_pos in TERRAIN_TILES[terrain_type]:
                tile_types.append(self.tilesheet.subsurface((tile_pos[0], tile_pos[1], TILESIZE, TILESIZE)))
            self.terrain_tiles.append(tile_types)


    def draw(self, height_map, wait_for_key):
        self.draw_tiles(height_map)
        pygame.display.flip()
        if wait_for_key:
            self.wait_key()


    def wait_key(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                break


    def draw_tiles(self, terrain_type_map):
        for y, row in enumerate(terrain_type_map):
            for x, value in enumerate(row):

                if x == WORLD_X or y == WORLD_Y:
                    continue

                tile_corner_types = []
                tile_corner_types.append(terrain_type_map[y + 1][x + 1])
                tile_corner_types.append(terrain_type_map[y + 1][x])
                tile_corner_types.append(terrain_type_map[y][x + 1])
                tile_corner_types.append(terrain_type_map[y][x])

                for terrain_type in ALL_TERRAIN_TYPES:
                    if terrain_type in tile_corner_types:
                        tile_index = self.get_tile_index_for_type(tile_corner_types, terrain_type)
                        image = self.terrain_tiles[terrain_type][tile_index]
                        break
                self.display_surface.blit(image, (x * TILESIZE, y * TILESIZE))


    def get_tile_index_for_type(self, tile_corners, terrain_type):
        tile_index = 0
        for power, corner_type in enumerate(tile_corners):
                if corner_type == terrain_type:
                    tile_index += 2 ** power
        return tile_index
