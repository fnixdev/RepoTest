

import time
import aiohttp

from urllib.parse import unquote


async def fast_download(download_url, filename=None, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                filename = unquote(download_url.rpartition("/")[-1])
            downloaded_size = 0
            start_time = time.time()
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
            return filename, time.time() - start_time