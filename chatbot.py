from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os


# Load .env file
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

print("API KEY LOADED:", api_key is not None)


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json

        message = data["message"]

        print("User:", message)


        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=message
        )


        reply = response.text

        print("AI:", reply)


        return jsonify({
            "reply": reply
        })


    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "reply": str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True)