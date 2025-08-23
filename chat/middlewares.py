from .utils import generate_username
from .constants import USERNAME


class RandomUsernameMiddleware:
    def __init__(self,inner):
        self.inner = inner

    async def __call__(self,scope,receive,send):
        scope[USERNAME] = generate_username()

        return await self.inner(scope,receive,send)