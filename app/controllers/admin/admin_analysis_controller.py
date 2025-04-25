from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db

admin_analysis_controller = Blueprint('admin_analysis_controller', __name__, url_prefix='/analysis')

def is_logged_in():
    return "admin_id" in session

@admin_analysis_controller.route("/")
def show_analysis():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        results = list(db.analysis_results.find())
        return render_template("analysis.html", results=results)
    except Exception as e:
        print(f"Analysis error: {e}")
        return render_template("error.html", message="Failed to load analysis"), 500