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
impath = 'C:\\Users\\trach\\Documents\\GitHub\\Desktop-Pet\\Desktop_Pet\\img\\'

x_coordinate, y_coordinate = 0, 0

def get_screen_size(root):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

def set_initial_screen_position(root):
    global x_coordinate, y_coordinate
    screen_width, screen_height = get_screen_size(root)
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    x_coordinate = screen_width - root_width
    y_coordinate = screen_height - root_height

    root.geometry(f"+{x_coordinate}+{y_coordinate}")    

def set_move_screen_position(root, direction=None):
    screen_width, screen_height = get_screen_size(root)
    global x_coordinate, y_coordinate
    if direction == "right" and x_coordinate < screen_width - 400:
        x_coordinate += 10
        root.geometry(f"+{x_coordinate}+{y_coordinate}")
    elif direction == "left" and x_coordinate > 0:
        x_coordinate -= 10
        root.geometry(f"+{x_coordinate}+{y_coordinate}")

def dakota_speak(lines):
    line = lines[random.randint(0,7)]
    dakota_label.config(text=line)
    window.after(3000, hide_message)

def hide_message():
    dakota_label.config(text="")

def dakota_close(event):
    window.destroy()

def update_gif(root, label, gif_path, direction=None):
    global pos
    # Cancel previous animation loop
    if hasattr(label, 'after_id'):
        label.after_cancel(label.after_id)
    
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

    def update(root, direction=None):
        nonlocal frame_index
        label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        label.after_id = label.after(delay, lambda: update(root, direction))

        if direction == "right":
            set_move_screen_position(root, direction)
        elif direction == "left":
            set_move_screen_position(root, direction)

    update(root, direction)

def handle_event(root):
    events_list = os.listdir(impath)

    new_random_event = random.choice(events_list)

    new_event_path = os.path.join(impath, new_random_event)

    if new_random_event == "Dakota-Walking-Left.gif":
        update_gif(root, label, new_event_path, "left")
    elif new_random_event == "Dakota-Walking-Right.gif":
        update_gif(root, label, new_event_path, "right")
    else:
        update_gif(root, label, new_event_path)        

    delay = random.randint(5000, 8000)
    window.after(delay, lambda: handle_event(root))


window = tk.Tk()

window.geometry("500x500")
set_initial_screen_position(window)


initial_image = Image.open(impath + "Dakota-Idle.gif")
initial_image = ImageTk.PhotoImage(initial_image)

label = tk.Label(window, image=initial_image, bg="white", text="", font=("Arial, 12"), bd=0, highlightthickness=0)

label.pack()

label.initial_image = initial_image

dakota_label = tk.Label(window, text="", font=("Arial, 12"), fg="black", bd=0, highlightthickness=0)
dakota_label.pack(pady=20)


window.bind("<Button-1>", lambda event : dakota_speak(dakota_lines_idle))
window.bind("<Button-3>", dakota_close)

window.overrideredirect(True)
window.attributes("-transparentcolor", "white")

handle_event(window)

window.mainloop()