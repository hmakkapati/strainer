
class MemcacheException(Exception):
    pass


class Memcache(object):

    _cache = dict()

    @classmethod
    def set_to_cache(cls, key, value, override=True):
        if key in cls._cache.has_key and not override:
                raise MemcacheException()
        cls._cache[key] = value

    @classmethod
    def get_from_cache(cls, key):
        return cls._cache.get(key)

    @classmethod
    def has_key(cls, key):
        return key in cls._cache
