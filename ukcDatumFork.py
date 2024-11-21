import tkinter as tk
from tkinter import ttk, messagebox
import requests
from noaa_coops import Station

def search_stations():
    station_name = station_search_entry.get()
    try:
        response = requests.get('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json')
        stations = response.json()

        # Filter stations by name
        matching_stations = [station for station in stations['stations'] if station_name.lower() in station['name'].lower()]

        # Populate the listbox with matching stations
        station_listbox.delete(0, tk.END)
        for station in matching_stations:
            station_listbox.insert(tk.END, f"{station['name']} ({station['id']})")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search stations: {e}")

def on_station_select(event):
    selection = station_listbox.curselection()
    if selection:
        station_info = station_listbox.get(selection[0])
        station_name, station_id = station_info.rsplit('(', 1)
        station_name_entry.config(state='normal')
        station_name_entry.delete(0, tk.END)
        station_name_entry.insert(0, station_name.strip())
        station_name_entry.config(state='readonly')
        station_id_entry.delete(0, tk.END)
        station_id_entry.insert(0, station_id.strip(')'))

def fetch_station_id():
    station_id = station_id_entry.get()
    try:
        response = requests.get(f'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station_id}.json')
        
        # Check if the response is valid
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to fetch station data: {response.status_code}")
            return

        # Print the response content for debugging
        print(f"Response content: {response.content}")
        
        # Check if the response content is empty
        if not response.content:
            messagebox.showerror("Error", "Received empty response from the API.")
            return
        
        station_info = response.json()

        if 'stations' in station_info and len(station_info['stations']) > 0:
            station_name = station_info['stations'][0]['name']
            station_name_entry.config(state='normal')
            station_name_entry.delete(0, tk.END)
            station_name_entry.insert(0, station_name)
            station_name_entry.config(state='readonly')
            
            # Use the 'self' URL for datums from the station information
            datums_url = station_info['stations'][0]['datums']['self']
            datums_response = requests.get(datums_url)
            
            # Check if the datums response is valid
            if datums_response.status_code != 200:
                messagebox.showerror("Error", f"Failed to fetch datums data: {datums_response.status_code}")
                return
            
            datums_info = datums_response.json()
            available_datums = [datum['datum'] for datum in datums_info['datums']]
            
            datum_combo['values'] = available_datums
            datum_combo.set(available_datums[0])
        else:
            messagebox.showinfo("Info", "Station not found, please enter a valid ID.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch station data: {e}")

def fetch_tide_data():
    station_id = station_id_entry.get()
    date = date_entry.get()
    datum = datum_combo.get()
    try:
        station = Station(id=station_id)
        data = station.get_data(begin_date=date, end_date=date, product='predictions', datum=datum)
        display_data(data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

def display_data(data):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"{'Time':<15}{'Height (ft)':<15}{'Height (m)':<15}\n")
    result_text.insert(tk.END, "-"*45 + "\n")
    for _, row in data.iterrows():
        time = row['t']
        height_ft = row['v'] * 3.28084
        height_m = row['v']
        result_text.insert(tk.END, f"{time:<15}{height_ft:<15.2f}{height_m:<15.2f}\n")

root = tk.Tk()
root.title("Tide Data Fetcher")

tk.Label(root, text="Search Tide Station Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
station_search_entry = ttk.Entry(root)
station_search_entry.grid(row=0, column=1, padx=10, pady=5)

search_button = ttk.Button(root, text="Search", command=search_stations)
search_button.grid(row=0, column=2, padx=10, pady=5)

station_listbox = tk.Listbox(root, height=6)
station_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
station_listbox.bind('<<ListboxSelect>>', on_station_select)

tk.Label(root, text="Tide Station ID:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
station_id_entry = ttk.Entry(root)
station_id_entry.grid(row=2, column=1, padx=10, pady=5)

confirm_button = ttk.Button(root, text="Confirm Station ID", command=fetch_station_id)
confirm_button.grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Tide Station Name:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
station_name_entry = ttk.Entry(root)
station_name_entry.grid(row=3, column=1, padx=10, pady=5)
station_name_entry.config(state='readonly')

tk.Label(root, text="Date (YYYYMMDD):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
date_entry = ttk.Entry(root)
date_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Datum:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
datum_combo = ttk.Combobox(root)
datum_combo.grid(row=5, column=1, padx=10, pady=5)

fetch_button = ttk.Button(root, text="Fetch Tide Data", command=fetch_tide_data)
fetch_button.grid(row=6, column=0, columnspan=3, pady=10)

result_text = tk.Text(root, width=50, height=15)
result_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
