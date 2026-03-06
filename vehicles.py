from flask import Blueprint, render_template, request
from models import db, Vehicle

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")

@vehicles_bp.route("/search", methods=["GET", "POST"])
def search():
    #filtros formulário
    brand = request.form.get("brand")
    model = request.form.get("model")
    category = request.form.get("category")
    transmission = request.form.get("transmission")
    vehicle_type = request.form.get("vehicle_type")
    seats = request.form.get("seats")
    max_price = request.form.get("max_price")

    # Começar query base
    query = Vehicle.query

    # Aplicar filtros se existirem
    if brand:
        query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if category:
        query = query.filter_by(category=category)
    if transmission:
        query = query.filter_by(transmission=transmission)
    if vehicle_type:
        query = query.filter_by(vehicle_type=vehicle_type)
    if seats:
        query = query.filter(Vehicle.seats >= int(seats))
    if max_price:
        query = query.filter(Vehicle.daily_rate <= float(max_price))

    # Obter resultados da BD
    vehicles = query.all()

    return render_template("search.html", vehicles=vehicles)

@vehicles_bp.route("/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template("vehicle_detail.html", vehicle=vehicle)