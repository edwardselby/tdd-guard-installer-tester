import pytest

def test_task_creation_success():
    task_data = {"title": "Complete project", "description": "Finish the TDD implementation"}
    task = Task(task_data)

    assert task.title == "Complete project"
    assert task.description == "Finish the TDD implementation"
    assert task.created_at is not None