from app import create_app
from models import db, Vehicle, PaymentMethod
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Métodos de pagamento
    pm1 = PaymentMethod(name="Cartão de Crédito")
    pm2 = PaymentMethod(name="MBWay")
    pm3 = PaymentMethod(name="PayPal")

    db.session.add_all([pm1, pm2, pm3])

    v1 = Vehicle(
        brand="BMW",
        model="X5",
        category="SUV",
        transmission="Automático",
        vehicle_type="Carro",
        seats=5,
        daily_rate=120.0,
        image_url="images/image_bmwx5.jpg",
        last_service_date=date(2024, 5, 10),
        next_service_date=date(2025, 5, 10),
        last_inspection_date=date(2024, 3, 1)
    )

    v2 = Vehicle(
        brand="Honda",
        model="CB500",
        category="Médio",
        transmission="Manual",
        vehicle_type="Moto",
        seats=2,
        daily_rate=45.0,
        image_url="images/image honda cb500.jpg",
        last_service_date=date(2025, 7, 20),
        next_service_date=date(2026, 7, 20),
        last_inspection_date=date(2025, 6, 15)
    )

    v3 = Vehicle(
        brand="Fiat",
        model="500",
        category="pequeno",
        transmission="Manual",
        vehicle_type="Carro",
        seats=4,
        daily_rate=45.0,
        image_url=None,
        last_service_date=date(2025, 11, 1),
        next_service_date=date(2026, 6, 1),
        last_inspection_date=date(2025, 12, 11)
    )

    db.session.add_all([v1, v2, v3])
    db.session.commit()

    print("Base de dados criada e populada com sucesso!")