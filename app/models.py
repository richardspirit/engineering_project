from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repre__(self):
	return '<User %r>' % (self.login)

class Request(db.Model):
    reqid = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(20))
    desc = db.Column(db.String(160))
    client = db.Column(db.String(20))
    priorty = db.Column(db.Integer)
    target_date = db.Column(db.DateTime)
    ticket_url = db.Column(db.String(120))
    product_area = db.Column(db.String(10))

    def __repr__(self):
	return '<Request %r>' % (self.desc)
