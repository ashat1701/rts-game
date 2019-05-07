from .ActionBuilder import ActionBuilder


# import AnimationSet


class Visitor:
    def visit_player(self, entity, player=1):
        if player == 1:
            ActionBuilder().set_position(entity.get_box().topleft).set_type("PLAYER1")
        if player == 0:
            ActionBuilder().set_position(entity.get_box().topleft).set_type("PLAYER2")

    def visit_melee_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("MELEE_ENEMY")

    def visit_ranged_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("RANGED_ENEMY")

    def visit_projectile(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type("PROJECTILE")
