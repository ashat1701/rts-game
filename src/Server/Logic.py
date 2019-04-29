from src.Server.SpawnSystem import SpawnSystem
from src.Server.GeometrySystem import GeometrySystem
from src.Server.DamageSystem import DamageSystem
from src.Server.Animation import AnimationSystem
from src.Server.WorldState import World
import src.Entity
from src.utility.constants import FREE_SPACE, WALL


class Logic:
    def __init__(self):
        self.spawn_system = SpawnSystem()
        self.geometry_system = GeometrySystem()
        self.damage_system = DamageSystem()
        self.animation_system = AnimationSystem()

    def move(self, entity_id, direction=None):
        x, y = World.get_position(entity_id)
        if direction is None:
            direction = World.get_direction(entity_id)
        World.set_direction(entity_id, direction)
        dx, dy = [i * World.get_velocity(entity_id) for i in direction]
        if isinstance(World.entity[entity_id], src.Entity.Projectile) and World.map.get(x + dx, y + dy) > 0:  # if projectile hit some entity
            self.damage_system.deal_damage(entity_id, World.map.get(x + dx, y + dy))
            World.delete_entity(entity_id)
        if World.map.get(x + dx, y + dy) == FREE_SPACE:
            print("ХУЙ")
            self.geometry_system.move(entity_id)
        if World.map.get(x + dx, y + dy) == WALL:  # if we intersect the wall, we need to move as close as we can
            # move until he reach the wall
            pass

    def move_all_unplayable_entities(self):
        for entity in World.movable_entities:
            self.move(entity)
