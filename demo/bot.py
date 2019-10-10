import asyncio
import itertools
import random
import string
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Callable

import aiohttp


def random_string() -> Callable[[int], str]:
    seen = set()

    def generate(length: int = 16):
        template = list(string.ascii_letters + string.digits)

        while True:
            random.shuffle(template)
            generated = ''.join(template)[:length]

            if generated not in seen:
                seen.add(generated)

                return generated

    return generate


get_random_string = random_string()


# very simplified version of activity bot, doesn't handle pagination and auth-refresh
# by conditions defined in the test task, this bot performs bulk post & like operations

class User:
    def __init__(self, posts_count: int, likes_count: int, base_url: str):
        self.posts_count = posts_count
        self.likes_count = likes_count
        self.credentials = {}
        self.base_url = base_url

    def url(self, rel: str) -> str:
        return f'{self.base_url}/{rel}'

    async def signup(self):
        # we could create and use here a bot-signup endpoint for internal services authentication
        while True:
            try:
                async with self.session(auth=False) as session:
                    credentials = {
                        'username': get_random_string(15),
                        'email': f'{get_random_string(15)}@test.com',
                        'password': get_random_string(15),
                    }
                    response = await session.post(self.url('accounts/signup/'), data=credentials)
                    response.raise_for_status()

                    credentials.pop('email')
                    self.credentials = credentials

                    break
            except aiohttp.ClientResponseError as e:
                if e.status != 401:
                    raise e

    @asynccontextmanager
    async def session(self, auth: bool = True) -> aiohttp.ClientSession:
        headers = {}

        if auth:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url('accounts/login/'), data=self.credentials) as response:
                    token_resp = await response.json()
                    headers['Authorization'] = f'JWT {token_resp["token"]}'

        async with aiohttp.ClientSession(headers=headers) as session:
            yield session

    async def post(self) -> List[int]:
        async def perform_post():
            async with self.session() as session:
                data = {'content': get_random_string(100)}

                async with session.post(self.url('posts/'), data=data) as resp:
                    post_resp = await resp.json()

                    return post_resp['id']

        return await asyncio.gather(*[perform_post() for _ in range(self.posts_count)])

    async def like(self, posts_ids: List[int]):
        async def perform_like(post_id: int):
            async with self.session() as session:
                await session.post(self.url(f'posts/{post_id}/like/'))

        await asyncio.gather(*[perform_like(random.choice(posts_ids)) for _ in range(self.likes_count)])


class Bot:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

        self.users = [
            User(self.config['max_posts_per_user'], self.config['max_likes_per_user'], config['base_url'])
            for _ in range(self.config['number_of_users'])
        ]
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(5)

    async def post_activity(self) -> List[int]:
        async def signup_and_post(user: User) -> List[int]:
            await user.signup()
            return await user.post()

        posts_by_users = await asyncio.gather(*list(map(signup_and_post, self.users)))

        return list(itertools.chain.from_iterable(posts_by_users))

    async def like_activity(self, posts_ids: List[int]):
        await asyncio.gather(*[user.like(posts_ids) for user in self.users])

    async def run(self):
        posts_ids = await self.post_activity()
        await self.like_activity(posts_ids)


if __name__ == '__main__':
    bot = Bot({
        'number_of_users': 2,
        'max_posts_per_user': 3,
        'max_likes_per_user': 3,
        'base_url': 'http://127.0.0.1:8000',
    })

    asyncio.run(bot.run())
