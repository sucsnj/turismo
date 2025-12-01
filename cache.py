import redis
import json

# Conexão com Redis (nome do serviço no docker-compose)
r = redis.Redis(host="redis", port=6379, db=0)

def get_cache(key: str):
    """Retorna valor do cache se existir"""
    if r.exists(key):
        return json.loads(r.get(key))
    return None

def set_cache(key: str, value, ttl: int = 3600):
    """Salva valor no cache com TTL (default 1h)"""
    r.setex(key, ttl, json.dumps(value))
