import tkinter as tk
import math
from tkinter import ttk
from tkinter import scrolledtext as sctxt
from preprocessing import artists, genres
from utils import default_params


class LyricsGUI(tk.Frame):
    def __init__(self, master, generation):
        tk.Frame.__init__(self, master)
        self.master = master
        self.generation = generation
        self.master.title("Lyrics Generation")
        self.create_settings_frame()
        self.create_lyrics_textarea()

    def create_lyrics_textarea(self):
        frame = tk.Frame(self.master)
        label = tk.Label(frame, text='Generated bars')
        label.pack(padx=10, pady=5, fill='both', expand='no')
        self.gen_lyrics_textarea = sctxt.ScrolledText(master=frame, wrap=tk.WORD)
        self.gen_lyrics_textarea.pack(padx=5, pady=10, fill='both', expand='yes')
        frame.pack(padx=10, pady=5, fill='both', expand='yes', side=tk.RIGHT)

    def create_tabs(self, parent):
        self.nb = ttk.Notebook(parent)
        artists_tab = ttk.Frame(self.nb)
        self.nb.add(artists_tab, text='Artists')
        genres_tab = ttk.Frame(self.nb)
        self.nb.add(genres_tab, text='Genres')
        self.fill_tabs(artists_tab, genres_tab)
        self.nb.pack(padx=10, pady=5, fill='both', expand='yes')

    def fill_tabs(self, artists_tab, genres_tab):
        self.artists_cb = ttk.Combobox(artists_tab, values=artists, state='readonly')
        self.genres_cb = ttk.Combobox(genres_tab, values=list(genres.keys()), state='readonly')
        self.artists_cb.bind('<<ComboboxSelected>>', self.clear_params)
        self.genres_cb.bind('<<ComboboxSelected>>', self.clear_params)
        self.artists_cb.pack(padx=10, pady=5, fill='both', expand='no')
        self.genres_cb.pack(padx=10, pady=5, fill='both', expand='no')
        self.artists_cb.current(0)
        self.genres_cb.current(0)

        shuffle_frame = tk.Frame(artists_tab)
        shuffle_label = tk.Label(shuffle_frame, text='Shuffle with')
        self.shuffle_value = tk.BooleanVar()
        self.shuffle_value.set(False)
        shuffle_check = tk.Checkbutton(shuffle_frame, var=self.shuffle_value)
        self.add_artists_cb = ttk.Combobox(shuffle_frame, values=artists, state='readonly')
        self.add_artists_cb.bind('<<ComboboxSelected>>', self.clear_params)
        shuffle_check.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        shuffle_label.pack(padx=0, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.add_artists_cb.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        shuffle_frame.pack(padx=10, pady=5, fill='both', expand='no')

    def create_parameters_frame(self, parent):
        params_frame = tk.Frame(parent)
        lines_frame = tk.Frame(params_frame)
        lines_label = tk.Label(lines_frame, text='Num of lines:')
        self.num_lines = tk.Entry(lines_frame)
        lines_label.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.num_lines.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        nn_frame = tk.Frame(params_frame)
        nn_label = tk.Label(nn_frame, text='NN depth:')
        self.nn_depth = tk.Entry(nn_frame)
        nn_label.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.nn_depth.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        overlap_frame = tk.Frame(params_frame)
        overlap_label = tk.Label(overlap_frame, text='Max. overlap:')
        self.max_overlap = tk.Entry(overlap_frame)
        overlap_label.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.max_overlap.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        syl_frame = tk.Frame(params_frame)
        syl_label = tk.Label(syl_frame, text='Max. syllables:')
        self.max_syllables = tk.Entry(syl_frame)
        syl_label.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.max_syllables.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)

        default_frame = tk.Frame(params_frame)
        default_label = tk.Label(default_frame, text='Use default parameters')
        self.def_value = tk.BooleanVar()
        self.def_value.set(False)
        default_check = tk.Checkbutton(default_frame, var=self.def_value, command=self.on_check_default)
        default_check.bind()
        default_check.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        default_label.pack(padx=0, pady=5, fill='both', expand='no', side=tk.LEFT)
        default_frame.pack(padx=10, pady=5, fill='both', expand='no')

        for f in [lines_frame, nn_frame, overlap_frame, syl_frame]:
            f.pack(padx=10, pady=5, fill='both', expand='no')
        params_frame.pack(padx=10, pady=10, fill='both', expand='yes')

    def create_settings_frame(self):
        set_frame = tk.Frame(self.master)
        self.create_tabs(set_frame)
        self.create_parameters_frame(set_frame)
        self.create_gen_button(set_frame)
        self.create_eval_frame(set_frame)
        set_frame.pack(padx=5, pady=5, fill='both', expand='yes', side=tk.RIGHT)

    def create_gen_button(self, parent):
        generate_button = tk.Button(parent, text='Generonimo!')
        generate_button.bind("<Button-1>", self.on_click_generate)
        generate_button.pack(padx=10, pady=5, fill='both', expand='no')

    def create_eval_frame(self, parent):
        eval_frame = tk.Frame(parent)
        self.eval_result = tk.Entry(eval_frame)
        eval_button = tk.Button(eval_frame, text='Evaluate')
        eval_button.bind("<Button-1>", self.on_click_evaluate)
        eval_button.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        self.eval_result.pack(padx=10, pady=5, fill='both', expand='no', side=tk.LEFT)
        eval_frame.pack(padx=10, pady=5, fill='both', expand='no')

    def on_click_generate(self, event):
        self.gen_lyrics_textarea.delete(1.0, tk.END)
        self.eval_result.delete(0, tk.END)
        ident = self.get_current_identifier()
        params = self.check_params()
        if params:
            lyrics = self.generation(ident, params)
            if lyrics:
                self.gen_lyrics_textarea.insert(1.0, lyrics)
            else:
                self.gen_lyrics_textarea.insert(1.0, 'Generation failed :(')

    def check_params(self):
        if not self.num_lines.get() or not self.nn_depth.get() or\
           not self.max_syllables.get() or not self.max_overlap.get():
            print('please fill all parameters')  # todo replace with an alert
            return None
        try:
            params = {'depth': int(self.nn_depth.get()),
                      'num_lines': int(self.num_lines.get()),
                      'max_syllables': float(self.max_syllables.get()),
                      'max_overlap': float(self.max_overlap.get())}
        except ValueError:
            print('please check format (int or float only)')  # todo replace with an alert
            return None
        return params

    def on_check_default(self):
        if self.def_value.get():
            self.set_default_params()
        else:
            self.clear_params()

    def on_click_evaluate(self, event):
        self.eval_result.delete(0, tk.END)
        # res = get_eval_res()
        res = 'hmm %'
        self.eval_result.insert(0, res)

    def get_current_identifier(self):
        tab = self.nb.tab(self.nb.select(), "text")
        if tab == 'Artists':
            primary_artist = self.artists_cb.get()
            if self.shuffle_value.get():
                additional_artist = self.add_artists_cb.get()
                if not additional_artist:
                    print('Choose second artist!')
                elif primary_artist == additional_artist:
                    print('Warning: shuffling with the same artist, ignored.')
                    return [primary_artist]
                else:
                    return [primary_artist, additional_artist]
            else:
                return [primary_artist]
        else:
            return [self.genres_cb.get()]

    def set_default_params(self):
        ident = self.get_current_identifier()
        if len(ident) > 1:
            max_syllables = math.ceil((default_params['syl_overlap'][ident[0]][0] +
                                       default_params['syl_overlap'][ident[1]][0]) / 2)
            max_overlap = math.ceil((default_params['syl_overlap'][ident[0]][1] +
                                     default_params['syl_overlap'][ident[1]][1]) / 2 * 10) / 10
        else:
            max_syllables = default_params['syl_overlap'][ident[0]][0]
            max_overlap = default_params['syl_overlap'][ident[0]][1]
        self.num_lines.insert(0, default_params['num_lines'])
        self.nn_depth.insert(0, default_params['depth'])
        self.max_overlap.insert(0, max_overlap)
        self.max_syllables.insert(0, max_syllables)

    def clear_params(self, event=None):
        if self.def_value.get():
            self.def_value.set(False)
        self.num_lines.delete(0, tk.END)
        self.nn_depth.delete(0, tk.END)
        self.max_overlap.delete(0, tk.END)
        self.max_syllables.delete(0, tk.END)


def open_gui(generation_method):
    root = tk.Tk()
    root.geometry("800x600")
    app = LyricsGUI(root, generation_method)
    root.mainloop()
