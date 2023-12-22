import aioredis
import redis
import json
redis_url = 'redis://localhost:6379'
async def save_dict_to_redis(redis_url, key, dictionary):
    async with aioredis.create_redis_pool(redis_url) as redis:
        # Преобразование словаря в JSON и сохранение в Redis
        json_dict = json.dumps(dictionary)
        await redis.set(key, json_dict)

async def load_dict_from_redis(redis_url, key):
    async with aioredis.create_redis_pool(redis_url) as redis:
        # Загрузка JSON из Redis и преобразование в словарь
        json_dict = await redis.get(key, encoding='utf-8')
        if json_dict:
            return json.loads(json_dict)
        else:
            return None
async def save_list_to_redis(redis_url, key, my_list):
    async with aioredis.create_redis_pool(redis_url) as redis:
        # Преобразование списка в JSON и сохранение в Redis
        json_list = json.dumps(my_list)
        await redis.set(key, json_list)

async def load_list_from_redis(redis_url, key):
    async with aioredis.create_redis_pool(redis_url) as redis:
        # Загрузка JSON из Redis и преобразование в список
        json_list = await redis.get(key, encoding='utf-8')
        if json_list:
            return json.loads(json_list)
        else:
            return None

