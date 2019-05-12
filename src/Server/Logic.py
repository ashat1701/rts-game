import logging
import os
from time import time

from .AnimationSystem import AnimationSystem
from .DamageSystem import DamageSystem
from .Entity import Enemy
from .Entity import Projectile
from .GeometrySystem import GeometrySystem
from .SpawnSystem import SpawnSystem
from .WorldState import world


class Logic:
    def __init__(self):
        self.spawn_system = SpawnSystem()
        self.geometry_system = GeometrySystem()
        self.damage_system = DamageSystem()
        self.animation_system = AnimationSystem()
        dirname = os.path.dirname(__file__)
        self.animation_system.load_entity_config(
            os.path.join(dirname, '../utility/animations/'
                                  'melee_animations.json'))
        self.animation_system.load_entity_config(
            os.path.join(dirname, '../utility/animations/'
                                  'player1_animations.json'))
        self.animation_system.load_entity_config(
            os.path.join(dirname, '../utility/animations/'
                                  'player2_animations.json'))

    # move в Logic должен разумно вызывать move GeometrySystem в зависимости от WorldState
    # move в GeometrySystem должен обновлять состояние мира
    # move у Entity - просто делает сдвигает в указанном направлении
    def move(self, entity_id, direction=None):
        if direction is None:
            direction = world.get_direction(entity_id)
        if direction == (0, 0):
            return
        world.set_direction(entity_id, direction)
        dx, dy = [i * world.get_velocity(entity_id) for i in direction]

        # PROJECTILES
        if isinstance(world.entity[entity_id], Projectile):
            temp_box = world.get_box(entity_id).move(dx, dy)
            # Если снаряд попал в стену, то его нужно удалить
            if self.geometry_system.collide_with_wall(temp_box):
                world.dead_entities.append(entity_id)
                return

            # Если наш projectile пересекается с другим entity
            for other_entity_id in world.entity.keys():
                if self.geometry_system.collide(temp_box,
                                                world.get_box(other_entity_id)) \
                        and entity_id != other_entity_id:
                    self.damage_system.deal_damage(entity_id, other_entity_id)

        # NOT-PROJECTILE
        for delta_x, delta_y in [(dx, 0), (0, dy)]:
            temp_box = world.get_box(entity_id).move(delta_x, delta_y)
            if self.geometry_system.collide_with_wall(temp_box):
                continue

            for other_entity_id in world.entity.keys():
                if (self.geometry_system.collide(temp_box, world.get_box(
                        other_entity_id))
                        and entity_id != other_entity_id):
                    break
            else:
                # Если никто ни в кого не врезался - двигаем
                world.set_box(entity_id, temp_box)

    def move_all_entities(self):
        for entity_id in world.movable_entities:
            # Если entity не начал атаку
            if world.get_last_attack(entity_id) is None:
                self.move(entity_id)
                self.animation_system.continue_or_reset_move_animation(
                    entity_id,
                    world.get_direction(entity_id))

    # TODO: different attack types (Melee/Ranged)
    def attack(self, entity_id):
        for other_entity_id in self.geometry_system.get_attackable_entites(
                entity_id):
            self.damage_system.deal_damage(entity_id, other_entity_id)

    def update_attack_state(self):
        for entity_id in world.entity.keys():
            if world.get_last_attack(entity_id) is not None:
                if time() - world.get_last_attack(
                        entity_id) > world.get_attack_reload(entity_id):
                    self.attack(entity_id)
                    world.set_last_attack(entity_id, None)
                    self.animation_system.continue_or_reset_move_animation(
                        entity_id, world.get_direction(entity_id)
                    )

            if isinstance(world.entity[entity_id], Enemy) and len(
                    self.geometry_system.get_attackable_entites(
                        entity_id)) > 0:
                if world.get_last_attack(entity_id) is None:
                    self.start_attack(entity_id,
                                      world.get_direction(entity_id))

    def update_enemies_direcion(self):
        for entity_id in world.enemies:
            if entity_id not in world.dead_entities:
                self.geometry_system.find_aim(entity_id)
                world.set_direction(entity_id,
                                    self.geometry_system.generate_npc_movement(
                                        entity_id))

    def start_attack(self, id_, direction):
        if world.get_last_attack(id_) is not None:
            return
        attack_anim = self.animation_system.get_attack_animation(id_,
                                                                 direction)

        self.animation_system.reset_animation(id_, attack_anim)
        world.set_last_attack(id_, time())
        logging.info("Entity {} attacked".format(id_))
