import tkinter as tk
from PIL import Image, ImageTk
import random
import os
from tkinter import messagebox

class CoinFlipGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Coin Flip Illusion")
        self.master.geometry("400x500")
        self.master.configure(bg="#f0f0f0")
        
        # Statistics
        self.wins = 0
        self.losses = 0
        self.total_flips = 0
        
        # Use local images instead of URLs
        # You'll need to create or download coin images and place them in the same directory
        # For now, we'll create placeholder images
        self.create_placeholder_images()
        
        # Main container with some padding and styling
        self.main_frame = tk.Frame(master, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill='both')
        
        # Title with better styling
        self.title_label = tk.Label(
            self.main_frame, 
            text="COIN FLIP CHALLENGE", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.title_label.pack(pady=10)
        
        # Instruction with better text
        self.instruction_label = tk.Label(
            self.main_frame, 
            text="Can you predict the outcome?", 
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="#555555"
        )
        self.instruction_label.pack(pady=10)
        
        # Statistics display
        self.stats_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.stats_frame.pack(pady=5)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="Wins: 0 | Losses: 0 | Win Rate: 0%",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#555555"
        )
        self.stats_label.pack()
        
        # Frame for buttons with better styling
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.button_frame.pack(pady=15)
        
        # Improved button styling
        button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 10,
            "border": 0,
            "padx": 15,
            "pady": 8,
            "cursor": "hand2"
        }
        
        self.heads_button = tk.Button(
            self.button_frame, 
            text="HEADS", 
            command=lambda: self.start_flip("heads"),
            bg="#4CAF50",
            fg="white",
            **button_style
        )
        self.heads_button.pack(side=tk.LEFT, padx=10)
        
        self.tails_button = tk.Button(
            self.button_frame, 
            text="TAILS", 
            command=lambda: self.start_flip("tails"),
            bg="#2196F3",
            fg="white",
            **button_style
        )
        self.tails_button.pack(side=tk.LEFT, padx=10)
        
        # Label to show coin image with border
        self.coin_frame = tk.Frame(
            self.main_frame,
            bd=2,
            relief=tk.GROOVE,
            bg="#e0e0e0",
            padx=10,
            pady=10
        )
        self.coin_frame.pack(pady=15)
        
        self.coin_label = tk.Label(self.coin_frame, bg="#e0e0e0")
        self.coin_label.pack()
        
        # Display initial coin image
        self.coin_label.config(image=self.heads_image)
        
        # Label to show result with improved styling
        self.result_label = tk.Label(
            self.main_frame, 
            text="", 
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        )
        self.result_label.pack(pady=15)
        
        # Restart button with better styling
        self.restart_button = tk.Button(
            self.main_frame, 
            text="PLAY AGAIN", 
            command=self.reset_game,
            bg="#FF5722",
            fg="white",
            state=tk.DISABLED,
            **button_style
        )
        self.restart_button.pack(pady=5)
        
        # Variables to store state
        self.user_choice = None
        self.flipping = False
        self.flip_count = 0
        self.max_flips = 15  # reduced for better UX
        self.flip_delay = 80  # slightly faster
        self.current_image = self.heads_image
    
    def create_placeholder_images(self):
        # Create simple placeholder coin images
        # In a real app, you'd use actual image files
        
        # Create a canvas for heads
        heads_canvas = tk.Canvas(width=200, height=200)
        heads_canvas.create_oval(10, 10, 190, 190, fill="#FFD700", outline="#DAA520", width=3)
        heads_canvas.create_text(100, 100, text="H", font=("Arial", 80, "bold"), fill="#DAA520")
        
        # Convert canvas to image
        heads_canvas.update()
        heads_img = heads_canvas.postscript(colormode='color')
        img = Image.open(BytesIO(heads_img.encode('utf-8')))
        self.heads_image = ImageTk.PhotoImage(img)
        
        # Create a canvas for tails
        tails_canvas = tk.Canvas(width=200, height=200)
        tails_canvas.create_oval(10, 10, 190, 190, fill="#C0C0C0", outline="#A9A9A9", width=3)
        tails_canvas.create_text(100, 100, text="T", font=("Arial", 80, "bold"), fill="#A9A9A9")
        
        # Convert canvas to image
        tails_canvas.update()
        tails_img = tails_canvas.postscript(colormode='color')
        img = Image.open(BytesIO(tails_img.encode('utf-8')))
        self.tails_image = ImageTk.PhotoImage(img)
        
        # Alternative approach, just in case the canvas method doesn't work well
        try:
            # Create simple images using PIL directly
            heads = Image.new('RGB', (200, 200), color='#FFD700')
            tails = Image.new('RGB', (200, 200), color='#C0C0C0')
            
            self.heads_image = ImageTk.PhotoImage(heads)
            self.tails_image = ImageTk.PhotoImage(tails)
        except:
            # If all else fails, we'll just use colored labels
            pass

    def start_flip(self, user_choice):
        # Disable guess buttons during flipping
        self.heads_button.config(state=tk.DISABLED)
        self.tails_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.user_choice = user_choice
        
        # Let user know the flip is happening
        self.result_label.config(text="Flipping...", fg="#555555")
        
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
            # Vary the speed for more realistic effect - slower at the end
            delay = self.flip_delay + int(self.flip_count * 5)
            self.master.after(delay, self.animate_coin)
        else:
            # Stop flipping and show final result
            self.flipping = False
            self.show_result()
    
    def show_result(self):
        # Determine the result
        result = random.choice(["heads", "tails"])
        
        # Set the final image to match the result
        final_image = self.heads_image if result == "heads" else self.tails_image
        self.coin_label.config(image=final_image)
        
        # Update statistics
        self.total_flips += 1
        
        # Check if user guessed correctly
        if self.user_choice == result:
            self.wins += 1
            self.result_label.config(text="YOU WIN! It's " + result.upper(), fg="#4CAF50")
        else:
            self.losses += 1
            self.result_label.config(text="YOU LOSE! It's " + result.upper(), fg="#F44336")
        
        # Update statistics display
        win_rate = (self.wins / self.total_flips) * 100 if self.total_flips > 0 else 0
        stats_text = f"Wins: {self.wins} | Losses: {self.losses} | Win Rate: {win_rate:.1f}%"
        self.stats_label.config(text=stats_text)
        
        # Enable the restart button
        self.restart_button.config(state=tk.NORMAL)
    
    def reset_game(self):
        # Reset the game state
        self.coin_label.config(image=self.heads_image)
        self.current_image = self.heads_image
        self.result_label.config(text="")
        
        # Enable choice buttons
        self.heads_button.config(state=tk.NORMAL)
        self.tails_button.config(state=tk.NORMAL)
        
        # Disable restart button until next game
        self.restart_button.config(state=tk.DISABLED)

# Add the BytesIO import that was missing
from io import BytesIO

# Main function to run the app
def main():
    root = tk.Tk()
    app = CoinFlipGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()