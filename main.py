import asyncio
import sqlite3
from pathlib import Path
from typing import Any, AsyncIterator, Awaitable, Callable, Dict
from tortoise.contrib.aiohttp import register_tortoise

from models import ActiveUserCount
import aiosqlite
from aiohttp import web

router = web.RouteTableDef()

def handle_json_error(
        func: Callable[[web.Request], Awaitable[web.Response]]
) -> Callable[[web.Request], Awaitable[web.Response]]:
    async def handler(request: web.Request) -> web.Response:
        try:
            return await func(request)
        except asyncio.CancelledError:
            raise
        except Exception as ex:
            return web.json_response(
                {"status": "failed", "reason": str(ex)}, status=400
            )

    return handler


@router.get("/")
async def root(request: web.Request) -> web.Response:
    actuser = ActiveUserCount()
    await actuser.save()
    return web.Response(text=f"Placeholder")


@router.get("/getActiveUsers")
@handle_json_error
async def get_activeUsers_count(request: web.Request) -> web.Response:
    ret = {}
    count = await ActiveUserCount.all()
    return web.json_response({"status": "ok", "data": count[0].count})


@router.post("/incActiveUsers")
@handle_json_error
async def inc_user_count(request: web.Request) -> web.Response:
    delta_json = await request.json()
    delta = delta_json["delta"]
    actuser = await ActiveUserCount.get(id=1)
    actuser.count += int(delta)
    await actuser.save()
    return web.json_response(
        {
            "status": "ok",
            "data": {"success": "true"}
        }
    )


@router.post("/decActiveUsers")
@handle_json_error
async def dec_user_count(request: web.Request) -> web.Response:
    delta_json = await request.json()
    delta = delta_json["delta"]
    actuser = await ActiveUserCount.get(id=1)
    actuser.count -= int(delta)
    await actuser.save()
    return web.json_response(
        {
            "status": "ok",
            "data": {"success": "true"}
        }
    )


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    # app.cleanup_ctx.append(init_db)
    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={"models": ["models"]},
        generate_schemas=True,
    )
    return app


web.run_app(init_app())
