import tkinter as tk
from tkinter import ttk, messagebox
import datetime

length_list = []
char_loop = ""
timer_loop = ""
start_time = 0
now = datetime.datetime.now()

def start():
    """If the timer and character counter are not running, it starts them."""
    if char_loop == "":
        counter()
    if timer_loop == "":
        timer()
        radiobutton1.configure(state="disabled")
        radiobutton2.configure(state="disabled")
        radiobutton3.configure(state="disabled")
        radiobutton4.configure(state="disabled")
        radiobutton5.configure(state="disabled")
        export.configure(state="disabled")


def counter():
    """Counts the characters and deletes all the text after 5 seconds"""
    global char_loop
    # Current text length:
    text_input = text.get("1.0", "end-1c")
    length_list.append(len(text_input.replace(" ", "")))

    text.configure(state="normal")
    text.focus()

    if len(length_list) > 5:
        length_list.pop(0)
        # 5 sec difference + window color change:
        diff_5 = length_list[4] - length_list[0]
        if length_list[4] != 0:
            if diff_5 == 0:
                text.delete("1.0", tk.END)
                window.configure(bg="#ff2323")
            elif length_list[4] == length_list[1]:
                window.configure(bg="#ff5656")
            elif length_list[4] == length_list[2]:
                window.configure(bg="#ff7e7e")
        else:
            window.configure(bg=orig_color)
    char_loop = window.after(1000, counter)
    return char_loop


def reset():
    """Deletes the text, stops the counter function, stops and resets the timer"""
    global start_time, timer_loop, char_loop
    start_time = 0
    text.delete("1.0", tk.END)
    window.after_cancel(char_loop)
    window.after_cancel(timer_loop)
    char_loop = ""
    timer_loop = ""
    length_list.clear()
    radiobutton1.configure(state="normal")
    radiobutton2.configure(state="normal")
    radiobutton3.configure(state="normal")
    radiobutton4.configure(state="normal")
    radiobutton5.configure(state="normal")


def timer():
    """Based on the set time limit, it counts down to 0"""
    global start_time, timer_loop
    if start_time == 0:
        start_time = set_time() * 60
        export.configure(state="normal")
    # print(start_time)
    if start_time > 0:
        start_time -= 1
        pb['value'] = start_time * 100 / (set_time() * 60)
        timer_loop = window.after(1000, timer)
        return timer_loop


def export_text():
    """When the countdown is over, the user can export the text in a txt file."""
    final_text = text.get("1.0", "end-1c")
    with open(f"my_text_{now}.txt", "w") as file:
        file.write(final_text)
    tk.messagebox.showinfo(title="Success", message=f"Successful file export: {file.name}")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.config(padx=25, pady=25)
window.title("Evil Notebook")

orig_color = window.cget("background")

text = tk.Text(height=40, width=75, wrap=tk.WORD)
# Buttons:
start = tk.Button(text="Start writing", command=start)
reset = tk.Button(text="Reset", command=reset)
export = tk.Button(text="Export", command=export_text)
export.configure(state="disabled")

# Progress Bar:
pb = ttk.Progressbar(
    window,
    orient="horizontal",
    mode="determinate",
    length=500
)

# Radio buttons:
def set_time():
    """From the radio button selection returns the value"""
    # print(radio_state.get())
    return radio_state.get()


radio_state = tk.IntVar()
radiobutton1 = tk.Radiobutton(text="3 min", value=3, variable=radio_state)
radiobutton1.select()
radiobutton2 = tk.Radiobutton(text="5 min", value=5, variable=radio_state)
radiobutton3 = tk.Radiobutton(text="10 min", value=10, variable=radio_state)
radiobutton4 = tk.Radiobutton(text="15 min", value=15, variable=radio_state)
radiobutton5 = tk.Radiobutton(text="20 min", value=20, variable=radio_state)
# Grid:
radiobutton1.grid(column=0, row=0)
radiobutton2.grid(column=1, row=0)
radiobutton3.grid(column=2, row=0)
radiobutton4.grid(column=3, row=0)
radiobutton5.grid(column=4, row=0)

start.grid(column=1, row=1)
reset.grid(column=2, row=1)
export.grid(column=3, row=1)
pb.grid(column=0, row=2, columnspan=5)
text.grid(column=0, row=3, columnspan=5)

window.mainloop()
