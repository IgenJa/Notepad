import tkinter as tk
from tkinter import filedialog, messagebox

# Alap szövegszerkesztő ablak
root = tk.Tk()
root.geometry("1000x600")
root.title("Szövegszerkesztő - Sorok számozásával")

# A fő szövegdoboz (ahol a szöveg íródik)
text_area = tk.Text(root, wrap=tk.WORD, width=80, height=20, undo=True)  # Engedélyezzük a visszavonás lehetőségét
text_area.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# A sorok számát mutató szegélyes text widget
line_numbers = tk.Text(root, width=4, height=20, bg='lightgray', state=tk.DISABLED)
line_numbers.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Beállítjuk, hogy az oszlopok és sorok rugalmasan változhassanak az ablak méretével
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

# Szöveghez tartozó sorok számának frissítése
def update_line_numbers(event=None):
    lines = text_area.get(1.0, tk.END).splitlines()
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete(1.0, tk.END)

    for i in range(1, len(lines) + 1):
        line_numbers.insert(tk.END, f"{i}\n")

    line_numbers.config(state=tk.DISABLED)

# Fájl mentése
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END))
            messagebox.showinfo("Mentés", "A fájl sikeresen el lett mentve!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült a fájl mentése: {e}")

# Fájl betöltése
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
            update_line_numbers()  # Frissítjük a sorok számát betöltés után
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült a fájl betöltése: {e}")

# Kilépés
def exit_app():
    if messagebox.askokcancel("Kilépés", "Biztosan ki szeretnél lépni?"):
        root.quit()

# Sötét mód váltása
dark_mode = False  # Sötét mód állapota

def toggle_dark_mode():
    global dark_mode
    if dark_mode:
        text_area.config(bg="white", fg="black", insertbackground="black")
        line_numbers.config(bg="lightgray", fg="black")
        dark_mode = False
    else:
        text_area.config(bg="gray20", fg="white", insertbackground="white")
        line_numbers.config(bg="gray30", fg="white")
        dark_mode = True

# Keresési ablak létrehozása
def search_window():
    search_win = tk.Toplevel(root)
    search_win.title("Keresés")
    search_win.geometry("400x120")
    
    # Kereső mező
    search_label = tk.Label(search_win, text="Keresett szöveg:")
    search_label.pack(pady=10)
    
    search_entry = tk.Entry(search_win, width=30)
    search_entry.pack(pady=5)
    
    # Keresés gomb
    def search_text():
        search_term = search_entry.get()
        text_area.tag_remove("highlight", 1.0, tk.END)
        if search_term:
            idx = '1.0'
            while True:
                idx = text_area.search(search_term, idx, nocase=True, stopindex=tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(search_term)}c"
                text_area.tag_add("highlight", idx, end_idx)
                if dark_mode == False:
                    text_area.tag_config("highlight", background="yellow")
                if dark_mode == True:
                    text_area.tag_config("highlight", background="grey")
                idx = end_idx

    search_button = tk.Button(search_win, text="Keresés", command=search_text)
    search_button.pack(pady=10)

    # Keresési ablak bezárásakor a kiemelések eltávolítása
    def on_close():
        text_area.tag_remove("highlight", 1.0, tk.END)
        search_win.destroy()

    # Az ablak bezárásának kezeléséhez hozzárendelünk egy eseményt
    search_win.protocol("WM_DELETE_WINDOW", on_close)
    
    search_win.mainloop()

# Menüsor létrehozása
menu_bar = tk.Menu(root)

# Fájl menü
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Új", command=lambda: text_area.delete(1.0, tk.END))
file_menu.add_command(label="Megnyitás", command=open_file)
file_menu.add_command(label="Mentés", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Kilépés", command=exit_app)

menu_bar.add_cascade(label="Menü", menu=file_menu)

# Sötét mód gomb hozzáadása a menübe
menu_bar.add_command(label="Sötét mód", command=toggle_dark_mode)

# Keresés gomb a menübe
menu_bar.add_command(label="Keresés", command=search_window)

# Beállítjuk a menüsor megjelenítését
root.config(menu=menu_bar)

# Billentyűparancsok hozzáadása
root.bind('<Control-s>', lambda event: save_file())  # Ctrl + S a mentéshez
root.bind('<Control-z>', lambda event: text_area.edit_undo())  # Ctrl + Z a visszavonáshoz
root.bind('<Control-y>', lambda event: text_area.edit_redo())  # Ctrl + Y az újra
root.bind('<Control-f>', lambda event: search_window())  # Ctrl + F a kereséshez

# Frissítjük a sorok számát, amikor a felhasználó gépel
text_area.bind("<KeyRelease>", update_line_numbers)

# Alkalmazás futtatása
root.mainloop()