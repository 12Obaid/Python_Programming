import requests
import datetime
import pytz
import h3
from timezonefinder import TimezoneFinder
from PIL import Image, ImageTk
import tkinter as tk

# Replace with your actual OpenWeatherMap API key
API_KEY = "7f03d1f665d67f83986495e91e2373d8"

def get_weather(city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Error: {data.get('message', 'Unknown error')}", None

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]
    h3_index = h3.geo_to_h3(lat, lon, 6)  # resolution 6 is reasonable for cities

    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)

    local_time = datetime.datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d %H:%M:%S")

    weather_info = (
        f"📍 City: {data['name']}, {data['sys']['country']}\n"
        f"🕒 Local Time: {local_time} ({timezone})\n"
        f"🌡️ Temp: {data['main']['temp']}°C\n"
        f"🌤️ Weather: {data['weather'][0]['description'].title()}\n"
        f"💧 Humidity: {data['main']['humidity']}%\n"
        f"🌬️ Wind: {data['wind']['speed']} m/s\n"
    )
    return weather_info, h3_index

# GUI Setup
def show_weather():
    city = city_entry.get()
    weather_text, _ = get_weather(city)
    result_label.config(text=weather_text)

app = tk.Tk()
app.title("🌤️ Weather App 🌤️ ")
app.geometry("500x600")

# Load background image
try:
    bg_image = Image.open("background.jpg").resize((500, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception:
    app.configure(bg="#DDEEFF")  # fallback

title_label = tk.Label(app, text="Weather App", font=("Times New Roman", 20), bg="#DDEEFF")
title_label.pack(pady=20)

city_entry = tk.Entry(app, font=("Times New Roman", 16), justify="center")
city_entry.pack(pady=10)

check_button = tk.Button(app, text="Check Weather", font=("Times New Roman", 14), command=show_weather)
check_button.pack(pady=10)

result_label = tk.Label(app, text="", font=("Times New Roman", 12), bg="#DDEEFF", justify="left")
result_label.pack(padx=20, pady=20)

app.mainloop()
