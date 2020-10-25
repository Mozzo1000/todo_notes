from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(240), index=True, unique=True)
    name = db.Column(db.String(240), index=True)
    password = db.Column(db.String(512))
    notes = db.relationship('Notes', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120))
    content = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime, index=True)
    due_date = db.Column(db.DateTime, index=True)
    tags = db.Column(db.String)
