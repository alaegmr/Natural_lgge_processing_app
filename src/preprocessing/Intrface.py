import tkinter as tk
from tkinter import messagebox
import json
import os


def load_word_transitions(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get("matrix", [])
    except Exception:
        return []


def predict_next_word(input_word, word_transitions):
    predictions = []
    for entry in word_transitions:
        if entry["word"].startswith(input_word):
            for trans in entry["transitions"]:
                predictions.append((trans["word"], trans["probability"]))
    predictions.sort(key=lambda x: x[1], reverse=True)
    if predictions:
        max_prob = predictions[0][1]
        return [p[0] for p in predictions if p[1] == max_prob]
    return []


def on_key_release(event=None):
    user_input = word_input.get().strip()
    suggestion_box.delete(0, tk.END)
    if user_input:
        predictions = predict_next_word(user_input, word_transitions)
        for word in predictions[:5]:
            suggestion_box.insert(tk.END, word)


def on_suggestion_click(event):
    if suggestion_box.curselection():
        selected = suggestion_box.get(suggestion_box.curselection())
        word_input.delete(0, tk.END)
        word_input.insert(0, selected)
        suggestion_box.delete(0, tk.END)


def create_gui():
    global word_input, suggestion_box

    window = tk.Tk()
    window.title("🔮 الأمثال و الحكم باللغة العربية")
    window.geometry("800x500")
    window.configure(bg="#FDF8EE")

    # Conteneur principal qui s'étire avec la fenêtre
    container = tk.Frame(window, bg="#FFFFFF", bd=2, relief="groove")
    container.pack(expand=True, fill="both", padx=20, pady=20)

    # Titre
    tk.Label(container, text="🔮 الأمثال و الحكم باللغة العربية", font=("Cairo", 20, "bold"),
             bg="#FFFFFF", fg="#5A4E3C").pack(pady=(10, 20))

    # Barre de recherche
    search_frame = tk.Frame(container, bg="#FFFFFF")
    search_frame.pack(pady=10, anchor="e", padx=30)

    word_input = tk.Entry(search_frame, font=("Cairo", 16), width=30, justify="right",
                          relief="flat", bd=2, highlightthickness=2,
                          highlightbackground="#e3c291", highlightcolor="#e3c291")
    word_input.pack(side=tk.RIGHT, padx=10)
    word_input.focus()
    word_input.bind("<KeyRelease>", on_key_release)

    tk.Label(search_frame, text="🔎 أدخل كلمة:", font=("Cairo", 14), bg="#FFFFFF", fg="#333").pack(side=tk.RIGHT)

    # Liste des suggestions
    suggestion_box = tk.Listbox(container, font=("Cairo", 14), bg="#FFFDF6", fg="#000000",
                                activestyle="none", justify="right", relief="flat", height=5,
                                highlightthickness=1, highlightbackground="#e3c291")
    suggestion_box.pack(anchor='e', fill='x', padx=30, pady=(10, 20))
    suggestion_box.bind("<<ListboxSelect>>", on_suggestion_click)

    window.mainloop()


if __name__ == "__main__":
    word_transitions = load_word_transitions("../../data/processed/word_matrix.json")
    create_gui()
