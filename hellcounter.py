import os
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import requests
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to download the gif
def download_gif(url):
    response = requests.get(url)
    if response.status_code == 200:
        gif_data = io.BytesIO(response.content)
        return Image.open(gif_data)
    else:
        raise Exception("Failed to download gif")

# Function to update player count periodically
def update_player_count(label):
    steam_api_key = os.getenv("STEAM_API_KEY")
    if steam_api_key:
        try:
            response = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=553850&key={steam_api_key}")
            data = response.json()
            player_count = data['response']['player_count']
            label.config(text=f"Current Defenders of Democracy: {player_count}")
        except Exception as e:
            print(f"Error fetching player count: {e}")
    else:
        print("STEAM_API_KEY not found in environment variables.")
    label.after(60000, update_player_count, label)  # Update every 60 seconds

# Initialize main window
root = tk.Tk()
root.title("Defenders of Democracy")
root.geometry("400x300")

# Create a label to display the player count with a black background and white font
player_count_label = Label(root, text="Loading player count...", bg="black", fg="white")
player_count_label.pack(side="top", fill="x")

# Download the gif
gif_url = "https://c.tenor.com/l9D2veYHMXwAAAAC/tenor.gif"
gif = download_gif(gif_url)

# Load and prepare the gif frames
frames = []  # List to hold the frames
try:
    while True:
        # Copy the current frame and append it to the frames list
        frames.append(ImageTk.PhotoImage(gif.copy()))
        gif.seek(gif.tell() + 1)  # Move to the next frame
except EOFError:
    pass  # End of sequence

gif.close()

# Function to animate the GIF
def update_gif(label, frames, current_frame):
    frame = frames[current_frame]
    label.configure(image=frame)
    next_frame = (current_frame + 1) % len(frames)  # Loop back to first frame
    root.after(40, update_gif, label, frames, next_frame)  # Update frame every 40ms

# Set up the gif label
gif_label = Label(root)
gif_label.pack()

# Start the GIF animation and update the player count
update_gif(gif_label, frames, 0)
update_player_count(player_count_label)

root.mainloop()
