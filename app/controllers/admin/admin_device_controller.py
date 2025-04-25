from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db import db

admin_device_controller = Blueprint('admin_device_controller', __name__, url_prefix='/devices')

def is_logged_in():
    return "admin_id" in session

@admin_device_controller.route("/")
def list_devices():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        devices = list(db.devices.find().skip((page-1)*per_page).limit(per_page))
        return render_template("devices.html", devices=devices, page=page)
    except Exception as e:
        print(f"Devices list error: {e}")
        return render_template("error.html", message="Failed to load devices"), 500