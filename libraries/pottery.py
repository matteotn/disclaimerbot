from pottery import RedisDict, Redlock
from redis import Redis


class RedisDictWrapper:
    def __init__(self, redis_link: str, key: str):
        self.key = key
        conn = self.redis_init(redis_link)
        self.dict = RedisDict(redis=conn, key=key)

    def redis_init(self, redis_link: str):
        return Redis.from_url(redis_link)

    def get(self, key):
        return self.dict[key] if key in self.dict else None

    def set(self, key, value):
        self.dict[key] = value

    def sub_get(self, chatid, variable):
        with Redlock(key=self.key):
            if str(chatid) in self.dict:
                if str(variable) in self.dict[str(chatid)]:
                    return self.dict[str(chatid)][str(variable)]
            return None

    def sub_set(self, chatid, variable, value):
        with Redlock(key=self.key):
            if str(chatid) not in self.dict:
                self.dict[str(chatid)] = {}
            self.redisWR(str(chatid), str(variable), value)

    def sub_delete(self, chatid, variable):
        with Redlock(key=self.key):
            if str(chatid) not in self.dict:
                self.dict[str(chatid)] = {}
            self.redisWR(str(chatid), str(variable), None, True)

    # auxiliary func for set and delete
    def redisWR(self, keychild, key, value=None, delete=False):
        if not delete:
            tmpdic = self.dict[keychild]
            tmpdic[key] = value
            self.dict[keychild] = tmpdic
        else:
            tmpdic = self.dict[keychild]
            del tmpdic[key]
            self.dict[keychild] = tmpdic
