from .SpawnSystem import SpawnSystem
from .GeometrySystem import GeometrySystem
from .DamageSystem import DamageSystem
from .AnimationSystem import AnimationSystem
from .WorldState import World
from .Entity import Projectile
from time import time


class Logic:
    def __init__(self):
        self.spawn_system = SpawnSystem()
        self.geometry_system = GeometrySystem()
        self.damage_system = DamageSystem()
        self.animation_system = AnimationSystem()

    # move в Logic должен разумно вызывать move GeometrySystem в зависимости от WorldState
    # move в GeometrySystem должен обновлять состояние мира
    # move у Entity - просто делает сдвигает в указанном направлении
    def move(self, entity_id, direction=None):
        box = World.get_box(entity_id)
        if direction is None:
            direction = World.get_direction(entity_id)
        World.set_direction(entity_id, direction)
        dx, dy = [i * World.get_velocity(entity_id) for i in direction]
        temp_box = box.move(dx, dy)

        # PROJECTILES
        if isinstance(World.entity[entity_id], Projectile):
            # Если снаряд попал в стену, то его нужно удалить
            if self.geometry_system.collide_with_wall(temp_box):
                World.delete_entity(entity_id)
                return

            # Если наш projectile пересекается с другим entity
            for other_entity_id in World.entity.values():
                if self.geometry_system.collide(World.get_box(entity_id), World.get_box(other_entity_id)) \
                        and entity_id != other_entity_id:
                    self.damage_system.deal_damage(entity_id, other_entity_id)
                    World.delete_entity(entity_id)

        # NOT-PROJECTILE
        if self.geometry_system.collide_with_wall(temp_box):
            if self.geometry_system.collide_with_wall(temp_box):
                return
            for other_entity_id in World.entity.values():
                if self.geometry_system.collide(World.get_box(entity_id), World.get_box(other_entity_id)) \
                        and entity_id != other_entity_id:
                    return

        # Если никто ни в кого не врезался - двигаем
        World.set_box(entity_id, temp_box)

    def move_all_entities(self):
        for entity_id in World.movable_entities:
            # Если entity не начал атаку
            if World.get_last_attack(entity_id) is None:
                self.move(entity_id)

    # TODO: different attack types (Melee/Ranged)
    def attack(self, entity_id):
        for other_entity_id in self.geometry_system.get_attackable_entites(entity_id):
            self.damage_system.deal_damage(entity_id, other_entity_id)

    def all_npc_start_attack(self):
        for entity_id in World.enemies:
            if World.get_last_attack(entity_id) is not None:
                if time() - World.get_last_attack(entity_id) > World.get_attack_reload(entity_id):
                    self.attack(entity_id)
                    World.set_last_attack(entity_id, None)
            else:
                World.set_last_attack(entity_id, time())

