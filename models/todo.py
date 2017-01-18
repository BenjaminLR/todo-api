from db import db


class TodoModel(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140))
    completed = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, task, completed, user_id):
        self.task = task
        self.completed = completed
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "task": self.task, "completed": self.completed}

    @classmethod
    def find_by_id(cls, t_id):
        return cls.query.filter_by(id=t_id).first()

    @classmethod
    def find_by_user_and_id(cls, t_id, u_id):
        return cls.query.filter_by(id=t_id, user_id=u_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
