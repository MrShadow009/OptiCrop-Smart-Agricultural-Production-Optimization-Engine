from flask import Flask, request, render_template
import json
import os
import random



def load_random_outputs(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("outputs", [])


# Load static/random recommendation pool once at startup
JSON_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "random_output.json")
_random_outputs = load_random_outputs(JSON_OUTPUT_PATH)
if not _random_outputs:
    # Safe fallback if json is missing/empty
    _random_outputs = ["Random recommendation unavailable. Please try again."]

# Note: plant_api_key.txt remains in the repo from the previous version, but
# this app no longer reads it or makes any external API calls.



# creating flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    # Random-output mode (API key removed). Inputs are read only to mirror the form contract.
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    # Choose a deterministic-ish random recommendation based on inputs.
    seed_str = f"{N}|{P}|{K}|{temp}|{humidity}|{ph}|{rainfall}"
    seed = abs(hash(seed_str))
    rng = random.Random(seed)
    result = rng.choice(_random_outputs) if _random_outputs else "Random recommendation unavailable."

    return render_template('index.html', result=result)






# python main
if __name__ == "__main__":
    app.run(debug=True)