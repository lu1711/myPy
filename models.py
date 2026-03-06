from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship("Reservation", backref="user", lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

    @property
    def image(self):
        return self.image_url or "images/padrao.jpg"

    last_service_date = db.Column(db.Date)
    next_service_date = db.Column(db.Date)
    last_inspection_date = db.Column(db.Date)

    reservations = db.relationship("Reservation", backref="vehicle", lazy=True)

    def is_available(self, start_date, end_date):
        # 1. Verificar inspeção
        if self.last_inspection_date:
            delta = datetime.utcnow().date() - self.last_inspection_date
            if delta.days > 365:
                return False

        # 2. Verificar revisão
        if self.next_service_date and self.next_service_date <= datetime.utcnow().date():
            return False

        # 3. Verificar reservas existentes
        for r in self.reservations:
            if r.status == "active":
                if not (end_date <= r.start_date or start_date >= r.end_date):
                    return False
        return True

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    payment_method_id = db.Column(db.Integer, db.ForeignKey("payment_method.id"))
    status = db.Column(db.String(20), default="active")