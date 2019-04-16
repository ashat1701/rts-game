from abc import ABC, abstractmethod
import Entity
import constants

class EntityFactory(ABC):
    _id = -1
    # returns id
    @abstractmethod
    def create(self, *args) -> int:
        pass


class MoveableEntityFactory(EntityFactory):
    @abstractmethod
    def create(self, position: tuple, direction: tuple, moveable_entities: set, *args) -> int:
        pass

class ProjectileFactory(MoveableEntityFactory):
    def create(self, position: tuple, direction: tuple, projectiles: set, *args) -> int:
        EntityFactory._id += 1
        Entity.Projectile(position, EntityFactory._id, constants.PROJECTILE_VELOCITY, direction)
        return EntityFactory._id


class EnemyFactory(MoveableEntityFactory):
    @abstractmethod
    def create(self, position: tuple, direction: tuple, enemies: set, health: int, damage: int, *args) -> int:
        pass


