class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, amount=1):
        self.items[item_id] = self.items.get(item_id, 0) + amount

    def remove_item(self, item_id, amount=1):
        if self.items.get(item_id, 0) < amount:
            return False
        self.items[item_id] -= amount
        if self.items[item_id] <= 0:
            del self.items[item_id]
        return True

    def has_item(self, item_id):
        return self.items.get(item_id, 0) > 0

    def get_item_count(self, item_id):
        return self.items.get(item_id, 0)

    def count(self):
        return sum(self.items.values())

    def clear(self):
        self.items.clear()

    def to_dict(self):
        return dict(self.items)

    def from_dict(self, data):
        self.items = {str(key): int(value) for key, value in data.items()}
