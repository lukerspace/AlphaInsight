import os
# fake redis
USE_FAKE_REDIS = os.getenv("USE_FAKE_REDIS", "1") == "1"

_client = None  

def get_redis_client():
    global _client
    if _client is not None:
        return _client

    if USE_FAKE_REDIS:
        import fakeredis
        _client = fakeredis.FakeStrictRedis(decode_responses=True)
        print("[INFO] Using fakeredis (in-memory)")
        try:
            _client.ping()
            print("[INFO] Connected to Redis")
        except Exception as e:
            print("[WARN] Redis not available:", e)
            _client = None
    return _client
