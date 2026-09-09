import zipfile

from app.assets import asset_file, asset_manifest, export_assets, list_assets, register
from app.storage.manager import storage


def test_manifest_and_export():
    p = storage.path("image", ".txt")
    p.write_text("bina")
    aid = register("image", p, "phase e", "test")
    m = asset_manifest(aid)
    assert m["available"] and m["size"] == 4
    z, items = export_assets([aid])
    assert z.exists() and items and zipfile.is_zipfile(z)


def test_search_assets():
    p = storage.path("image", ".txt")
    p.write_text("x")
    register("image", p, "unique-phase-e-prompt", "test")
    assert any(
        "unique-phase-e" in x["prompt"] for x in list_assets(query="unique-phase-e")
    )


def test_missing_asset_file():
    assert asset_file("missing") == (None, None)
