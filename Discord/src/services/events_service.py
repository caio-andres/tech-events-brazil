import aiohttp
from typing import List, Dict, Any


async def fetch_events(url: str) -> List[Dict[str, Any]]:
    """Retorna a lista completa de eventos do JSON."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("tba", [])


async def get_last_events(url: str, count: int = 3) -> List[Dict[str, Any]]:
    """Retorna apenas os últimos `count` eventos."""
    events = await fetch_events(url)
    return events[-count:] if events else []
