from .ActionBuilder import ActionBuilder
# import AnimationSet

# TODO: Гриша, может быть перенсети AnimationSet к Entity???


class Visitor:
    def visit_player(self, entity, player=1):
        if player == 1:
            ActionBuilder().set_box(entity.get_box()).set_type("PLAYER1").set_animation_state(
                entity.get_animation_state()).get_action()  # пока что нет get_animation_state - это надо переделать

        if player == 0:
            ActionBuilder().set_box(entity.get_box()).set_type("PLAYER2").set_animation_state(
                entity.get_animation_state()).get_action()

    def visit_melee_enemy(self, entity):
        return ActionBuilder().set_box(entity.get_box()).set_type("MELEE_ENEMY").get_action()  # TODO: add animation

    def visit_ranged_enemy(self, entity):
        return ActionBuilder().set_box(entity.get_box()).set_type("RANGED_ENEMY").get_action()

    def visit_projectile(self, entity):
        return ActionBuilder().set_box(entity.get_box()).set_type("PROJECTILE").get_action()
