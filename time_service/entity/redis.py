import redis
import os
import datetime


class Redis:

    @staticmethod
    def getClientInstance():
        return redis.Redis(
            host=os.getenv("redis_host", "localhost"),
            port=os.getenv("redis_port", "6379"),
        )
