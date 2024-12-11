import tkinter as tk
from tkinter import ttk, messagebox
import requests
from noaa_coops import Station
import datetime
from datetime import timedelta
import math

def fetch_station_id():
    station_name = station_name_entry.get()
    try:
        response = requests.get(f'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json')
        stations = response.json()
        
        # Attempt to find the station by name
        for station in stations['stations']:
            if station_name.lower() in station['name'].lower():
                station_id_entry.delete(0, tk.END)
                station_id_entry.insert(0, station['id'])
                return
        
        # If station not found, notify the user
        messagebox.showinfo("Info", "Station not found, please enter the ID manually.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch station data: {e}")

def fetch_tide_data():
    station_id = station_id_entry.get()
    date = date_entry.get()
    try:
        data = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={date}&range=24&station={station_id}&product=predictions&interval=hilo&datum=MLLW&time_zone=lst_ldt&units=english&application=DataAPI_Sample&format=json')
        display_data(data.json())

    except Exception as e:
        messagebox.showerror("Error," f"Failed to fetch data: {e}")

def display_data(data):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"{'Time':<15}{'Height (ft)':<15}{'Height (m)':<15}\n")
    result_text.insert(tk.END, "-"*45 + "\n")
    print(f"here {data}")
    for row in data['predictions']:
        time = row['t']
        height_ft = float(row['v']) * 3.28084
        height_m = float(row['v'])
        result_text.insert(tk.END, f"{time:<15}{height_ft:<15.2f}{height_m:<15.2f}\n")

def calculate_squat():
    try:
        block_coefficient = float(block_coefficient_entry.get())
        speed_of_transit = float(speed_of_transit_entry.get())

        squat = (block_coefficient * (speed_of_transit ** 2)) / 100

        messagebox.showinfo("Squat Calculation", f"Estimated Squat: {squat:.2f} meters")
        squat_entry.delete(0, tk.END)
        squat_entry.insert(0, squat)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def calculate_under_keel_clearance():
    try:
        shallowest_depth =  float(shallowest_depth_entry.get())
        deep_draft = float(deep_draft_entry.get())
        lowest_tide = float(lowest_tide_entry.get())
        squat = float(squat_entry.get())

        if squat is None or lowest_tide is None:
            raise ValueError("Error in fetching squat or tide data.")
        
        under_keel_clearance = shallowest_depth + lowest_tide - (deep_draft + squat)
        messagebox.showinfo("Under Keel Clearance", f"Estimated Under Keel Clearance: {under_keel_clearance:.2f} meters")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for all inputs.")

def height_of_tide():
    
    hour_of_passage = hour_of_passage_entry.get()
    minute_of_passage = minute_of_passage_entry.get()
    time_of_passage_delta = timedelta(hours=hour_of_passage, minutes=minute_of_passage)

    #Mid-Time Calculation
    time_high = timedelta(hours=, minutes=)
    time_low = timedelta(hours=, minutes=)

    if time_high > time_low:
        time_mid = (time_high - time_low) / 2
    else:
        time_mid = (time_low - time_high) / 2

    #Tidal Range Calculation
    tidal_median = (height_high - height_low) / 2
    tidal_range = height_high - height_low

    global tidal_prediction
    tidal_prediction = (tidal_median + tidal_range) * ((math.pi * (time_of_passage_delta - time_mid)) / (time_high - time_low))


root = tk.Tk()
root.title("UKC Calculator")

tk.Label(root, text="Tide Station Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
station_name_entry = ttk.Entry(root)
station_name_entry.grid(row=0, column=1, padx=10, pady=5)

search_button = ttk.Button(root, text="Search Station ID", command=fetch_station_id)
search_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Tide Station ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
station_id_entry = ttk.Entry(root)
station_id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Date (YYYYMMDD):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
date_entry = ttk.Entry(root)
date_entry.grid(row=2, column=1, padx=10, pady=5)

fetch_button = ttk.Button(root, text="Fetch Tide Data", command=fetch_tide_data)
fetch_button.grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, width=50, height=15)
result_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

#Squat Calculator
tk.Label(root, text="Block Coefficient:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
block_coefficient_entry = ttk.Entry(root)
block_coefficient_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Speed of Transit (knots):").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
speed_of_transit_entry = ttk.Entry(root)
speed_of_transit_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Squat (meters):").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
squat_entry = ttk.Entry(root)
squat_entry.grid(row=7, column=1, padx=10, pady=5)

calculate_button = ttk.Button(root, text="Calculate Squat", command=calculate_squat)
calculate_button.grid(row=8, column=0, columnspan=2, pady=10)

#UKC Calculator
tk.Label(root, text="Lowest Tide (meters):").grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)
lowest_tide_entry = ttk.Entry(root)
lowest_tide_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Shallowest Depth on Route (meters):").grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)
shallowest_depth_entry = ttk.Entry(root)
shallowest_depth_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Vessel Deep Draft (meters):").grid(row=11, column=0, padx=10, pady=5, sticky=tk.W)
deep_draft_entry = ttk.Entry(root)
deep_draft_entry.grid(row=11, column=1, padx=10, pady=5)

calculateUKC_button = ttk.Button(root, text="Calculate Under Keel Clearance", command=calculate_under_keel_clearance)
calculateUKC_button.grid(row=12, column=0, columnspan=2, pady=10)

tk.Label(root, text="Hour of Passage:").grid(row=13, column=0, padx=10, pady=5, sticky=tk.W)
hour_of_passage_entry = ttk.Entry(root)
hour_of_passage_entry.grid(row=13, column=1, padx=10, pady=5)

tk.Label(root, text="Minute of Passage:").grid(row=14, column=0, padx=10, pady=5, sticky=tk.W)
minute_of_passage_entry = ttk.Entry(root)
minute_of_passage_entry.grid(row=14, column=1, padx=10, pady=5)

root.mainloop()
