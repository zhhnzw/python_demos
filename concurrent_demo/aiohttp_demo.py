import asyncio
import aiohttp
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

plan_time = 2
begin_time = time.time()
coroutine_num = 1000


async def start_task():
    async with aiohttp.ClientSession() as session:
        response_bytes = 0
        request_num = 0
        while True:
            if time.time() - begin_time < plan_time:
                content = await request(session)
                response_bytes += len(content)
                request_num += 1
            else:
                return response_bytes, request_num


async def request(session):
    url = 'https://www.baidu.com/'
    async with session.get(url, headers=headers) as response:
        content = await response.read()
        print('c')
        return content


def run():
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(start_task()) for i in range(coroutine_num)]
    tasks_return_list = loop.run_until_complete(asyncio.gather(*tasks))
    end_time = time.time()
    pass_time = end_time-begin_time
    msg = '执行时长:%f s, 并行任务量:%d, 请求数:%d, 吞吐量约:%f MB(只计response), QPS:%f' % \
          (
              pass_time,
              coroutine_num,
              sum([i[1] for i in tasks_return_list]),
              sum([i[0] for i in tasks_return_list])/(1024*1024),
              sum([i[1] for i in tasks_return_list])/pass_time
          )
    print(msg)


if __name__ == '__main__':
    run()