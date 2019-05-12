from .WorldState import world


class DamageSystem:

    def deal_damage(self, attacker_id, receiver_id):
        new_health = world.get_health(receiver_id) - world.get_damage(
            attacker_id)
        if new_health > 0:
            world.set_health(receiver_id, new_health)
        else:
            world.dead_entities.append(receiver_id)
