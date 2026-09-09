from app.storage.manager import storage
def stats():
 return {"images":len(storage.list("image")),"videos":len(storage.list("video")),"root":str(storage.root)}
