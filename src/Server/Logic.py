from .SpawnSystem import SpawnSystem
from .GeometrySystem import GeometrySystem
from .DamageSystem import DamageSystem
from .AnimationSystem import AnimationSystem
from .WorldState import world
from .Entity import Projectile
from time import time


class Logic:
    def __init__(self):
        self.spawn_system = SpawnSystem()
        self.geometry_system = GeometrySystem()
        self.damage_system = DamageSystem()
        self.animation_system = AnimationSystem()
        self.animation_system.load_entity_config('utility/animations/'
                                                 'melee_animations.json')

    # move в Logic должен разумно вызывать move GeometrySystem в зависимости от WorldState
    # move в GeometrySystem должен обновлять состояние мира
    # move у Entity - просто делает сдвигает в указанном направлении
    def move(self, entity_id, direction=None):
        box = world.get_box(entity_id)
        if direction is None:
            direction = world.get_direction(entity_id)
        world.set_direction(entity_id, direction)
        dx, dy = [i * world.get_velocity(entity_id) for i in direction]
        temp_box = box.move(dx, dy)

        # PROJECTILES
        if isinstance(world.entity[entity_id], Projectile):
            # Если снаряд попал в стену, то его нужно удалить
            if self.geometry_system.collide_with_wall(temp_box):
                world.delete_entity(entity_id)
                return

            # Если наш projectile пересекается с другим entity
            for other_entity_id in world.entity.values():
                if self.geometry_system.collide(world.get_box(entity_id), world.get_box(other_entity_id)) \
                        and entity_id != other_entity_id:
                    self.damage_system.deal_damage(entity_id, other_entity_id)
                    world.delete_entity(entity_id)

        # NOT-PROJECTILE
        if self.geometry_system.collide_with_wall(temp_box):
            if self.geometry_system.collide_with_wall(temp_box):
                return
            for other_entity_id in world.entity.values():
                if self.geometry_system.collide(world.get_box(entity_id), world.get_box(other_entity_id)) \
                        and entity_id != other_entity_id:
                    return

        # Если никто ни в кого не врезался - двигаем
        world.set_box(entity_id, temp_box)

    def move_all_entities(self):
        for entity_id in world.movable_entities:
            # Если entity не начал атаку
            if world.get_last_attack(entity_id) is None:
                self.move(entity_id)

    # TODO: different attack types (Melee/Ranged)
    def attack(self, entity_id):
        for other_entity_id in self.geometry_system.get_attackable_entites(entity_id):
            self.damage_system.deal_damage(entity_id, other_entity_id)

    def all_npc_start_attack(self):
        for entity_id in world.enemies:
            if world.get_last_attack(entity_id) is not None:
                if time() - world.get_last_attack(entity_id) > world.get_attack_reload(entity_id):
                    self.attack(entity_id)
                    world.set_last_attack(entity_id, None)
            else:
                world.set_last_attack(entity_id, time())
