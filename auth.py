from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password or not confirm_password:
            flash("Todos os campos são obrigatórios.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("As passwords não coincidem.", "error")
            return render_template("register.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Já existe um utilizador com esse email.", "error")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registo realizado com sucesso! Já pode fazer login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Por favor, preencha email e password.", "error")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciais inválidas.", "error")
            return render_template("login.html")

        session["user_id"] = user.id
        session["user_name"] = user.name

        flash(f"Bem-vindo(a), {user.name}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada com sucesso.", "success")
    return redirect(url_for("index"))