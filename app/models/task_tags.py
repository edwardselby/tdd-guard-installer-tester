"""
Task Tags Model - TDD Implementation.

This module implements task tagging functionality following TDD principles.
Implementation progresses through RED (failing tests) -> GREEN (minimal code) -> REFACTOR.

FEATURE: Task Tags
- Tasks can have multiple tags (labels/categories)
- Tags are simple strings (e.g., "urgent", "backend", "bug")
- Tags can be added, removed, and filtered
- Tags are stored as a list in the task document
"""

import re
from typing import List, Dict, Any, Optional
from collections import Counter


class TaskTags:
    """Utility class for managing task tags."""

    # Tag validation constants
    MAX_TAG_LENGTH = 50
    TAG_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')

    @classmethod
    def add_tag(cls, task_data: Dict[str, Any], tag: str) -> Dict[str, Any]:
        """
        Add a tag to a task.

        :param task_data: Task dictionary
        :param tag: Tag string to add
        :return: Updated task dictionary
        :raises ValueError: If tag is invalid
        """
        if not tag:
            raise ValueError("Tag cannot be empty")

        # Validate and normalize tag
        cls.validate_tag(tag)
        normalized_tag = cls.normalize_tag(tag)

        # Create a copy to avoid modifying original
        result = task_data.copy()

        # Initialize tags field if it doesn't exist
        if 'tags' not in result:
            result['tags'] = []

        # Make a copy of tags list to avoid modifying original
        tags = result['tags'].copy()

        # Add tag if it doesn't already exist
        if normalized_tag not in tags:
            tags.append(normalized_tag)

        result['tags'] = tags
        return result

    @classmethod
    def remove_tag(cls, task_data: Dict[str, Any], tag: str) -> Dict[str, Any]:
        """
        Remove a tag from a task.

        :param task_data: Task dictionary
        :param tag: Tag string to remove
        :return: Updated task dictionary
        :raises ValueError: If tag is invalid
        """
        if not tag:
            raise ValueError("Tag cannot be empty")

        normalized_tag = cls.normalize_tag(tag)

        # Create a copy to avoid modifying original
        result = task_data.copy()

        # If no tags field, return as-is
        if 'tags' not in result:
            result['tags'] = []
            return result

        # Make a copy of tags list and remove the tag
        tags = result['tags'].copy()
        if normalized_tag in tags:
            tags.remove(normalized_tag)

        result['tags'] = tags
        return result

    @classmethod
    def get_tags(cls, task_data: Dict[str, Any]) -> List[str]:
        """
        Get all tags from a task.

        :param task_data: Task dictionary
        :return: List of tags
        """
        return task_data.get('tags', [])

    @classmethod
    def has_tag(cls, task_data: Dict[str, Any], tag: str) -> bool:
        """
        Check if a task has a specific tag.

        :param task_data: Task dictionary
        :param tag: Tag string to check
        :return: True if task has the tag, False otherwise
        :raises ValueError: If tag is invalid
        """
        if not tag:
            raise ValueError("Tag cannot be empty")

        normalized_tag = cls.normalize_tag(tag)
        tags = cls.get_tags(task_data)
        return normalized_tag in tags

    @classmethod
    def validate_tag(cls, tag: str) -> None:
        """
        Validate a tag format.

        :param tag: Tag string to validate
        :raises ValueError: If tag is invalid
        """
        if not tag:
            raise ValueError("Tag cannot be empty")

        if tag is None:
            raise ValueError("Tag cannot be empty")

        # Check length
        if len(tag) > cls.MAX_TAG_LENGTH:
            raise ValueError(f"Tag is too long (max {cls.MAX_TAG_LENGTH} characters)")

        # Check for invalid characters (spaces, tabs, newlines, special symbols)
        if ' ' in tag or '\t' in tag or '\n' in tag:
            raise ValueError("Tag contains invalid characters")

        # Check against allowed pattern
        if not cls.TAG_PATTERN.match(tag):
            raise ValueError("Tag contains invalid characters")

    @classmethod
    def normalize_tag(cls, tag: str) -> str:
        """
        Normalize a tag (lowercase and trim whitespace).

        :param tag: Tag string to normalize
        :return: Normalized tag string
        """
        if not tag:
            return tag

        return tag.strip().lower()

    @classmethod
    def filter_tasks_by_tag(cls, tasks: List[Dict[str, Any]], tag: str) -> List[Dict[str, Any]]:
        """
        Filter tasks that have a specific tag.

        :param tasks: List of task dictionaries
        :param tag: Tag to filter by
        :return: List of tasks that have the tag
        """
        normalized_tag = cls.normalize_tag(tag)
        filtered_tasks = []

        for task in tasks:
            task_tags = task.get('tags', [])
            if normalized_tag in task_tags:
                filtered_tasks.append(task)

        return filtered_tasks

    @classmethod
    def get_all_unique_tags(cls, tasks: List[Dict[str, Any]]) -> List[str]:
        """
        Get all unique tags from a list of tasks.

        :param tasks: List of task dictionaries
        :return: List of unique tags
        """
        all_tags = set()

        for task in tasks:
            task_tags = task.get('tags', [])
            all_tags.update(task_tags)

        return sorted(list(all_tags))

    @classmethod
    def get_tag_counts(cls, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get usage counts for all tags from a list of tasks.

        :param tasks: List of task dictionaries
        :return: Dictionary mapping tag names to usage counts
        """
        all_tags = []

        for task in tasks:
            task_tags = task.get('tags', [])
            all_tags.extend(task_tags)

        return dict(Counter(all_tags))