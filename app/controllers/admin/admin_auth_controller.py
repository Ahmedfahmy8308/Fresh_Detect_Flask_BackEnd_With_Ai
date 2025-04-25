from flask import Blueprint, render_template, request, redirect, session, url_for
from app.db import db

admin_auth_controller = Blueprint('auth_controller', __name__)
admins_collection = db["admins"]

@admin_auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        admin = admins_collection.find_one({"email": email})
        if admin and admin["password"] == password:  
            session.clear()
            session["admin_id"] = str(admin["admin_ID"])
            session.permanent = True
            return redirect(url_for("dashboard_controller.show_dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@admin_auth_controller.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_controller.login"))