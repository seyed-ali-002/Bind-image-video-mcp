from app.core.runtime import free_port
from app.core.doctor import doctor
from app.db import record,history
def test_free_port():assert isinstance(free_port(19000),int)
def test_doctor():assert "platform" in doctor()
def test_history():record("test","hello","mock");assert history(1)
