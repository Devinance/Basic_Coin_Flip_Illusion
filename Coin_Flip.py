import tkinter as tk
from PIL import Image, ImageTk
import random
import requests
from io import BytesIO

class CoinFlipGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Coin Flip Illusion")
        self.master.geometry("300x400")
        self.master.resizable(False, False)

        # URLs for the images
        heads_url = "https://example.com/heads.png"
        tails_url = "https://example.com/tails.png"

        # Load images from URLs
        self.heads_image = self.load_image_from_url(heads_url)
        self.tails_image = self.load_image_from_url(tails_url)

        # Frame to hold everything
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill='both')

        # Label for instructions
        self.instruction_label = tk.Label(self.main_frame, text="Guess the outcome of the coin flip:", font=("Arial", 14))
        self.instruction_label.pack(pady=10)

        # Frame for buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)

        # Buttons for user choice
        self.heads_button = tk.Button(self.button_frame, text="Heads", command=lambda: self.start_flip("heads"))
        self.heads_button.pack(side=tk.LEFT, padx=5)

        self.tails_button = tk.Button(self.button_frame, text="Tails", command=lambda: self.start_flip("tails"))
        self.tails_button.pack(side=tk.LEFT, padx=5)

        # Label to show coin image
        self.coin_label = tk.Label(self.main_frame)
        self.coin_label.pack(pady=20)

        # Label to show result
        self.result_label = tk.Label(self.main_frame, font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=5)

        # Restart button to play again
        self.restart_button = tk.Button(self.main_frame, text="Play Again", command=self.reset_game, state=tk.DISABLED)
        self.restart_button.pack(pady=5)

        # Variables to store state
        self.user_choice = None
        self.flipping = False
        self.flip_count = 0
        self.max_flips = 20  # number of image toggles before stopping
        self.flip_delay = 100  # delay in ms between flips
        self.current_image = self.heads_image  # start with heads

    def load_image_from_url(self, url):
        response = requests.get(url)
        image_data = BytesIO(response.content)
        img = Image.open(image_data).resize((200, 200), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def start_flip(self, user_choice):
        # Disable guess buttons during flipping
        self.heads_button.config(state=tk.DISABLED)
        self.tails_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.user_choice = user_choice

        # Start the animation
        self.flipping = True
        self.flip_count = 0
        self.animate_coin()

    def animate_coin(self):
        if not self.flipping:
            return

        # Toggle the image
        self.current_image = self.tails_image if self.current_image == self.heads_image else self.heads_image
        self.coin_label.config(image=self.current_image)

        self.flip_count += 1

        if self.flip_count < self.max_flips:
            # Continue flipping
            self.master.after(self.flip_delay, self.animate_coin)
        else:
            # Stop flipping and show final result
            self.flipping = False
            sel
