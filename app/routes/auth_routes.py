from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
import asyncio
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity

from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_service import create_user, authenticate_user, get_all_users, delete_user
from app.routes.student_routes import admin_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = UserRegister(
                username=request.form.get("username"),
                email=request.form.get("email"),
                password=request.form.get("password")
            )
            asyncio.run(create_user(data))
            flash("Account created! You can now login.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Registration Error: {str(e)}", "danger")
            
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = asyncio.run(authenticate_user(username, password))
        
        if user:
            token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            
            response = make_response(redirect(url_for("students.index")))
            set_access_cookies(response, token)
            flash(f"Welcome back, {user.username}!", "success")
            return response
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(response)
    flash("Successfully logged out.", "success")
    return response

@auth_bp.route("/users")
@admin_required
def list_users():
    users = asyncio.run(get_all_users())
    return render_template("users.html", users=users)

@auth_bp.route("/users/delete/<int:id>", methods=["POST"])
@admin_required
def delete_user_route(id):
    current_user_id = int(get_jwt_identity())
    if id == current_user_id:
        flash("Error: You cannot delete your own account while logged in!", "danger")
        return redirect(url_for("auth.list_users"))

    user = asyncio.run(delete_user(id))
    if user:
        flash(f"User {user.username} has been removed.", "success")
    else:
        flash("Error: User not found.", "danger")
        
    return redirect(url_for("auth.list_users"))
