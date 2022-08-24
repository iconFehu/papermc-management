from tqdm import tqdm


async def aiohttp_progress(fn):
    response = await fn
    content = bytes()
    progress_bar = tqdm(total=response.content_length, unit='iB', unit_scale=True)
    async with response as r:
        async for data in r.content:
            progress_bar.update(len(data))
            content += data
    progress_bar.close()
    return response, content
