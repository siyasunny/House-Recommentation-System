from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# --------------------------
# Load Models (Joblib format)
# --------------------------
design_model = joblib.load("design_model.joblib")
cement_model = joblib.load("cement_model.joblib")
steel_model = joblib.load("steel_model.joblib")
bricks_model = joblib.load("bricks_model.joblib")

# --------------------------
# Static Data / Maps
# --------------------------
design_names = ["Simple 2BHK", "Standard Duplex", "Modern Villa", "Luxury Villa"]

cement_map = {
    0: "200–250 bags",
    1: "300–350 bags",
    2: "400–450 bags"
}

steel_map = {
    0: "800–1000 kg",
    1: "1200–1500 kg",
    2: "1800–2200 kg"
}

bricks_map = {
    0: "10000–14000 units",
    1: "15000–18000 units",
    2: "20000–26000 units"
}

# --------------------------
# Routes
# --------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict_design", methods=["POST"])
def predict_design():
    try:
        sq = float(request.form["square_feet"])
        pc = float(request.form["plot_cents"])
    except ValueError:
        return "Invalid input! Please enter numeric values for square feet and plot size."

    # Predict design
    pred_index = design_model.predict([[sq, pc]])[0]
    if 0 <= pred_index < len(design_names):
        design_name = design_names[pred_index]
    else:
        design_name = "Unknown Design"

    return render_template(
        "materials_input.html",
        square_feet=sq,
        plot_cents=pc,
        design_name=design_name
    )


@app.route("/predict_materials", methods=["POST"])
def predict_materials():
    try:
        sq = float(request.form["square_feet"])
        pc = float(request.form["plot_cents"])
        design_name = request.form["design_name"]
        budget = float(request.form["budget"])
    except ValueError:
        return "Invalid input! Please enter numeric values for budget."

    # Predict materials
    cement_pred = cement_model.predict([[budget]])[0]
    steel_pred = steel_model.predict([[budget]])[0]
    bricks_pred = bricks_model.predict([[budget]])[0]

    cement = cement_map.get(cement_pred, "Unknown")
    steel = steel_map.get(steel_pred, "Unknown")
    bricks = bricks_map.get(bricks_pred, "Unknown")

    return render_template(
        "result.html",
        design_name=design_name,
        square_feet=sq,
        plot_cents=pc,
        budget=budget,
        cement=cement,
        steel=steel,
        bricks=bricks
    )


# --------------------------
# Run App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
