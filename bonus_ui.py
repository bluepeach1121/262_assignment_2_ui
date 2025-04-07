import tkinter as tk
from tkinter import messagebox
import random

class RouletteGame:
    def __init__(self, master):
        self.master = master
        master.title("Digital Roulette Game")
        self.balance = 100
        self.balance_label = tk.Label(master, text=f"Balance: ${self.balance}")
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.bet_label = tk.Label(master, text="Bet Amount:")
        self.bet_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.bet_entry = tk.Entry(master)
        self.bet_entry.grid(row=1, column=1, padx=5)
        
        self.pos_label = tk.Label(master, text="Bet Number (0-37, 37=00):")
        self.pos_label.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.pos_entry = tk.Entry(master)
        self.pos_entry.grid(row=2, column=1, padx=5)
        
        self.place_bet_button = tk.Button(master, text="Place Bet", command=self.place_bet)
        self.place_bet_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.bet_listbox = tk.Listbox(master, width=40)
        self.bet_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.spin_button = tk.Button(master, text="Spin", command=self.spin)
        self.spin_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.result_label = tk.Label(master, text="Result: ")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.bets = []

    def place_bet(self):
        try:
            bet_amount = int(self.bet_entry.get())
            bet_number = int(self.pos_entry.get())
            if bet_number < 0 or bet_number > 37:
                raise ValueError("Bet number must be between 0 and 37")
            if bet_amount <= 0:
                raise ValueError("Bet amount must be positive")
            if bet_amount > self.balance:
                messagebox.showerror("Error", "Insufficient balance for this bet.")
                return
            # Store bet
            self.bets.append((bet_number, bet_amount))
            self.bet_listbox.insert(tk.END, f"Bet: ${bet_amount} on {bet_number}")
            # Clear entries
            self.bet_entry.delete(0, tk.END)
            self.pos_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
    
    def spin(self):
        if not self.bets:
            messagebox.showinfo("Info", "Please place a bet first!")
            return
        winning_number = random.randint(0, 37)
        result_text = f"Winning Number: {winning_number}\n"
        round_payout = 0
        
        for bet in self.bets:
            bet_num, bet_amt = bet
            if bet_num == winning_number:
                win_amt = bet_amt * 36
                round_payout += win_amt
                result_text += f"Bet on {bet_num} won ${win_amt}!\n"
            else:
                round_payout -= bet_amt
                result_text += f"Bet on {bet_num} lost ${bet_amt}.\n"
        
        self.balance += round_payout
        result_text += f"New Balance: ${self.balance}"
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.result_label.config(text=result_text)
        
        self.bets = []
        self.bet_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = RouletteGame(root)
    root.mainloop()
