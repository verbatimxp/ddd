import asyncio
import datetime
import logging
from threading import Thread, enumerate
from uuid import uuid4

import aiohttp
import aiohttp_cors
from aiohttp import web

from database.init_connection import Database

TIMER_THREAD_NAME = 'timer_thread'
WS = []
HEADERS_CORS = {
    "http://localhost:3000": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers=("X-Custom-Server-Header",),
        allow_headers=("X-Requested-With", "Content-Type"),
        max_age=3600,
    )
}


def get_timer_thread(list_threads):
    for thread in list_threads:
        if thread.name == TIMER_THREAD_NAME:
            return thread
    return None


class AsyncTimer:

    def __init__(self, callback, loop):
        self._callback = callback
        self._task = asyncio.ensure_future(self._run(), loop=loop)
        self.timer = 0

    async def _run(self):
        while True:
            await asyncio.sleep(1)
            self.timer += 1
            await self._callback(self)


async def get_timer_value(async_timer):
    return async_timer.timer


class AsyncThreadTimer(Thread):

    def __init__(self, *args, **kwargs):
        super(AsyncThreadTimer, self).__init__(*args, **kwargs)
        self._loop = asyncio.new_event_loop()
        self.timer = AsyncTimer(callback=get_timer_value, loop=self._loop)
        self.daemon = True
        self.name = TIMER_THREAD_NAME

    def stop(self):
        self._loop.stop()

    def run(self):
        start_loop(self._loop)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def start(request):
    if len(enumerate()) > 1:
        timer_thread = get_timer_thread(enumerate())
        count = await get_timer_value(timer_thread.timer)
        text = f'Timer has already started, current value {count} sec.'
        return web.Response(text=text)
    else:
        Database.save_data_timer_start(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        timer_async = AsyncThreadTimer()
        timer_async.start()
        for ws in WS:
            await ws.send_str('Start time')
        return web.Response(text='Start timer')


async def stop(request):
    if len(enumerate()) > 1:
        Database.save_data_timer_end(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        timer_thread = get_timer_thread(enumerate())
        timer_thread.stop()
        for ws in WS:
            await ws.send_str('Timer has been stopped')
        return web.Response(text='Timer has been stopped')

    return web.Response(text='Timer has not been already started')


async def get(request):
    if len(enumerate()) > 1:
        timer_thread = get_timer_thread(enumerate())
        count = await get_timer_value(timer_thread.timer)
        text = f'value: {count} sec'
        return web.Response(text=text)

    return web.Response(text='The timer has not been started. Please click on the button Start timer')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws.id = uuid4()
    WS.append(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = msg.data.strip('\n')
            if data == 'close':
                await ws.close()
                WS.remove(ws)
            else:
                await ws.send_str(data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logging.info('ws connection closed with exception %s' %
                  ws.exception())

    logging.info('websocket connection closed')

    return ws


app = web.Application()

cors = aiohttp_cors.setup(app)


def resource(url_name=''):
    return cors.add(app.router.add_resource(f'{url_name}'))


urlpatterns = [
    cors.add(resource('/start').add_route("GET", start), HEADERS_CORS),
    cors.add(resource('/stop').add_route("GET", stop), HEADERS_CORS),
    cors.add(resource('/get').add_route("GET", get), HEADERS_CORS),
    cors.add(resource('/ws').add_route("GET", websocket_handler), HEADERS_CORS),
]

logging.basicConfig(level=logging.DEBUG, filename='./logs.log', filemode='a')

if __name__ == '__main__':
    web.run_app(app)
