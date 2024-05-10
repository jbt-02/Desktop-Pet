import tkinter as tk
from PIL import Image, ImageTk
import random
import os

dakota_lines_idle = {
    0: "Herro, Is Dakotaa",
    1: "Im booaaed, can we wAyyy",
    2: "Wheres Mommy??",
    3: "*Side eye*",
    4: "Im just a pwincess gwrl",
    5: "I wove you Mia",
    6: "I tak showas",
    7: "Can I hav some fud?"
}
impath = 'C:\\Users\\Mia Aragon\\Desktop\\Desktop_Pet\\img\\'


def dakota_speak(lines):
    line = lines[random.randint(0,7)]
    dakota_label.config(text=line)
    window.after(3000, hide_message)

def hide_message():
    dakota_label.config(text="")

def dakota_close(event):
    window.destroy()

def update_gif(label, gif_path):
    # Cancel previous animation loop
    label.after_cancel(label.after_idle)
    
    gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass
    except Exception as e:
        print("Error loading frames:", e)
    
    delay_per_frame = gif.info.get('duration', 100)
    buffer_time = 50  # Additional buffer time in milliseconds
    delay = delay_per_frame + buffer_time  # Total delay including buffer time

    frame_index = 0

    def update():
        nonlocal frame_index
        label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        label.after_id = label.after(delay, update)

    update()

def handle_event():
    events_list = os.listdir(impath)

    new_random_event = random.choice(events_list)

    new_event_path = os.path.join(impath, new_random_event)

    update_gif(label, new_event_path)

    delay = random.randint(10000, 15000)
    window.after(delay, handle_event)


window = tk.Tk()

initial_image = Image.open(impath + "Dakota-Idle.gif")
initial_image = ImageTk.PhotoImage(initial_image)

label = tk.Label(window, image=initial_image, bg="white", text="", font=("Arial, 12"), bd=0, highlightthickness=0)

label.pack()

label.initial_image = initial_image

dakota_label = tk.Label(window, text="", font=("Arial, 12"), bg="grey", fg="white", bd=0, highlightthickness=0)
dakota_label.pack(pady=20)


window.bind("<Button-1>", lambda event : dakota_speak(dakota_lines_idle))
window.bind("<Button-3>", dakota_close)

# Set window attributes to remove decorations
window.overrideredirect(True)
window.attributes("-transparentcolor", "white")
# Loop the program
#window.after(1, update, cycle, check, event_number, x)

handle_event()

window.mainloop()
