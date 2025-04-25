from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db

admin_dashboard_controller = Blueprint('dashboard_controller', __name__)

def is_logged_in():
    return "admin_id" in session

@admin_dashboard_controller.route("/")
def show_dashboard():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        counts = {
            "admins": db.admins.count_documents({}),
            "devices": db.devices.count_documents({}),
            "images": db.images.count_documents({}),
            "feedbacks": db.feedbacks.count_documents({})
        }

        analysis = list(db.analysis_results.find({}, {"quality_score": 1, "error_flag": 1}))
        scores = [res.get("quality_score", 0) for res in analysis if res.get("quality_score") is not None]
        avg_score = round(sum(scores)/len(scores), 2) if scores else 0

        quality_counts = {
            "excellent": sum(1 for res in analysis if res.get("quality_score", 0) > 0.5),
            "low": sum(1 for res in analysis if res.get("quality_score", 0) <= 0.5 and not res.get("error_flag", False)),
            "error": sum(1 for res in analysis if res.get("error_flag", False))
        }

        return render_template("dashboard.html",
            counts=counts,
            avg_quality_score=avg_score,
            quality_counts=quality_counts
        )
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template("error.html", message="Failed to load dashboard data"), 500