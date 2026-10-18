
import tkinter as tk
import math
import random
import webbrowser
from urllib.parse import quote

WIDTH = 1100
HEIGHT = 700

root = tk.Tk()
root.title("Interactive Solar System")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#050510")

canvas = tk.Canvas(
    root, bg="#050510",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

center_x = 400
center_y = 360

# Stars
for _ in range(220):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.choice([1, 1, 2])
    canvas.create_oval(
        x, y, x + size, y + size,
        fill="white", outline=""
    )

canvas.create_text(
    center_x, 30,
    text="INTERACTIVE SOLAR SYSTEM",
    fill="white",
    font=("Arial", 19, "bold")
)

# Sun
canvas.create_oval(
    center_x - 28, center_y - 28,
    center_x + 28, center_y + 28,
    fill="#FFD700", outline="#FF9900", width=3
)
canvas.create_text(
    center_x, center_y + 42,
    text="SUN", fill="#FFD700",
    font=("Arial", 10, "bold")
)

# Name, orbit, size, color, animation speed, diameter, orbital period
planets = [
    ("Mercury", 60, 5, "#B8B8B8", 0.055, 4879, 88),
    ("Venus", 95, 8, "#E6B566", 0.035, 12104, 225),
    ("Earth", 130, 9, "#3399FF", 0.025, 12742, 365),
    ("Mars", 165, 7, "#FF5533", 0.020, 6779, 687),
    ("Jupiter", 205, 15, "#D8A078", 0.012, 139820, 4333),
    ("Saturn", 250, 13, "#E8D29B", 0.009, 116460, 10759),
]

planet_objects = []

for name, orbit, size, color, speed, diameter, period in planets:
    canvas.create_oval(
        center_x - orbit, center_y - orbit,
        center_x + orbit, center_y + orbit,
        outline="#353550"
    )

for name, orbit, size, color, speed, diameter, period in planets:
    planet = canvas.create_oval(
        0, 0, size * 2, size * 2,
        fill=color, outline="white", width=1
    )
    label = canvas.create_text(
        0, 0, text=name, fill="white",
        font=("Arial", 9)
    )

    planet_objects.append({
        "name": name,
        "orbit": orbit,
        "size": size,
        "color": color,
        "speed": speed,
        "diameter": diameter,
        "period": period,
        "angle": random.uniform(0, math.pi * 2),
        "planet": planet,
        "label": label
    })

# Information panel
panel = tk.Frame(root, bg="#15152B", padx=16, pady=14)
panel.place(x=750, y=155, width=320, height=410)

title = tk.Label(
    panel, text="PLANET INFO",
    bg="#15152B", fg="#FFD700",
    font=("Arial", 16, "bold")
)
title.pack(anchor="w", pady=(0, 14))

info = tk.Label(
    panel,
    text="Click any planet to explore it!",
    bg="#15152B", fg="white",
    font=("Arial", 11),
    justify="left",
    wraplength=280
)
info.pack(anchor="w")

selected_planet = None

def open_wikipedia():
    if selected_planet is None:
        return

    name = selected_planet["name"]
    url = "https://en.wikipedia.org/wiki/" + quote(name)

    try:
        success = webbrowser.open_new_tab(url)
        if not success:
            status.config(
                text="Browser did not open. Try the URL below.",
                fg="#FFCC66"
            )
            url_label.config(text=url)
    except Exception:
        status.config(
            text="Could not open browser. Copy the URL below.",
            fg="#FFCC66"
        )
        url_label.config(text=url)

# Clickable link
wiki_link = tk.Label(
    panel,
    text="Wanna know more? Click here!",
    bg="#15152B", fg="#55CCFF",
    cursor="hand2",
    font=("Arial", 10, "underline"),
    wraplength=280
)
wiki_link.pack(anchor="w", pady=(18, 0))
wiki_link.bind("<Button-1>", lambda event: open_wikipedia())

status = tk.Label(
    panel, text="",
    bg="#15152B", fg="#AAAAAA",
    font=("Arial", 9),
    wraplength=280,
    justify="left"
)
status.pack(anchor="w", pady=(8, 0))

url_label = tk.Label(
    panel, text="",
    bg="#15152B", fg="#55CCFF",
    font=("Arial", 8),
    wraplength=280,
    justify="left"
)
url_label.pack(anchor="w")

def show_info(p):
    global selected_planet
    selected_planet = p

    title.config(text=p["name"].upper(), fg=p["color"])

    info.config(
        text=(
            f"Orbital speed:\n"
            f"{p['speed']:.3f} rad/frame (simulation)\n\n"
            f"Distance from Sun:\n"
            f"{p['orbit']} pixels (simulation)\n\n"
            f"Diameter:\n"
            f"{p['diameter']:,} km\n\n"
            f"Orbital period:\n"
            f"{p['period']:,} Earth days\n\n"
            f"Formation age:\n"
            f"Approximately 4.5 billion years ago"
        )
    )

    status.config(text="Planet selected!", fg="#88FFAA")
    url_label.config(text="")
    
    # Highlight the selected planet
    for other in planet_objects:
        canvas.itemconfig(other["planet"], width=1)
    canvas.itemconfig(p["planet"], width=3)

# Click a planet OR its name to select it
for p in planet_objects:
    for item in (p["planet"], p["label"]):
        canvas.tag_bind(
            item, "<Button-1>",
            lambda event, planet=p: show_info(planet)
        )
        canvas.tag_bind(
            item, "<Enter>",
            lambda event, planet=p: title.config(
                text=planet["name"].upper(),
                fg=planet["color"]
            )
        )

running = True

def animate():
    if not running:
        return

    for p in planet_objects:
        p["angle"] += p["speed"]

        x = center_x + math.cos(p["angle"]) * p["orbit"]
        y = center_y + math.sin(p["angle"]) * p["orbit"]
        s = p["size"]

        canvas.coords(
            p["planet"],
            x - s, y - s, x + s, y + s
        )
        canvas.coords(p["label"], x, y + s + 12)

    root.after(20, animate)

def toggle_animation():
    global running
    running = not running
    button.config(text="Resume" if not running else "Pause")
    if running:
        animate()

button = tk.Button(
    root, text="Pause",
    command=toggle_animation,
    bg="#242447", fg="white",
    activebackground="#444477",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief="flat", padx=18, pady=6
)
button.place(x=20, y=20)

animate()
root.mainloop()
