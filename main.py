from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from timezonefinder import TimezoneFinder

root = Tk()
root.title("Weather App")
root.geometry("950x580+250+100")
root.resizable(False, False)
root.config(bg="#00bfff")  # Sky Blue Background

def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)

    long_lat.config(text=f"{round(location.latitude, 4)}°N {round(location.longitude, 4)}°E")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    api_key = "161eba479c7f2cf65427be9ed8d9cf32"
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    json_data = requests.get(api).json()

    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed = current['wind']['speed']
    description = current['weather'][0]['description']
    weather_icon_code = current['weather'][0]['icon']

    # Update main weather values
    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description}")

    # Load and display weather icon
    icon_img = Image.open(f"icon/{weather_icon_code}@2x.png").resize((50, 50))
    current_weather_icon = ImageTk.PhotoImage(icon_img)
    weather_icon_label.config(image=current_weather_icon)
    weather_icon_label.image = current_weather_icon

    # Forecast data
    forecast_list = json_data['list']
    icons.clear()
    temps.clear()

    today = datetime.now(home).date()

    for i in range(5):
        date = today + timedelta(days=i)

        day_temp = None
        night_temp = None
        icon_code = None

        for entry in forecast_list:
            entry_time = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
            if entry_time.date() == date:
                if entry_time.hour == 12:
                    day_temp = entry['main']['temp']
                    if not icon_code:
                        icon_code = entry['weather'][0]['icon']
                if entry_time.hour == 21:
                    night_temp = entry['main']['temp']

        if icon_code:
            img = Image.open(f"icon/{icon_code}@2x.png").resize((40, 40))
            icons.append(ImageTk.PhotoImage(img))
        else:
            icons.append(None)

        temps.append((day_temp, night_temp))

    day_widget = [
        (firstimage, day1, day1temp),
        (secondimage, day2, day2temp),
        (thirdimage, day3, day3temp),
        (fourthimage, day4, day4temp),
        (fifthimage, day5, day5temp)
    ]

    for i, (img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(temps): break
        if icons[i]:
            img_label.config(image=icons[i])
            img_label.image = icons[i]
        else:
            img_label.config(image='')

        day, night = temps[i]
        text = f"Day: {'-' if day is None else str(round(day, 2)) + '°C'}\nNight: {'-' if night is None else str(round(night, 2)) + '°C'}"
        temp_label.config(text=text)

        future_date = today + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))

image_icon = PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

cloud_img = PhotoImage(file="Images/Layer 7.png")
search_icon_img = PhotoImage(file="Images/Layer 6.png")

clock = Label(root, font=("Helvetica", 20), bg="#00bfff", fg="#081c24")
clock.place(x=20, y=20)

timezone = Label(root, font=("Helvetica", 20), bg="#00bfff", fg="#081c24")
timezone.place(x=750, y=20)

long_lat = Label(root, font=("Helvetica", 10), bg="#00bfff", fg="#081c24")
long_lat.place(x=750, y=55)

search_label = Label(root, text="Enter city name", font=("Helvetica", 15, "bold"), bg="#00bfff", fg="#081c24")
search_label.place(x=380, y=70)

search_frame = Frame(root, bg="#e0f7fa", bd=2, relief="groove")
search_frame.place(x=270, y=105)

Label(search_frame, image=cloud_img, bg="#e0f7fa").pack(side=LEFT, padx=(5, 10))
textfield = Entry(search_frame, justify="center", width=15, font=("poppins", 22), bg="#ffffff", border=0, fg="#081c24")
textfield.pack(side=LEFT, ipady=5)
search_icon = Button(search_frame, image=search_icon_img, borderwidth=0, cursor="hand2", bg="#0c1c4d", command=getWeather)
search_icon.pack(side=LEFT, padx=(10, 5))

info_box = Frame(root, width=900, height=140, bg="#e0f7fa")
info_box.place(x=25, y=170)

Label(info_box, text="Temperature", font=("Helvetica", 12 , "bold"), bg="#e0f7fa", fg="#3d3d3d").place(x=30, y=20)
t = Label(info_box, font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#081c24")
t.place(x=150, y=20)

Label(info_box, text="Humidity", font=("Helvetica", 12 , "bold"), bg="#e0f7fa", fg="#3d3d3d").place(x=30, y=50)
h = Label(info_box, font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#081c24")
h.place(x=150, y=50)

Label(info_box, text="Pressure", font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#3d3d3d").place(x=30, y=80)
p = Label(info_box, font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#081c24")
p.place(x=150, y=80)

Label(info_box, text="Wind Speed", font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#3d3d3d").place(x=400, y=20)
w = Label(info_box, font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#081c24")
w.place(x=530, y=20)

Label(info_box, text="Description", font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#3d3d3d").place(x=400, y=50)
d = Label(info_box, font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#081c24")
d.place(x=530, y=50)

weather_icon_label = Label(info_box, bg="#e0f7fa")
weather_icon_label.place(x=650, y=40)

frame = Frame(root, width=900, height=180, bg="#00bfff")
frame.place(x=25, y=330)

card_width = 150
card_gap = 30
start_x = 10

def create_day_box(parent, x):
    f = Frame(parent, width=card_width, height=160, bg="#ffffff")
    f.place(x=x, y=10)
    return f

firstframe = Frame(frame, width=card_width, height=160, bg="#0c1c4d")
firstframe.place(x=start_x, y=10)
firstimage = Label(firstframe, bg="#0c1c4d")
firstimage.place(x=10, y=40)
day1 = Label(firstframe, font=("arial", 14, "bold"), bg="#0c1c4d", fg="white")
day1.place(x=10, y=5)
day1temp = Label(firstframe, font=("arial", 12), bg="#0c1c4d", fg="white")
day1temp.place(x=10, y=110)

icons = []
temps = []

secondframe = create_day_box(frame, start_x + (card_width + card_gap) * 1)
secondimage = Label(secondframe, bg="white")
secondimage.place(x=35, y=40)
day2 = Label(secondframe, font=("Helvetica", 10, "bold"), bg="white")
day2.place(x=25, y=10)
day2temp = Label(secondframe, bg="white", font=("Helvetica", 10))
day2temp.place(x=10, y=100)

thirdframe = create_day_box(frame, start_x + (card_width + card_gap) * 2)
thirdimage = Label(thirdframe, bg="white")
thirdimage.place(x=35, y=40)
day3 = Label(thirdframe, font=("Helvetica", 10, "bold"), bg="white")
day3.place(x=25, y=10)
day3temp = Label(thirdframe, bg="white", font=("Helvetica", 10))
day3temp.place(x=10, y=100)

fourthframe = create_day_box(frame, start_x + (card_width + card_gap) * 3)
fourthimage = Label(fourthframe, bg="white")
fourthimage.place(x=35, y=40)
day4 = Label(fourthframe, font=("Helvetica", 10, "bold"), bg="white")
day4.place(x=25, y=10)
day4temp = Label(fourthframe, bg="white", font=("Helvetica", 10))
day4temp.place(x=10, y=100)

fifthframe = create_day_box(frame, start_x + (card_width + card_gap) * 4)
fifthimage = Label(fifthframe, bg="white")
fifthimage.place(x=35, y=40)
day5 = Label(fifthframe, font=("Helvetica", 10, "bold"), bg="white")
day5.place(x=25, y=10)
day5temp = Label(fifthframe, bg="white", font=("Helvetica", 10))
day5temp.place(x=10, y=100)

root.mainloop()
