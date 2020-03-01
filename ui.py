import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as sctxt
from preprocessing import artists, genres


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("GUI")
        self.pack(fill='both', expand='yes')
        self.create_tabs()
        self.create_lyrics_textarea()

    def create_lyrics_textarea(self):
        self.gen_lyrics_textarea = sctxt.ScrolledText(
            master=self.master,
            wrap=tk.WORD,
            width=20,
            height=10
        )
        self.gen_lyrics_textarea.pack(padx=10, pady=10, fill='both', expand='yes', side=tk.RIGHT)

    def create_tabs(self):
        nb = ttk.Notebook(self.master)
        self.artists_tab = ttk.Frame(nb)
        nb.add(self.artists_tab, text='Artists')
        self.genres_tab = ttk.Frame(nb)
        nb.add(self.genres_tab, text='Genres')
        self.fill_tabs()
        nb.pack(padx=10, pady=10, fill='both', expand='yes', side=tk.RIGHT)

    def fill_tabs(self):
        artists_cb = ttk.Combobox(self.artists_tab, values=artists, state='readonly')
        genres_cb = ttk.Combobox(self.genres_tab, values=list(genres.keys()), state='readonly')
        artists_cb.pack(padx=10, pady=10, fill='both', expand='no')
        genres_cb.pack(padx=10, pady=10, fill='both', expand='no')
        artists_cb.current(0)
        genres_cb.current(0)

    def fill_textarea(self, text):
        self.scrolled_text.insert(tk.INSERT, text)


root = tk.Tk()
root.geometry("600x900")
app = Window(root)
root.mainloop()
