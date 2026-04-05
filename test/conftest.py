import pytest
from sequana_pipetools.snaketools.sequana_config import _Namespace


@pytest.fixture(autouse=True)
def patch_namespace_setitem(monkeypatch):
    """Add dict-style item assignment support to _Namespace so that
    cfg["section"]["key"] = value works the same as cfg.section.key = value."""
    monkeypatch.setattr(_Namespace, "__setitem__", lambda self, key, value: setattr(self, key, value), raising=False)
