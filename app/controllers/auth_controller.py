from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():
    is_active = True
    if request.method == "POST":
        success = AuthService.signup(request.form)
        if not success:
            is_active = False
            return render_template('signup.html', is_active=is_active)
        return redirect(url_for('auth.login'))
    return render_template('signup.html', is_active=is_active)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    is_active = True
    if request.method == "POST":
        user = AuthService.login(request.form)
        if not user:
            is_active = False
            return render_template('login.html', is_active=is_active)
        session.permanent = True
        session["user"] = user.email
        return redirect(url_for('data.index'))
    return render_template('login.html', is_active=is_active)

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))