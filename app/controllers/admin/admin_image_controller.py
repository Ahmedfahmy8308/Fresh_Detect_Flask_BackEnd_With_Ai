from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db

admin_image_controller = Blueprint('admin_image_controller', __name__, url_prefix='/images')

def is_logged_in():
    return "admin_id" in session

@admin_image_controller.route("/")
def list_images():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        images = list(db.images.find())
        return render_template("images.html", images=images)
    except Exception as e:
        print(f"Images error: {e}")
        return render_template("error.html", message="Failed to load images"), 500