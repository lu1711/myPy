from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from models import db, Vehicle, Reservation, PaymentMethod

reservations_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

def require_login():
    user_id = session.get("user_id")
    if not user_id:
        flash("Tem de fazer login para efectuar uma reserva.", "error")
        return None
    return user_id

@reservations_bp.route("/create/<int:vehicle_id>", methods=["GET", "POST"])
def create_reservation(vehicle_id):
    user_id = require_login()
    if user_id is None:
        return redirect(url_for("auth.login"))

    vehicle = Vehicle.query.get_or_404(vehicle_id)
    payment_methods = PaymentMethod.query.filter_by(is_active=True).all()

    if request.method == "POST":
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        payment_method_id = request.form.get("payment_method_id")

        if not start_date_str or not end_date_str or not payment_method_id:
            flash("Por favor, preencha todas as informações.", "error")
            return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Datas inválidas.", "error")
            return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

        if start_date >= end_date:
            flash("A data de início deve ser anterior à data de fim.", "error")
            return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

        if start_date < datetime.utcnow().date():
            flash("A data de início não pode ser no passado.", "error")
            return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

        if not vehicle.is_available(start_date, end_date):
            flash("O veículo não está disponível para as datas selecionadas.", "error")
            return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

        num_days = (end_date - start_date).days
        total_price = num_days * vehicle.daily_rate

        reservation = Reservation(
            user_id=user_id,
            vehicle_id=vehicle.id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            payment_method_id=int(payment_method_id),
            status="active"
        )

        db.session.add(reservation)
        db.session.commit()

        flash(f"Reserva concluída com sucesso! Valor total: {total_price:.2f}€", "success")
        return redirect(url_for("reservations.my_reservations"))

    return render_template("reservation.html", vehicle=vehicle, payment_methods=payment_methods)

@reservations_bp.route("/my")
def my_reservations():
    user_id = require_login()
    if user_id is None:
        return redirect(url_for("auth.login"))

    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.start_date.desc()).all()
    return render_template("my_reservations.html", reservations=reservations)

@reservations_bp.route("/edit/<int:reservation_id>", methods=["GET", "POST"])
def edit_reservation(reservation_id):
    user_id = require_login()
    if user_id is None:
        return redirect(url_for("auth.login"))

    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != user_id:
        flash("Não tem permissão para alterar esta reserva.", "error")
        return redirect(url_for("reservations.my_reservations"))

    vehicle = reservation.vehicle

    if request.method == "POST":
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")

        if not start_date_str or not end_date_str:
            flash("Por favor, preencha ambas as datas.", "error")
            return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

        try:
            new_start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            new_end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Datas inválidas.", "error")
            return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

        if new_start_date >= new_end_date:
            flash("A data de início deve ser anterior à data de fim.", "error")
            return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

        if new_start_date < datetime.utcnow().date():
            flash("A data de início não pode ser no passado.", "error")
            return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

        # Temporariamente remover esta reserva da lista do veículo
        original_status = reservation.status
        reservation.status = "temp_ignore"

        if not vehicle.is_available(new_start_date, new_end_date):
            reservation.status = original_status
            flash("O veículo não está disponível para as novas datas.", "error")
            return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

        reservation.status = original_status
        reservation.start_date = new_start_date
        reservation.end_date = new_end_date

        num_days = (new_end_date - new_start_date).days
        reservation.total_price = num_days * vehicle.daily_rate

        db.session.commit()

        flash("Reserva atualizada com sucesso.", "success")
        return redirect(url_for("reservations.my_reservations"))

    return render_template("reservation.html", vehicle=vehicle, reservation=reservation, edit_mode=True)

@reservations_bp.route("/cancel/<int:reservation_id>", methods=["POST"])
def cancel_reservation(reservation_id):
    user_id = require_login()
    if user_id is None:
        return redirect(url_for("auth.login"))

    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != user_id:
        flash("Não tem permissão para cancelar esta reserva.", "error")
        return redirect(url_for("reservations.my_reservations"))

    reservation.status = "cancelled"
    db.session.commit()

    flash("Reserva cancelada com sucesso.", "success")
    return redirect(url_for("reservations.my_reservations"))