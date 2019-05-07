from .WorldState import World


class DamageSystem:

    def deal_damage(self, attacker_id, receiver_id):
        new_health = World.get_health(receiver_id) - World.get_damage(attacker_id)
        if new_health > 0:
            World.set_health(receiver_id, new_health)
        else:
            World.delete_entity(receiver_id)
