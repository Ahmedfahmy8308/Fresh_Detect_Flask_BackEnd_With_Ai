from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db

admin_feedback_controller = Blueprint('admin_feedback_controller', __name__, url_prefix='/feedbacks')

def is_logged_in():
    return "admin_id" in session

@admin_feedback_controller.route("/")
def list_feedbacks():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        feedbacks = list(db.feedbacks.find())
        return render_template("feedbacks.html", feedbacks=feedbacks)
    except Exception as e:
        print(f"Feedbacks error: {e}")
        return render_template("error.html", message="Failed to load feedbacks"), 500