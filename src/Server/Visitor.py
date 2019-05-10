from .ActionBuilder import ActionBuilder


class Visitor:
    def visit_player(self, entity):
        return ActionBuilder().set_position(
            entity.get_box().topleft).set_type("player")

    def visit_melee_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "melee")

    def visit_ranged_enemy(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "range")

    def visit_projectile(self, entity):
        return ActionBuilder().set_position(entity.get_box().topleft).set_type(
            "projectile")
