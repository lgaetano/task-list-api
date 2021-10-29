from app import db
from flask import Blueprint, request, abort, jsonify
from datetime import datetime
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    """Retrieve all stored tasks."""
    query = request.args.get("sort")
    if query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    print(tasks_response)

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    """Retrieve one stored task by id."""
    task = Task.query.get_or_404(task_id)

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("", methods=["POST"])
def post_task():
    """Create a new task from JSON data."""
    form_data = request.get_json()

    #TODO: Refactor to validation decorator helper method
    mandatory_fields = ["title", "description", "completed_at"]
    for field in mandatory_fields:
        if field not in form_data:
            return jsonify({"details": "Invalid data"}), 400 

    new_task = Task(
        title=form_data["title"],
        description=form_data["description"],
        completed_at=form_data["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    print(new_task.to_dict())
    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    """Updates task by id."""
    # Search database for task by id
    task = Task.query.get_or_404(task_id)
    # Retrieve form data
    form_data = request.get_json()

    # Loops through attributes provided by user
    for key, value in form_data.items():
        # Restricts to attributes that are table columns
        if key in Task.__table__.columns.keys():
            setattr(task, key, value)

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_to_complete(task_id):
    """Updates task at particular id to completed."""
    task = Task.query.get_or_404(task_id)

    task.completed_at = datetime.now()

    db.session.commit()
    return {"task": task.to_dict()}, 200

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_to_incomplete(task_id):
    """ """
    task = Task.query.get_or_404(task_id)

    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes task by id."""
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }, 200