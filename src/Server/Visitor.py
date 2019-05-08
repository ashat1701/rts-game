from .ActionBuilder import ActionBuilder


# import AnimationSet


class Visitor:
    def visit_player(self, entity, player=1):
        if player == 1:
            ab = ActionBuilder().set_position(entity.get_box().topleft).set_type("player")
            return ab
        if player == 0:
            return ActionBuilder().set_position(entity.get_box().topleft).set_type("PLAYER2")

    def visit_melee_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("MELEE_ENEMY")

    def visit_ranged_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("RANGED_ENEMY")

    def visit_projectile(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("PROJECTILE")
