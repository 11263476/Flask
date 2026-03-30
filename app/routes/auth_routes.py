from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response  # Flask utilities
import asyncio  # Asynchronous support
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity # JWT support

from app.schemas.user_schema import UserRegister, UserLogin  # Import data schemas
from app.services.auth_service import create_user, authenticate_user, get_all_users, delete_user # Import logic functions
from app.routes.student_routes import admin_required # Import admin security

auth_bp = Blueprint("auth", __name__) # Create blueprint for Auth routes

# --- UI Routes (For Browser) ---

@auth_bp.route("/register", methods=["GET", "POST"]) # Page for user registration
def register():
    if request.method == "POST":
        try:
            # 1. Validate the form data
            data = UserRegister(
                username=request.form.get("username"),
                email=request.form.get("email"),
                password=request.form.get("password")
            )
            # 2. Save user to database
            asyncio.run(create_user(data))
            flash("Account created! You can now login.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Registration Error: {str(e)}", "danger")
            
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"]) # Page for user login
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 1. Check credentials
        user = asyncio.run(authenticate_user(username, password))
        
        if user:
            # 2. Create a JWT token containing the user's ID and role
            token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            
            # 3. Store the token in a secure cookie
            response = make_response(redirect(url_for("students.index")))
            set_access_cookies(response, token)
            flash(f"Welcome back, {user.username}!", "success")
            return response
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template("login.html")

@auth_bp.route("/logout") # Clears the session and token
def logout():
    response = make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(response) # Remove the JWT cookie
    flash("Successfully logged out.", "success")
    return response

@auth_bp.route("/users") # Admin-only page to see all registered users
@admin_required
def list_users():
    users = asyncio.run(get_all_users())
    return render_template("users.html", users=users)

@auth_bp.route("/users/delete/<int:id>", methods=["POST"]) # Admin-only delete action
@admin_required
def delete_user_route(id):
    # --- Safety Check: Prevent deleting yourself! ---
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
