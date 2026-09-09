import json
import mimetypes
import uuid
import zipfile
from pathlib import Path

from app import db
from app.storage.manager import storage


def register(kind, path, prompt="", provider="", job_id=None, metadata=None):
    p = Path(path).resolve()
    aid = uuid.uuid4().hex
    db.asset_add(
        id=aid,
        kind=kind,
        name=p.name,
        path=str(p),
        prompt=prompt,
        provider=provider,
        job_id=job_id,
        metadata=metadata or {},
    )
    return aid


def _decode(d):
    if d and isinstance(d.get("metadata"), str):
        try:
            d = {**d, "metadata": json.loads(d["metadata"])}
        except Exception:
            d = {**d, "metadata": {}}
    return d


def stats():
    return {
        "images": len(storage.list("image")),
        "videos": len(storage.list("video")),
        "root": str(storage.root),
        "registered_assets": len(db.assets_list(limit=100000)),
    }


def list_assets(kind=None, limit=100, query=None):
    rows = [_decode(x) for x in db.assets_list(kind, limit)]
    if query:
        q = query.lower()
        rows = [
            x
            for x in rows
            if q
            in (
                x.get("name", "")
                + " "
                + x.get("prompt", "")
                + " "
                + x.get("provider", "")
            ).lower()
        ]
    return rows


def get_asset(asset_id):
    return _decode(db.asset_get(asset_id))


def asset_file(asset_id):
    d = get_asset(asset_id)
    if not d:
        return None, None
    p = Path(d["path"]).resolve()
    roots = (storage.images.resolve(), storage.videos.resolve(), storage.temp.resolve())
    if not any(r == p.parent or r in p.parents for r in roots) or not p.is_file():
        return d, None
    return d, p


def asset_manifest(asset_id):
    d, p = asset_file(asset_id)
    if not d:
        return None
    return {
        **d,
        "available": bool(p),
        "size": p.stat().st_size if p else None,
        "content_type": mimetypes.guess_type(d["name"])[0]
        or "application/octet-stream",
    }


def export_assets(asset_ids):
    out = storage.temp / f"bina-export-{uuid.uuid4().hex}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        manifest = []
        for aid in asset_ids:
            d, p = asset_file(aid)
            if d and p:
                z.write(p, p.name)
                manifest.append(asset_manifest(aid))
        z.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return out, manifest


def delete_asset(kind, asset):
    d, p = asset_file(asset)
    name = d["name"] if d else asset
    ok = storage.delete(kind, name)
    db.asset_delete(asset)
    return ok
