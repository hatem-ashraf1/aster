import random

from settings import MAP_HEIGHT, MAP_WIDTH


class MapLoader:
    def generate(self, level_number):
        rng = random.Random(level_number * 911)
        tiles = [["#" for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        rooms = []

        for _ in range(42):
            width = rng.randint(4, 8)
            height = rng.randint(3, 6)
            x = rng.randint(1, MAP_WIDTH - width - 2)
            y = rng.randint(1, MAP_HEIGHT - height - 2)
            room = (x, y, width, height)
            if any(self._intersects(room, other) for other in rooms):
                continue
            self._carve_room(tiles, room)
            if rooms:
                self._connect(tiles, self._center(rooms[-1]), self._center(room), rng)
            rooms.append(room)

        if not rooms:
            fallback = (2, 2, MAP_WIDTH - 4, MAP_HEIGHT - 4)
            self._carve_room(tiles, fallback)
            rooms.append(fallback)

        spawn = self._center(rooms[0])
        exit_pos = self._center(rooms[-1])
        items = self._place_items(tiles, rng, level_number, spawn, exit_pos)
        return {"tiles": tiles, "spawn": spawn, "exit": exit_pos, "items": items}

    @staticmethod
    def _intersects(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax <= bx + bw and ax + aw >= bx and ay <= by + bh and ay + ah >= by

    @staticmethod
    def _carve_room(tiles, room):
        x, y, width, height = room
        for row in range(y, y + height):
            for col in range(x, x + width):
                tiles[row][col] = "."

    @staticmethod
    def _center(room):
        x, y, width, height = room
        return x + width // 2, y + height // 2

    @staticmethod
    def _connect(tiles, a, b, rng):
        points = (a, b) if rng.choice((True, False)) else ((a[0], b[1]), (b[0], a[1]))
        current = a
        for target in points:
            while current[0] != target[0]:
                current = (current[0] + (1 if target[0] > current[0] else -1), current[1])
                tiles[current[1]][current[0]] = "."
            while current[1] != target[1]:
                current = (current[0], current[1] + (1 if target[1] > current[1] else -1))
                tiles[current[1]][current[0]] = "."

    @staticmethod
    def _place_items(tiles, rng, level_number, spawn, exit_pos):
        candidates = [
            (x, y)
            for y, row in enumerate(tiles)
            for x, tile in enumerate(row)
            if tile == "." and (x, y) not in (spawn, exit_pos)
        ]
        rng.shuffle(candidates)
        item_ids = ["health_potion", "damage_boost", "speed_boost"]
        if level_number == 1:
            item_ids.append("key")
        return [{"id": item_ids[i % len(item_ids)], "tile": candidates[i]} for i in range(min(4, len(candidates)))]
