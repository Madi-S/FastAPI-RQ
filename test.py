import json
import redis

client = redis.Redis(host='127.0.0.1', port=6379)
client.delete('room1')
client.lpush('room1', json.dumps({'jack': 'hello alice'}))
client.lpush('room1', json.dumps({'jack': 'hello bob'}))
client.lpush('room1', json.dumps({'jack': 'hello jack'}))

msgs = client.lrange('room1', 0, -1)
for msg in msgs:
    print(json.loads(msg))
