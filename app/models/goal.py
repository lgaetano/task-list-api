from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def tasks_to_dict(self):
        tasks = [task.goals_to_dict() for task in self.tasks]
        return {
            "id": self.id,
            "title": self.title,
            "tasks": tasks
        }
    
    def update_from_dict(self, data):
        # Loops through attributes provided by users
        for key, value in data.items():
            # Restricts to attributes that are columns
            if key in Goal.__table__.columns.keys():
                setattr(self, key, value)