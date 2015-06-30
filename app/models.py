from app import db

class devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    ip = db.Column(db.String(128), index=True)
    timers = db.relationship('timer', backref='device_name',
                                lazy='dynamic')

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

class timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    start_time = db.Column(db.String(64), index=True)
    end_time = db.Column(db.String(64), index=True)
    timer_type = db.Column(db.Integer, index=True)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3