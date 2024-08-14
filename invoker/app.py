from flask import Flask, request, jsonify
import requests
import redis
import config
from concurrent.futures import ThreadPoolExecutor
from cache import Cache

app = Flask(__name__)

# Initialize Redis connection
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
# Initialize Local Cache with TTL of 10 seconds and 3 keys max
local_cache = Cache(ttl=10, max_size=3)


def call_generator(modelname, viewerid):
    response = requests.post(f'{config.GENERATOR_URL}/generate', json={
        'modelname': modelname,
        'viewerid': viewerid
    })

    return response.json()


@app.route('/recommend', methods=['GET'])
def recommend():
    viewerid = request.args.get('viewerid')

    # Check local cache
    if viewerid in local_cache:
        return jsonify(local_cache.get(viewerid))

    # Check Redis cache
    cached_data = redis_client.get(viewerid)
    if cached_data:
        return jsonify(eval(cached_data))

    # Run the cascade and cache the result
    result = runcascade(viewerid)
    local_cache.set(viewerid, result)
    redis_client.set(viewerid, str(result))

    return jsonify(result)


def runcascade(viewerid):
    modelnames = [f"model{i}" for i in range(1, 6)]
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda modelname: call_generator(modelname, viewerid), modelnames))

    # Merge results into a single response
    merged_result = {"viewerid": viewerid, "recommendations": results}
    return merged_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
