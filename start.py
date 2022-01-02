import asyncio
from spride.spride import Spride
from checker.check import Checker


async def main():
    checker = Checker()
    spride = Spride()
    # 并发
    # await asyncio.gather(checker.main(), spride.main())
    await spride.main()
    await checker.main()


if __name__ == '__main__':
    asyncio.run(main())
