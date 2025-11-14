import tkinter as tk 
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

def update_clock():
    global result

    try:
        home = pytz.timezone(result)
        now = datetime.now(home)
        clock.config(text=now.strftime("%I:%M:%S %p"))
        clock.after(1000, update_clock)
    except:
        pass

def get_weather ():
    try:
        city = textfield.get()
        geolocator = Nominatim (user_agent="geopiExercises")
        location = geolocator.geocode(city)
        lat = location.latitude
        lng = location.longitude
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lng, lat=lat)
        city_label.config(text=location.address.split(",")[0])
        print(result)
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        time_label.config(text="Local Time")

        update_clock()
        api_key ="aac0f03bb464b5bc85468c1873cce7bc"
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"

        json_data = requests.get(api).json()
        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = int(json_data["main"]["temp"]-273.15)# celvin to cantigrad
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]


        temp_label.config(text=f"{temp} °")
        condition_label.config(text=f"{condition} | Feels like {temp} °")
        wind_label.config(text=wind)
        humidity_label.config(text=humidity)
        description_label.config(text=description)
        pressure_label.config(text=pressure)

        sunrise = json_data["sys"]["sunrise"]
        sunset = json_data["sys"]["sunset"]

        sunrise_time = datetime.fromtimestamp(sunrise, home).strftime("%I:%M %p")
        sunset_time = datetime.fromtimestamp(sunset, home).strftime("%I:%M %p")

        sunrise_label.config(text=f"Sunrise: {sunrise_time}")
        sunset_label.config(text=f"Sunset: {sunset_time}")



        forecast_api = (
            f"https://api.openweathermap.org/data/2.5/onecall?"
            f"lat={lat}&lon={lng}&exclude=minutely,hourly&appid={api_key}&units=metric"
    )


        forecast_json = requests.get(forecast_api).json()

        # پاک کردن فریم قبلی
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        # رسم پیش‌بینی 7 روز
        for i in range(7):
            day = forecast_json["daily"][i]
            dt = datetime.fromtimestamp(day["dt"]).strftime("%a")
            temp_day = int(day["temp"]["day"])
            cond = day["weather"][0]["main"]

            frame = tk.Frame(forecast_frame, bg="#1ab5ef", bd=2)
            frame.grid(row=0, column=i, padx=5)

            tk.Label(frame, text=dt, bg="#1ab5ef",
                     font=("arial", 12, "bold")).pack(padx=5)
            tk.Label(frame, text=f"{temp_day}°C", bg="#1ab5ef",
                     font=("arial", 12, "bold")).pack()
            tk.Label(frame, text=cond, bg="#1ab5ef",
                     font=("arial", 10, "bold")).pack()
            

            alerts = forecast_json.get("alerts", [])
        if alerts:
            alert = alerts[0]
            event = alert["event"]
            desc = alert["description"]

            messagebox.showwarning("Weather Alert", f"{event}\n\n{desc}")


    except Exception as error:
        print(error)
        # messagebox.showerror("weather App" , "Invalid Entry")



root = tk.Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False,True)

search_image = tk.PhotoImage(file="search.png")
search_image_label = tk.Label(root , image=search_image)
search_image_label.pack(pady=20 , side=tk.TOP)

textfield = tk.Entry(root , justify="center", width=17,
                    font=("poppins",20,"bold"),
                    bg="#404040" , fg="white" , border=0)
textfield.place(x=280 , y=40)

search_icon = tk.PhotoImage(file="search_icon.png")
search_icon_button = tk.Button(root , image=search_icon , border=0,
                               cursor="hand2",bg="#404040",command=get_weather)
search_icon_button.place(x=590,y=34)

logo_image = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(side=tk.TOP)


frame_image = tk.PhotoImage(file="box.png")
frame_label = tk.Label(root, image=frame_image)
frame_label.pack(pady=10,side=tk.BOTTOM)


city_label = tk.Label(root,font=("arial",30,"bold"), fg= "#e355cd")
city_label.place(x=120 , y=160)

time_label = tk.Label(root,font=("arial",20,"bold"), fg= "#e3455c")
time_label.place(x=120 , y=230)

clock = tk.Label(root,font=("Helvetica",20), fg= "#b445cc")
clock.place(x=120 , y=270)

sunrise_label = tk.Label(root, font=("arial", 14, "bold"), fg="#e3455c")
sunrise_label.place(x=120, y=310)

sunset_label = tk.Label(root, font=("arial", 14, "bold"), fg="#e3455c")
sunset_label.place(x=120, y=340)


#سرعت باد
label1 = tk.Label(root,text="WIND",font=("Helvetica" , 15,"bold"),
                  fg="White" , bg="#1ab5ef")
label1.place(x=120,y=400)
# میزان رطوبت
label2 = tk.Label(root,text="HUMIDITY",font=("Helvetica" , 15,"bold"),
                  fg="White" , bg="#1ab5ef")
label2.place(x=280,y=400)
# وضعیت آب و هوا 
label3 = tk.Label(root,text="DESCRIPTION",font=("Helvetica" , 15,"bold"),
                  fg="White" , bg="#1ab5ef")
label3.place(x=450,y=400)
# میزان فشار هوا
label4 = tk.Label(root,text="PRESSURE",font=("Helvetica" , 15,"bold"),
                  fg="White" , bg="#1ab5ef")
label4.place(x=670,y=400)

temp_label = tk.Label(root, font=("arial",70,"bold"), fg= "#e355cd")
temp_label.place(x=590 , y=170)

condition_label = tk.Label(root, font=("arial",15,"bold"), fg= "#4b4bcc")
condition_label.place(x=590 , y=270)


wind_label = tk.Label(root, text="..." , font=("arial" ,20 , "bold" ),
                      bg="#1ab5ef" , fg="#404040")
wind_label.place(x=120, y=430)

humidity_label = tk.Label(root, text="..." , font=("arial" ,20 , "bold" ),
                           bg="#1ab5ef" , fg="#404040")
humidity_label.place(x=280 , y=430)

description_label = tk.Label(root, text="..." , font=("arial" ,20 , "bold"),
                           bg="#1ab5ef" , fg="#404040")
description_label.place(x=430 , y=430)

pressure_label = tk.Label(root, text="..." , font=("arial" ,20 , "bold" ),
                           bg="#1ab5ef" , fg="#404040")
pressure_label.place(x=670 , y=430)

forecast_frame = tk.Frame(root, bg="#2c2c2c")
forecast_frame.place(x=50, y=500)

root.mainloop()