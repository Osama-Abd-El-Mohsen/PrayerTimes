import requests
import customtkinter as ctk
from customtkinter import CTkToplevel
import os
import sys
import json
from PIL import Image, ImageTk
import datetime
import winreg as reg
import win11toast
import datetime

now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
times = []
salat = []
arabic_salat=["الفجْر","الشروق","الظُّهْر","العَصر","المَغرب","العِشاء"]

my_font = ctk.FontManager.load_font('assets/cairo.ttf')


sec_back_col="#DBE2E8"
main_back_col="#F3F5F4"
dark_color="#3d454f"
green_1 = "#90d0b5"
green_2 = "#3b9b6e"
green_3 = "#006b25"

def read_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data


def update_config(updated_data, config_file='config.json'):
    with open(config_file, 'w') as f:
        json.dump(updated_data, f, indent=4)
    # print("Config file updated successfully.")


def fetch_prayer_times(city, country):
    url = f'http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=5'
    response = requests.get(url)
    info = response.json()

    if 'data' in info:
        timings = info['data']['timings']
        return timings


def AddToRegistry():

    # in python __file__ is the instant of
    # file path where it was executed
    # so if it was executed from desktop,
    # then __file__ will be
    # c:\users\current_user\desktop
    pth = os.path.dirname(os.path.realpath(__file__))

    # name of the python file with extension
    s_name = "Prayer_Times_Script.py"

    # joins the file name to end of path address
    address = os.path.join(pth, s_name)

    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"

    # open the key to make changes to
    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

    # modify the opened key
    reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address)

    # now close the opened key
    reg.CloseKey(open)
remanning_time=0

def notification():
    global remanning_time,now,now_hour,now_min,next_hours,next_min
    if json_not_state == True:
        now = datetime.datetime.now()
        now_hour = int(now.strftime("%H"))
        now_min = int(now.strftime("%M"))
        current_time = now.strftime("%H:%M")

        next_hours, next_min = remanning_time.split(':')

        remanning_time = (datetime.timedelta(
            hours=int(next_hours), minutes=int(30)) - datetime.timedelta(hours=now_hour, minutes=now_min))

        rem_hour, rem_min, rem_sec = str(remanning_time).split(':')

        if next_hours == now_hour and next_min == now_min:

            win11toast.toast('حان الأن موعد أذان', f'{salat[index]}')


        elif rem_min == '05' :
            win11toast.toast(' متبقى 5 دقائق على اذان', f'{salat[index]}')

if __name__ == '__main__':
    AddToRegistry()
    app = ctk.CTk(fg_color=main_back_col)
    ctk.ThemeManager.load_theme('green')
    ctk.AppearanceModeTracker.set_appearance_mode('light')
    ctk.deactivate_automatic_dpi_awareness()
    app.title("Prayer Times App")
    icon_path = "\icon.ico"
    app.iconbitmap(os.getcwd()+icon_path)
    app.geometry('800x480')
    app.resizable(False, False)

    config_data = read_config()

    if config_data:
        state = config_data.get("First_Time")
        json_Country = config_data.get("Country")
        json_City = config_data.get("City")
        json_not_state = config_data.get("not_state")
        if state == True and json_Country == "None" and json_City == "None":
            main_state = 'First Time'
        else:
            main_state = 'Not First Time'

    if main_state == 'First Time':
        user_country = ctk.CTkInputDialog(text="country", title="test2")
        country = user_country.get_input()
        user_city = ctk.CTkInputDialog(text="city", title="test2")
        city = user_city.get_input()

        if country and city:
            config_data["Country"] = country
            config_data["City"] = city
            config_data["First_Time"] = False
            update_config(config_data)
            os.execv(sys.executable, ['python'] + sys.argv)
    elif main_state == 'Not First Time':
        try:
            values = fetch_prayer_times(json_City, json_Country)
            for x, y in values.items():
                if x in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
                    salat.append(x)
                    times.append(y)

        except Exception as E:
            print(E)

    fram0 = ctk.CTkFrame(app, fg_color=sec_back_col,corner_radius=20)
    fram1 = ctk.CTkFrame(fram0, fg_color=green_1)

    asr_img = ctk.CTkImage(Image.open("assets/asr.png"), size=(25, 25))
    dhuhr_img = ctk.CTkImage(Image.open("assets/dhuhr.png"), size=(25, 25))
    fajr_img = ctk.CTkImage(Image.open("assets/fajr.png"), size=(25, 20))
    isha_img = ctk.CTkImage(Image.open("assets/isha.png"), size=(25, 25))
    maghrib_img = ctk.CTkImage(Image.open(
        "assets/maghrib.png"), size=(25*1.46, 25))
    sunrise_img = ctk.CTkImage(Image.open(
        "assets/sunrise.png"), size=(25*1.46, 25))
    country_img = ctk.CTkImage(Image.open("assets/country.png"), size=(25, 25))
    city_img = ctk.CTkImage(Image.open("assets/city.png"), size=(25, 25))
    setting_img = ctk.CTkImage(Image.open(
        "assets/settings2.png"), size=(25, 25))
    logo_img = ctk.CTkImage(Image.open(
        "assets/logo.png"), size=(40, 40))


    
    city_label = ctk.CTkLabel(
        fram1,
        text=f"City : {json_City}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color

    )
    img_city = ctk.CTkLabel(
        fram1,
        text=' ',
        image=city_img
    )
    country_label = ctk.CTkLabel(
        fram1,
        text=f"Country : {json_Country}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color

    )
    img_country = ctk.CTkLabel(
        fram1,
        text=' ',
        image=country_img
    )

    fram2 = ctk.CTkFrame(fram1, fg_color=main_back_col)
    Salat_Fajr = ctk.CTkLabel(
        fram2,
        text=f"الفجْر",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Salat_Sunrise = ctk.CTkLabel(
        fram2,
        text=f"الشروق",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Salat_Dhuhr = ctk.CTkLabel(
        fram2,
        text=f"الظُّهْر",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Salat_Asr = ctk.CTkLabel(
        fram2,
        text=f"العَصر",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Salat_Maghrib = ctk.CTkLabel(
        fram2,
        text=f"المَغرب",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Salat_Isha = ctk.CTkLabel(
        fram2,
        text=f"العِشاء",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )

    Time_Fajr = ctk.CTkLabel(
        fram2,
        text=f"{times[0]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Time_Sunrise = ctk.CTkLabel(
        fram2,
        text=f"{times[1]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Time_Dhuhr = ctk.CTkLabel(
        fram2,
        text=f"{times[2]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Time_Asr = ctk.CTkLabel(
        fram2,
        text=f"{times[3]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Time_Maghrib = ctk.CTkLabel(
        fram2,
        text=f"{times[4]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )
    Time_Isha = ctk.CTkLabel(
        fram2,
        text=f"{times[5]}",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color
    )


    index = -1
    now = datetime.datetime.now()
    now_hour = int(now.strftime("%H"))
    now_min = int(now.strftime("%M"))
    current_time = now.strftime("%H:%M")

    for x in range(len(times)):
        time = times[x].split(':')
        next_hours = int(time[0])
        next_min = int(time[1])
        if times[x] > current_time:
            if x == 0:
                Salat_Fajr.configure(text_color=green_2)
                Time_Fajr.configure(text_color=green_2)
            elif x == 1:
                Salat_Sunrise.configure(text_color=green_2)
                Time_Sunrise.configure(text_color=green_2)
            elif x == 2:
                Salat_Dhuhr.configure(text_color=green_2)
                Time_Dhuhr.configure(text_color=green_2)
            elif x == 3:
                Salat_Asr.configure(text_color=green_2)
                Time_Asr.configure(text_color=green_2)
            elif x == 4:
                Salat_Maghrib.configure(text_color=green_2)
                Time_Maghrib.configure(text_color=green_2)
            elif x == 5:
                Salat_Isha.configure(text_color=green_2)
                Time_Isha.configure(text_color=green_2)
            next_salat = salat[x]
            index = x
            break
        elif current_time > times[-1]:
            Salat_Fajr.configure(text_color=green_2)
            Time_Fajr.configure(text_color=green_2)
            break


    fram4 = ctk.CTkFrame(fram2, fg_color=main_back_col)
    next_alaram_label = ctk.CTkLabel(

        fram4,
        text=f'الوقت المتبقي لأذان ',
        font=ctk.CTkFont('cairo', 20),
        text_color=dark_color
    )
    next_alaram_label2 = ctk.CTkLabel(

        fram4,
        text=f'{arabic_salat[index]}',
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=green_2
    )

    next_alaram_label3 = ctk.CTkLabel(

        fram4,
        text=f'هو',
        font=ctk.CTkFont('cairo', 20),
        text_color=dark_color
    )
    next_alaram_label4 = ctk.CTkLabel(

        fram4,
        text=f'{remanning_time}',
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=green_2
    )

    remanning_time = (datetime.timedelta(
        hours=next_hours, minutes=next_min) - datetime.timedelta(hours=now_hour, minutes=now_min))

    remanning_time = str(remanning_time).split()
    remanning_time = remanning_time[-1][:-3]
    
    next_alaram_label4.configure(text=remanning_time)
    notification()

    button2_default_value = "test"
    if json_not_state == True:
        button2_default_value = "on"
    else:
        button2_default_value = "off"

    switch_var = ctk.StringVar(value=button2_default_value)

    def button_event():
        setting_button.configure(state=ctk.DISABLED)

        top = CTkToplevel(app,fg_color=sec_back_col)
        top_frame = ctk.CTkFrame(top,fg_color=sec_back_col)
        top.resizable(False, False)
        top.title("settings")
        icon_path = "\icon.ico"
        top.iconbitmap(os.getcwd()+icon_path)

        top.geometry(
            "%dx%d+%d+%d" %
            (800/2-40, 480/2 + 50, app.winfo_x() + 800/4, app.winfo_y() + 480/4))
        country_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Enter Country",
            font=ctk.CTkFont('cairo', 20),
        )
        City_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Enter City",
            font=ctk.CTkFont('cairo', 20),
        )
        country_label = ctk.CTkLabel(
            top_frame,
            text="Country",
            font=ctk.CTkFont('cairo', 20, weight='bold'),

        )
        City_label = ctk.CTkLabel(
            top_frame,
            text="City",
            font=ctk.CTkFont('cairo', 20, weight='bold'),

        )
        
        def disable_event():
            setting_button.configure(state=ctk.NORMAL)
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", disable_event)

        def save():
            if country_entry.get() and City_entry.get():
                config_data['Country'] = country_entry.get()
                config_data['City'] = City_entry.get()

                update_config(config_data)
                setting_button.configure(state=ctk.NORMAL)
                top.destroy()
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                if switch_var.get() == "on":
                    config_data["not_state"] = True
                elif switch_var.get() == "off":
                    config_data["not_state"] = False
                update_config(config_data)
                # print(json_not_state)
                setting_button.configure(state=ctk.NORMAL)
                top.destroy()

        button = ctk.CTkButton(
            top_frame, command=save, text='Save', fg_color=green_1,
            text_color='black',
            hover_color=green_2,
            font=ctk.CTkFont('cairo', 18, weight='bold'),

        )

        def switch_event():
            global switch_var
            # print("switch toggled, current value:", switch_var.get())

        button2 = ctk.CTkSwitch(
            top_frame, text="Notfication State", progress_color=green_1,
            font=ctk.CTkFont('cairo', 18, weight='bold'),
            command=switch_event,
            variable=switch_var, onvalue="on", offvalue="off"

        )
        top_frame.place(relx=0.5, rely=0.5, anchor='center')
        country_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        country_entry.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        City_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
        City_entry.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))
        button.grid(row=6, column=0, columnspan=2,
                    padx=(10, 10), pady=(10, 10))
        button2.grid(row=5, column=0, columnspan=2,padx=(10, 10), pady=(10, 10))

        top.attributes('-topmost', 'true')

    setting_button = ctk.CTkButton(
        master=app,
        width=10,
        height=10,
        corner_radius=900,
        text="",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color,
        bg_color="transparent",
        fg_color="transparent",
        hover_color=sec_back_col,
        image=setting_img,
        state=ctk.NORMAL,
        command=button_event)
    
    logo = ctk.CTkLabel(
        master=app,
        width=10,
        height=10,
        corner_radius=900,
        text="   Prayer",
        font=ctk.CTkFont('cairo', 20, weight='bold'),
        text_color=dark_color,
        bg_color="transparent",
        fg_color="transparent",
        image=logo_img,
        compound="left"
    )
    logo2 = ctk.CTkLabel(
        master=app,
        width=10,
        height=10,
        corner_radius=900,
        text="Times",
        font=ctk.CTkFont('cairo', 20),
        text_color=dark_color,
        bg_color="transparent",
        fg_color="transparent",
        compound="left"
    )
        
    img_Fajr = ctk.CTkLabel(
        fram2,
        text=' ',
        image=fajr_img
    )
    img_Sunrise = ctk.CTkLabel(
        fram2,
        text=' ',
        image=sunrise_img
    )
    img_Dhuhr = ctk.CTkLabel(
        fram2,
        text=' ',
        image=dhuhr_img
    )
    img_Asr = ctk.CTkLabel(
        fram2,
        text=' ',
        image=asr_img
    )
    img_Maghrib = ctk.CTkLabel(
        fram2,
        text=' ',
        image=maghrib_img
    )
    img_Isha = ctk.CTkLabel(
        fram2,
        text=' ',
        image=isha_img
    )

    fram0.grid(row=0,column=2,columnspan=8,rowspan=10,padx=(10,10),pady=(50,0))
    
    setting_button.grid(row=4, column=0, sticky='n',padx=(10, 0), pady=(70, 5))
    logo.place(x=10,y=10)
    logo2.place(x=124,y=10)
    fram1.grid(row=1, column=0,padx=(100,1000),pady=(60,560))
    city_label.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
    img_city.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=(10, 10))
    img_country.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(10, 10))
    country_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))

    fram2.grid(row=3, column=0, columnspan=2,padx=(10, 10), pady=(10, 10))
    fram4.grid(row=0, column=0, columnspan=6, padx=(10, 10), pady=(10, 10))

    Salat_Fajr.grid(row=3, column=5, padx=(10, 10), pady=(10, 10))
    Salat_Sunrise.grid(row=3, column=4, padx=(10, 10), pady=(10, 10))
    Salat_Dhuhr.grid(row=3, column=3, padx=(10, 10), pady=(10, 10))
    Salat_Asr.grid(row=3, column=2, padx=(10, 10), pady=(10, 10))
    Salat_Maghrib.grid(row=3, column=1, padx=(10, 10), pady=(10, 10))
    Salat_Isha.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

    img_Fajr.grid(row=4, column=5, padx=(10, 10), pady=(10, 10))
    img_Sunrise.grid(row=4, column=4, padx=(10, 10), pady=(10, 10))
    img_Dhuhr.grid(row=4, column=3, padx=(10, 10), pady=(10, 10))
    img_Asr.grid(row=4, column=2, padx=(10, 10), pady=(10, 10))
    img_Maghrib.grid(row=4, column=1, padx=(10, 10), pady=(10, 10))
    img_Isha.grid(row=4, column=0, padx=(10, 10), pady=(10, 10))

    Time_Fajr.grid(row=5, column=5, padx=(10, 10), pady=(10, 10))
    Time_Sunrise.grid(row=5, column=4, padx=(10, 10), pady=(10, 10))
    Time_Dhuhr.grid(row=5, column=3, padx=(10, 10), pady=(10, 10))
    Time_Asr.grid(row=5, column=2, padx=(10, 10), pady=(10, 10))
    Time_Maghrib.grid(row=5, column=1, padx=(10, 10), pady=(10, 10))
    Time_Isha.grid(row=5, column=0, padx=(10, 10), pady=(10, 10))

    next_alaram_label.grid(row=0, column=3, columnspan=3,padx=(5, 5), pady=(5, 5))
    next_alaram_label2.grid(row=0, column=2, columnspan=1,padx=(5, 5), pady=(5, 5))
    next_alaram_label3.grid(row=0, column=1, columnspan=1,padx=(5, 5), pady=(5, 5))
    next_alaram_label4.grid(row=0, column=0, columnspan=1,padx=(5, 5), pady=(5, 5))

    app.mainloop()
