import tkinter as tk
from tkinter import ttk, messagebox
import requests
from noaa_coops import Station

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

root.mainloop()
