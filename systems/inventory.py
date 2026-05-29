"""
TODO:

Implement player inventory management.

Responsibilities:

- Store collected items
- Add items to inventory
- Remove items from inventory
- Search for items
- Count collected items

Inventory Rules:

- Items should have unique identifiers
- Inventory should support stacking when appropriate
- Inventory data must be serializable for saving/loading

Possible collectible items:

- Health Potion
- Damage Boost
- Speed Boost
- Key

Provide helper methods such as:

- add_item()
- remove_item()
- has_item()
- get_item_count()
- clear()

The inventory system should notify the HUD whenever inventory contents change.

The save system should serialize inventory contents and restore them correctly.
"""
