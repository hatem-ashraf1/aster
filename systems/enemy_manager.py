"""
TODO:

Implement enemy lifecycle management.

Responsibilities:

- Spawn enemies when a level starts
- Store all active enemies
- Update every enemy each frame
- Remove defeated enemies
- Track remaining enemy count
- Support difficulty scaling

Spawning Rules:

- Enemies should not spawn on walls
- Enemies should not spawn too close to the player
- Higher levels should spawn more enemies

This system should act as the single source of truth for enemy management.

Other systems should request enemy information from this manager rather than
maintaining their own enemy collections.

Provide helper methods such as:

- spawn_enemies()
- update()
- draw()
- get_active_enemies()
- remove_enemy()

EnemyManager should cooperate with:

- CombatSystem
- Pathfinder
- LevelManager
- HUD
"""