from .pottery import RedisDictWrapper


class Karma:
    def __init__(self, users: RedisDictWrapper):
        self.users = users

    def increment(self, user_id: int, amount=1):
        karma_level = self.users.sub_get(user_id, 'karma_level')
        actual_karma = karma_level if karma_level is not None else 0
        new_amount = actual_karma + amount
        self.users.sub_set(user_id, 'karma_level', new_amount)
        return new_amount

    def decrement(self, user_id: int, amount=1):
        return self.increment(user_id, amount=-abs(amount))

    def set(self, user_id: int, amount: int):
        self.users.sub_set(user_id, 'karma_level', amount)

    def get(self, user_id: int):
        karma_level = self.users.sub_get(user_id, 'karma_level')
        return karma_level if karma_level is not None else 0

    def reset(self, user_id: int):
        self.users.sub_delete(user_id, 'karma_level')
