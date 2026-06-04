class CombatSystem:
    def apply_damage(self, target, amount):
        target.health = max(0, target.health - amount)
        return target.health <= 0

    def enemy_attack(self, enemy, player, dt):
        enemy.attack_timer = max(0, enemy.attack_timer - dt)
        if enemy.attack_timer == 0 and enemy.can_attack(player):
            self.apply_damage(player, enemy.damage)
            enemy.attack_timer = enemy.attack_cooldown
            return True
        return False
