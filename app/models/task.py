from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Dict, Any


class Task:
    """Task model for MongoDB document."""

    @staticmethod
    def create(title, description=None, status='pending', tags=None):
        """Create a new task document."""
        return {
            'title': title,
            'description': description or '',
            'status': status,
            'tags': tags or [],
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }

    @staticmethod
    def validate(data):
        """Validate task data."""
        errors = []

        if not data.get('title'):
            errors.append('Title is required')

        if data.get('status') and data['status'] not in ['pending', 'in_progress', 'completed']:
            errors.append('Status must be one of: pending, in_progress, completed')

        # Validate tags if present
        if 'tags' in data and data['tags'] is not None:
            try:
                from app.models.task_tags import TaskTags
                if isinstance(data['tags'], list):
                    for tag in data['tags']:
                        TaskTags.validate_tag(tag)
                else:
                    errors.append('Tags must be a list')
            except ValueError as e:
                errors.append(f'Invalid tag: {str(e)}')

        return errors

    @staticmethod
    def serialize(task):
        """Convert MongoDB document to JSON-serializable format."""
        if task:
            if '_id' in task and task['_id'] is not None:
                task['_id'] = str(task['_id'])
            if 'created_at' in task and task['created_at'] is not None:
                if hasattr(task['created_at'], 'isoformat'):
                    task['created_at'] = task['created_at'].isoformat()
                else:
                    task['created_at'] = str(task['created_at'])
            if 'updated_at' in task and task['updated_at'] is not None:
                if hasattr(task['updated_at'], 'isoformat'):
                    task['updated_at'] = task['updated_at'].isoformat()
                else:
                    task['updated_at'] = str(task['updated_at'])
        return task

    @staticmethod
    def update_fields(data):
        """Prepare fields for update operation."""
        allowed_fields = ['title', 'description', 'status', 'tags']
        update_data = {
            key: value for key, value in data.items()
            if key in allowed_fields and value is not None
        }
        update_data['updated_at'] = datetime.now(timezone.utc)
        return update_data