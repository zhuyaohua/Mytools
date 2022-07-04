"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     python_websocket.py
@Author:   shenfan
@Time:     2022/4/6 11:35
"""
import asyncio
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator
        message = '{"action":"subscribe","args":["QuoteBin5m:14"]}'
        await converse.send(message)

        while True:
            receive = await converse.receive()

            print(receive.decode())


if __name__ == '__main__':
    remote = 'wss://api.bbxapp.vip/v1/ifcontract/realTime'
    asyncio.get_event_loop().run_until_complete(startup(remote))




