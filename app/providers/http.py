from __future__ import annotations

import json
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    pass


def request_json(url, payload, headers=None, timeout=120):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise ProviderError(
            f"provider_http_{e.code}: {e.read().decode(errors='ignore')[:500]}"
        )


def download(url, output):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=180) as r:
        output.write_bytes(r.read())
    return output
