import functools
import pathlib
import shutil

import requests
from tqdm import tqdm


def download(url, filename):
    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed

    with tqdm.wrapattr(
            open(filename, "wb"),
            "write",
            miniters=1,
            desc=desc,
            total=int(file_size),
    ) as file:
        for chunk in r.iter_content(chunk_size=4096):
            file.write(chunk)
    # with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
    #     with path.open("wb") as f:
    #         shutil.copyfileobj(r_raw, f)

    return path


def upgrade():
    filename = 'stealth.min.js'
    file_url = 'https://raw.githubusercontent.com/requireCool/stealth.min.js/main/stealth.min.js'
    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        response.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {file_url} returned status code {response.status_code}")

    file_size = int(response.headers.get('content-length', 0))
    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    response.raw.read = functools.partial(response.raw.read, decode_content=True)  # Decompress if needed
    desc = "(Unknown total file size)" if file_size == 0 else ""
    with tqdm.wrapattr(response.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)


if __name__ == '__main__':
    upgrade()
    # download('https://raw.githubusercontent.com/requireCool/stealth.min.js/main/stealth.min.js', 'stealth.min.js')
