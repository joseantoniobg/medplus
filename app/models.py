from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class Secretary(UserMixin, db.Model):

	__tablename__ = 'secretaries'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	last_name = db.Column(db.String(60), index=True)
	email = db.Column(db.String(60), index=True, unique=True)
	password = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=False)
	records = db.relationship("Record", backref="secretary", lazy="dynamic")

	def set_password(self, p):
		self.password = generate_password_hash(p)

	def verify_password(self, p):
		return check_password_hash(self.password, p)

	def __repr__(self):
		return "<Secretary id: {}, name: {} email: {} >".format(self.id, self.name, self.email)

@login.user_loader
def load_user(user_id):
	return Secretary.query.get(int(user_id))

class Record (db.Model):

	__tablename__="records"

	id = db.Column(db.Integer, primary_key=True)
	id_secretary = db.Column(db.Integer, db.ForeignKey('secretaries.id'))
	id_patient = db.Column(db.Integer, db.ForeignKey('patients.id'))
	appointments = db.relationship("Appointment", backref="appointment", lazy="dynamic")

	def __repr__(self):
		return "<Record: {}>".format(self.id)

class Patient(db.Model):

	__tablename__="patients"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	lastname = db.Column(db.String(60), index=True)
	age = db.Column(db.Integer)
	cadsus = db.Column(db.String, index=True)
	record = db.relationship("Record", backref="patient", lazy="dynamic")

	def __repr__(self):
                return "<Patient: id: {} name: {}>".format(self.id, self.name)

class Appointment(db.Model):

	__tablename__ = "appointments"

	id = db.Column(db.Integer, primary_key=True)
	datetimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	place = db.Column(db.String(60), index=True)
	id_record = db.Column(db.Integer, db.ForeignKey('records.id'))

	def __repr__(self):
                return "<Appointment: id: {}>".format(self.id)

class Medic(db.Model):

	__tablename__ = "medics"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	lastname = db.Column(db.String(60), index=True)
	coren = db.Column(db.String(30), index=True)

	def __repr__(self):
                return "<Medic: id: {} name: {}>".format(self.id, self.name)

