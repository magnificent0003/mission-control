import tracker


def test_add_task_creates_task(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "DB_PATH", tmp_path / "tasks.json")
    t = tracker.add_task("Test task")
    assert t["id"] == 1
    assert t["done"] is False


def test_add_task_rejects_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "DB_PATH", tmp_path / "tasks.json")
    try:
        tracker.add_task("   ")
        assert False
    except ValueError:
        assert True


def test_list_tasks_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "DB_PATH", tmp_path / "tasks.json")
    assert tracker.list_tasks() == []


def test_mark_done_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "DB_PATH", tmp_path / "tasks.json")
    tracker.add_task("A")
    updated = tracker.mark_done(1)
    assert updated["done"] is True


def test_mark_done_missing_id(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "DB_PATH", tmp_path / "tasks.json")
    try:
        tracker.mark_done(999)
        assert False
    except KeyError:
        assert True
