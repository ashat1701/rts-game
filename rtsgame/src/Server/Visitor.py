from rtsgame.src.Server.WorldState import world
from rtsgame.src.utility.constants import PLAYER_HEALTH
from .ActionBuilder import ActionBuilder


class Visitor:
    def visit_player(self, entity):
        return (ActionBuilder().set_position(
            entity.get_box().topleft).set_type("player" + str(entity.get_id() + 1))
                .set_hp(world.get_health(entity.get_id()), PLAYER_HEALTH))

    def visit_melee_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "melee")

    def visit_ranged_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "range")

    def visit_projectile(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "projectile")
