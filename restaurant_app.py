import tkinter as tk
from tkinter import messagebox
import difflib
import re

# Menu
menu = {
    'pizza': 60,
    'pasta': 40,
    'burger': 60,
    'salad': 70,
    'coffee': 80,
}

# Normalize menu
menu = {item.lower(): price for item, price in menu.items()}
order_total = 0

# Find closest item
def correct_item_name(item_name):
    item_name = item_name.lower()
    matches = difflib.get_close_matches(item_name, menu.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None

# Process order
def process_order(order_input):
    global order_total
    order_input = order_input.lower().replace("and", " ").replace(",", " ")
    pattern = r'(\d+)?\s*([a-zA-Z]+)\s*(\d+)?'
    matches = re.findall(pattern, order_input)

    added_items = []
    for qty1, item_name, qty2 in matches:
        if not item_name.strip():
            continue
        quantity = int(qty1 or qty2 or 1)
        item = correct_item_name(item_name.strip())
        if item:
            cost = quantity * menu[item]
            order_total += cost
            added_items.append(f"{quantity} x {item.capitalize()} = ₹{cost}")
        else:
            added_items.append(f"❌ '{item_name.strip()}' not on menu")

    return "\n".join(added_items)

# Button click
def add_order():
    user_input = entry.get()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter your order")
        return
    result = process_order(user_input)
    text_box.insert(tk.END, result + "\n")
    entry.delete(0, tk.END)

def show_bill():
    global order_total
    bill_label.config(text=f"🧾 Your total bill is ₹{order_total}\n⏳ Ready in 5 minutes\n🙏 Thank you!")
    order_total = 0
    text_box.delete(1.0, tk.END)

# GUI Window
root = tk.Tk()
root.title("🍽️ Zia Restaurant Ordering App 🍽️")
root.geometry("420x550")
root.configure(bg="lightyellow")  # 🌟 Background set to light yellow

# Heading
tk.Label(root, text="📋 Menu", font=("Arial", 14, "bold"), bg="lightyellow").pack(pady=5)

for item, price in menu.items():
    tk.Label(root, text=f"{item.capitalize()}: ₹{price}", bg="lightyellow", fg="black").pack()

# Input field
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=10)

tk.Button(root, text="➕ Add Order", command=add_order, bg="gold", fg="black", font=("Arial", 11, "bold")).pack(pady=5)

# Text area
text_box = tk.Text(root, height=10, width=40, bg="lemonchiffon", fg="black")
text_box.pack(pady=10)

# Bill button
tk.Button(root, text="🧾 Show Bill", command=show_bill, bg="orange", fg="black", font=("Arial", 11, "bold")).pack(pady=10)

# Bill display
bill_label = tk.Label(root, text="", font=("Arial", 12), bg="lightyellow", fg="black")
bill_label.pack(pady=10)

root.mainloop()
