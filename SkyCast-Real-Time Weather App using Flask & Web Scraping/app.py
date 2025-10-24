from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            city_formatted = city.lower().replace(" ", "-")
            url = f"https://www.timeanddate.com/weather/{city_formatted}"
            
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")

                temperature = soup.find("div", class_="h2").get_text(strip=True)
                description = soup.find("div", class_="h2").find_next("p").get_text(strip=True)

                weather_data = {
                    "city": city.title(),
                    "temperature": temperature,
                    "description": description
                }
            except AttributeError:
                weather_data = {"error": "City not found. Please check the name and try again."}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
