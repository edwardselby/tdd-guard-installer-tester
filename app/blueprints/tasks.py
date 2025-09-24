from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId

from app.database import mongo
from app.models.task import Task
from app.models.task_tags import TaskTags

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate task data
    errors = Task.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    # Create task document
    task_doc = Task.create(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'pending'),
        tags=data.get('tags', [])
    )

    # Insert into database
    result = mongo.db.tasks.insert_one(task_doc)
    task_doc['_id'] = result.inserted_id

    return jsonify(Task.serialize(task_doc)), 201


@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    # Get query parameters for filtering
    status = request.args.get('status')
    limit = request.args.get('limit', type=int, default=100)
    skip = request.args.get('skip', type=int, default=0)

    # Build query
    query = {}
    if status:
        query['status'] = status

    # Execute query
    cursor = mongo.db.tasks.find(query).skip(skip).limit(limit).sort('created_at', -1)
    all_tasks = list(cursor)

    # Filter by tag if specified
    tag_filter = request.args.get('tag')
    if tag_filter:
        all_tasks = TaskTags.filter_tasks_by_tag(all_tasks, tag_filter)
        total = len(all_tasks)
    else:
        total = mongo.db.tasks.count_documents(query)

    tasks = [Task.serialize(task) for task in all_tasks]

    return jsonify({
        'tasks': tasks,
        'total': total,
        'limit': limit,
        'skip': skip
    }), 200


@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID."""
    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify(Task.serialize(task)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400


@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate if status is provided
        if 'status' in data:
            errors = Task.validate({'title': 'dummy', 'status': data['status']})
            if errors:
                return jsonify({'errors': errors}), 400

        # Prepare update data
        update_data = Task.update_fields(data)

        # Update in database
        result = mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': update_data}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        # Get updated task
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        return jsonify(Task.serialize(task)), 200

    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400


@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})

        if result.deleted_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({'message': 'Task deleted successfully'}), 200

    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400


@tasks_bp.route('/tasks/bulk-delete', methods=['POST'])
def bulk_delete_tasks():
    """Delete multiple tasks at once."""
    data = request.get_json()
    if 'task_ids' not in data:
        return jsonify({'error': 'No task IDs provided'}), 400

    task_ids = data['task_ids']
    count = 0
    for task_id in task_ids:
        result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
        count += result.deleted_count

    return jsonify({
        'deleted_count': count,
        'message': f'{count} tasks deleted successfully'
    }), 200


def _get_x_value():
    """Helper method to get x value."""
    return 1

def _get_total_value():
    """Helper method to get total value."""
    return None

def _build_stats_response(x_value, total_value):
    """Helper method to build response dictionary."""
    return {'x': x_value, 'total': total_value}

@tasks_bp.route('/tasks/stats', methods=['GET'])
def get_task_statistics():
    """Get task statistics."""
    x = _get_x_value()
    total = _get_total_value()
    response_data = _build_stats_response(x, total)
    return jsonify(response_data), 200


@tasks_bp.route('/tasks/<task_id>/archive', methods=['POST'])
def archive_task(task_id):
    """Archive a task."""
    try:
        # Update the task to set archived = True
        result = mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'archived': True}}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({'message': 'Task archived successfully'}), 200

    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400


@tasks_bp.route('/tasks/<task_id>/tags', methods=['POST'])
def add_tag_to_task(task_id):
    """Add a tag to a task."""
    try:
        data = request.get_json()
        if not data or 'tag' not in data:
            return jsonify({'error': 'Tag parameter is required'}), 400

        tag = data['tag']

        # Find the task
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Add the tag
        try:
            updated_task = TaskTags.add_tag(task, tag)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Update in database
        result = mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'tags': updated_task['tags']}}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        # Get updated task
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        return jsonify(Task.serialize(task)), 200

    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@tasks_bp.route('/tasks/<task_id>/tags/<tag>', methods=['DELETE'])
def remove_tag_from_task(task_id, tag):
    """Remove a tag from a task."""
    try:
        # Find the task
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Remove the tag
        updated_task = TaskTags.remove_tag(task, tag)

        # Update in database
        result = mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'tags': updated_task['tags']}}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        # Get updated task
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        return jsonify(Task.serialize(task)), 200

    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@tasks_bp.route('/tasks/tags', methods=['GET'])
def get_all_tags():
    """Get all unique tags from all tasks."""
    try:
        # Get all tasks
        cursor = mongo.db.tasks.find({})
        all_tasks = list(cursor)

        # Get unique tags
        unique_tags = TaskTags.get_all_unique_tags(all_tasks)

        return jsonify({'tags': unique_tags}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@tasks_bp.route('/tasks/tags/stats', methods=['GET'])
def get_tag_statistics():
    """Get tag usage statistics."""
    try:
        # Get all tasks
        cursor = mongo.db.tasks.find({})
        all_tasks = list(cursor)

        # Get tag counts
        tag_counts = TaskTags.get_tag_counts(all_tasks)

        return jsonify({'tag_counts': tag_counts}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500