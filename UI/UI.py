# tkinter window 600 by 400 pixels
# 2 buttons, 1 label, 1 entry box
# if i click the button_1 the candle chart will be shown using View_Price.py
# if i click the button_1 again the candle chart will be closed
# if i click the button_2 the current price of the coin will be shown using Get_Current_Price.py
# if i click the button_2 again the current price of the coin will be closed
# use Class to make the code more readable

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from API import Get_Candle as gc
from API import Get_Current_Price as gcp
from Chart import View_Candle as vc
from Calcuate_Methods.RSI import rsi

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UI")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.button_1 = ttk.Button(self, text="View Candle", command=self.view_candle)
        self.button_1.place(x=50, y=50)
        self.button_2 = ttk.Button(self, text="View Current Price", command=self.view_current_price)
        self.button_2.place(x=50, y=100)
        self.label_1 = ttk.Label(self, text="Market Code")
        self.label_1.place(x=50, y=150)
        self.entry_1 = ttk.Entry(self)
        self.entry_1.place(x=150, y=150)
        self.label_2 = ttk.Label(self, text="Counts")
        self.label_2.place(x=50, y=200)
        self.entry_2 = ttk.Entry(self)
        self.entry_2.place(x=150, y=200)
        self.label_3 = ttk.Label(self, text="Units")
        self.label_3.place(x=50, y=250)
        self.entry_3 = ttk.Entry(self)
        self.entry_3.place(x=150, y=250)
        self.label_4 = ttk.Label(self, text="View Candle")
        self.label_4.place(x=50, y=300)
        self.label_5 = ttk.Label(self, text="View Current Price")
        self.label_5.place(x=50, y=350)
        self.label_6 = ttk.Label(self, text="Total Balance")
        self.label_6.place(x=1000, y=50)


        self.button_3 = ttk.Button(self, text="Exit", command=self.exit)
        self.button_3.place(x=50, y=500)
        self.button_4 = ttk.Button(self, text="Start Algorithm", command=self.start_algorithm)
        self.button_4.place(x=1000, y=100)

    def start_algorithm(self):
        return

    def view_candle(self):
        # if figure1 is already open, close it
        plt.close()

        market_code = self.entry_1.get()
        if market_code == "":
            market_code = "KRW-BTC"
        unit = self.entry_3.get()
        if unit == "":
            unit = "days"
        count = self.entry_2.get()
        if count == "":
            count = "200"
        candle_df = vc.view_candle(market_code, unit, count)
        mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code)

    def view_current_price(self):
        market_code = self.entry_1.get()
        if market_code == "":
            market_code = "KRW-BTC"
        current_price = gcp.get_current_price(market_code)
        self.label_5.configure(text="View Current Price            " + str(current_price))

    def exit(self):
        self.destroy()

if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
