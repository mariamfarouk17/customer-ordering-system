from flask import Flask, jsonify, render_template, redirect, url_for

from models.database import init_db, seed_data
from services.menu_service import get_all_items

# Create the Flask application
app = Flask(__name__)


# --- Page Routes ---

@app.route("/")
def index():
    # Redirect visitors from the root URL to the menu page
    return redirect(url_for("menu"))


@app.route("/menu")
def menu():
    # Render the menu page template (templates/menu.html)
    return render_template("menu.html")


# --- API Routes ---

@app.route("/api/menu")
def api_menu():
    # Return all menu items grouped by category as JSON
    data = get_all_items()
    return jsonify(data)


@app.route("/health")
def health():
    # Simple health check so you can confirm the server is running
    return jsonify({"status": "ok"})


# --- Entry Point ---

if __name__ == "__main__":
    # Set up the database tables and insert sample data on first run
    init_db()
    seed_data()
    print("Starting Customer Ordering System...")
    app.run(debug=True)