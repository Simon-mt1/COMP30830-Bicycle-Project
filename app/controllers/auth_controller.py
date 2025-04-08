"""
auth_controller.py

Handles authentication-related routes including signup, login, and logout.

**Routes:**\n
- /signup: Handles user registration.\n
- /login: Handles user login.\n
- /logout: Logs the user out of the session.\n
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():
    """
    Route to handle user signup.

    GET: Renders the signup page.
    POST: Processes signup form data using AuthService. If registration is
    successful, redirects to the login page; otherwise, reloads signup page with error state.

    Returns:
        Response: Rendered HTML template or redirect to login route.
    """
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
    """
    Route to handle user login.

    GET: Renders the login page.
    POST: Authenticates user credentials using AuthService. If valid, stores user
    in session and redirects to data dashboard; otherwise, reloads login page with error state.

    Returns:
        Response: Rendered HTML template or redirect to data dashboard.
    """
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
    """
    Route to log out the current user.

    Pops the user from the session and redirects to the login page.

    Returns:
        Response: Redirect to login route.
    """
    session.pop("user", None)
    return redirect(url_for('auth.login'))