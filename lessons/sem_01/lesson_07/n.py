import os
import argparse
import re

class InvalidTaskIDError(Exception):
    """Exception raised for invalid task IDs."""
    pass

def validate_task_id(task_id: str):
    # Check if the task_id already exists
    if os.path.exists(os.path.join("tasks", task_id)):
        raise InvalidTaskIDError(f"Task ID '{task_id}' already exists.")

    # Validate the task_id format
    if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', task_id):
        raise InvalidTaskIDError("Task ID must start with a letter, followed by letters, digits or underscores.")
    
    if task_id.startswith('_'):
        raise InvalidTaskIDError("Task ID cannot start with an underscore.")
    
    if task_id.endswith('_'):
        raise InvalidTaskIDError("Task ID cannot end with an underscore.")
    
    if len(task_id) < 2:
        raise InvalidTaskIDError("Task ID must be at least 2 characters long.")

def create_task_template(task_id: str):
    # Create directory for the task
    task_dir = os.path.join("tasks", task_id)
    os.makedirs(task_dir, exist_ok=True)

    # Create README.md
    readme_content = f"# {task_id}\n"
    with open(os.path.join(task_dir, "README.md"), 'w') as readme_file:
        readme_file.write(readme_content)

    # Create solution.py
    solution_content = """class Solution:
    # your code here
    pass


if __name__ == "__main__":
    solution = Solution()
    # testcases
"""
    with open(os.path.join(task_dir, "solution.py"), 'w') as solution_file:
        solution_file.write(solution_content)

def main():
    parser = argparse.ArgumentParser(description="Create a task template for interview preparation.")
    parser.add_argument("--task-id", required=True, help="The ID of the task to create.")
    args = parser.parse_args()

    task_id = args.task_id

    try:
        validate_task_id(task_id)
        create_task_template(task_id)
        print(f"Task template for '{task_id}' created successfully.")
    except InvalidTaskIDError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()