import tkinter as tk
from tkinter import simpledialog
import calendar

def show_calendar():
    root = tk.Tk()
    root.withdraw()

    year = simpledialog.askinteger("input", "masukkan tahun (YYYY):")
    month = simpledialog.askinteger("input", "masukkan bulan (1-12):")

    if year and month:
        cal = calendar.TextCalendar(calendar.SUNDAY)
        cal_str = cal.formatmonth(year, month)

        calendar_window = tk.Toplevel(root)
        calendar_window.title(f"kalender - {month}/{year}")

        label = tk.Label(calendar_window, text=cal_str, font=("courier", 14), justify=tk.LEFT)
        label.pack(padx=20, pady=20)

        close_button = tk.Button(calendar_window, text="tutup", command=calendar_window.destroy)
        close_button.pack(pady=10)

        root.mainloop()

show_calendar()