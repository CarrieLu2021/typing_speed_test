from tkinter import *
from words import random_words
import random

# ----------------------------------- CONSTANTS -------------------------------------------------------
FONT = "Courier"
LB_FONT = "Courier", 25, "bold"
BG_COLOR = "#E3F2C1"
TXT_COLOR = "#41644A"
LB_COLOR = "#C9DBB2"
ENTRY_L = 38
ENTRY_S = 22
ONE_MIN = 60
TEST_WORDS = random_words

# ----------------------------------- VARIABLES -------------------------------------------------------
initial_msg = "Click here or type to start the test.\n"
timer = None
current_word = None
testing = False
# Words per minute (WPM) score
wpm = 0
test_time = ONE_MIN


# ----------------------------------- FUNCTIONS -------------------------------------------------------
def next_word():
    """Select a random word and display it."""
    global current_word
    current_word = random.choice(TEST_WORDS)
    canvas.itemconfig(word, text=current_word, font=(FONT, 35, "bold"), fill="black")
    check()


def restart():
    """Reset to initial state with a new random word."""
    # Cancel the timer if it's running.
    if timer is not None:
        root.after_cancel(timer)
    # Reset timer and WPM score.
    global test_time, wpm
    test_time = ONE_MIN
    wpm = 0
    # Reset UI to initial state.
    label_timer.config(text=f"Time left: {test_time}s ")
    label_wpm.config(text=f"WPM:___  ")
    next_word()
    user_entry.delete(0, END)
    user_entry.insert(END, initial_msg)
    user_entry.config(fg=TXT_COLOR, width=ENTRY_L)
    user_entry.bind("<Button>", click)
    user_entry.bind("<Key>", click)


def count_down(count):
    """Start the countdown and update WPM score when time is up."""
    # When time's not up yet, update countdown.
    global timer, wpm, current_word, testing
    label_timer.config(text=f"Time left: {count}s ")
    if count > 0:
        timer = root.after(1000, count_down, count - 1)
    else:
        # When time's up, stop the test and display WPM score.
        canvas.itemconfig(word, text=f"Time's up.\nYour WPM score is {wpm}.", font=(FONT, 24, "bold"), fill="#E86A33")
        current_word = None
        testing = False


def click(event):
    """Start the test when the user click on or type in the input field."""
    global testing
    testing = True
    user_entry.delete(0, END)
    user_entry.config(fg="black", width=ENTRY_S)
    user_entry.unbind("<Button>")
    user_entry.unbind("<Key>")
    count_down(test_time)
    check()


def check(*args):
    """Check whether the user's input matches the current word, if so, update WPM score and display next word."""
    global wpm, testing
    # Check when user click or type.
    if testing and current_word is not None:
        user_input = user_var.get().strip()
        # If user type the correct word, update WPM score and display next word.
        if user_input == current_word:
            wpm += 1
            label_wpm.config(text=f"WPM: {wpm}   ")
            user_entry.delete(0, END)
            next_word()


# ----------------------------------- UI SETUP -------------------------------------------------------

root = Tk()
root.title("Typing Speed Test")
root.config(padx=100, pady=100, bg=BG_COLOR)

# First row:
# display WPM score
label_wpm = Label(text="WPM:___  ", font=LB_FONT, bg=BG_COLOR, fg=TXT_COLOR)
label_wpm.grid(column=0, row=0)
# countdown timer
label_timer = Label(text=f"Time left: {test_time}s", font=LB_FONT, bg=BG_COLOR, fg=TXT_COLOR)
label_timer.grid(column=1, row=0)
# restart button
button_restart = Button(text="Restart", font=LB_FONT, fg="#E86A33", highlightthickness=0, command=restart)
button_restart.bind("<FocusIn>", click)
button_restart.grid(column=2, row=0, padx=20)

# Second row: display test word
canvas = Canvas(width=400, height=200, bg="white", highlightthickness=0)
word = canvas.create_text(200, 100, text="", font=(FONT, 35, "bold"))
canvas.grid(column=0, row=1, columnspan=4, pady=20)

# Third row: user click on or type here
user_var = StringVar()
user_entry = Entry(root, width=ENTRY_L, bg="white", highlightthickness=0, font=(FONT, 30), fg=TXT_COLOR,
                   textvariable=user_var)
user_entry.insert(END, initial_msg)
user_entry.focus_set()
user_entry.icursor(END)
user_entry.bind("<Button>", click)
user_entry.bind("<Key>", click)
user_entry.grid(column=0, row=2, columnspan=4, pady=20)
user_var.trace("w", check)

# Fetch and display a random word when user run the program.
next_word()
root.mainloop()
