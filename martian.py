from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *
import pafy
from youtube_search import YoutubeSearch
import json
#from pydub import AudioSegment as convert
import os
import moviepy.editor as mp
import pygame

class Gui:
    def __init__(self):
        self.tk = Tk()
        self.directory = None
        if not os.path.exists("cache.txt"):
            with open("cache.txt", "w") as fw:
                fw.write("None")
                fw.close()
                self.directory = None
        else:
            with open("cache.txt", "r") as fr:
                self.directory = fr.read()
        self.gui_scale = "640x420"
        self.gui_title = "Martian: Visual YouTube Music Media Player"
        pass
    
    def add_directory(self):
        popup_find_dir = askdirectory()
        if popup_find_dir:
            self.directory = popup_find_dir + "/"
            with open("cache.txt", "w") as fw:
                 fw.write(self.directory)
            showinfo("Config", "Directory to: " + self.directory)
        else:
            showerror("Alert", "Directory Null")
        pass
    
    def download_to(self, link, title):
        a = pafy.new("https://www.youtube.com/" + link)
        b = a.getbest()
        c = a.streams
        
        if self.directory:
            print("---iniciando\n")
            name = self.directory + title + "." + str(c[0].extension)
            d = b.download(filepath = name)
            print("orgl: " + name)
            if os.path.exists(name):
                e = mp.VideoFileClip(name)
                print("---transformando\n")
                name = self.directory + title + "." + "mp3"
                e.audio.write_audiofile(name)
                print("convertido com sucesso\n")
                showinfo("Opa", "Video Converted Sucessfull!")
                self.update_list()
        else:
            showerror("Alert", "Escolher um diretório para os audios!!")
        pass
    
    def show_videos(self, tags):
        tk = Tk()
        tk.geometry(self.gui_scale)
        tk.title("Martian-native: Show Search Results")
        r = json.loads(YoutubeSearch(tags, max_results = 15).to_json())
        _int_pos = 1
        for i in r['videos']:
            _int_pos += 1
            l = Label(tk)
            l['text'] = i['title'][:50] + "..."
            l.grid(row = _int_pos, column = 1)
            b = Button(tk)
            b['text'] = 'Add this'
            b['command'] = lambda i = i: self.download_to(i['link'], i['title'][:10])
            b.grid(row = _int_pos, column = 2)
        pass
    
    def playnow(self):
        if self.directory:
            if self.files.curselection():
                _id = self.files.curselection()[0]
                name = self.directory + self.files.get(_id)
                print("tocando: " + name)
                pygame.mixer.init()
                pygame.mixer.music.load(name)
                pygame.mixer.music.play()
                
                stop = Button(self.tk)
                stop['text'] = 'Stop'
                stop['command'] = lambda: pygame.mixer.music.stop()
                stop.grid(row = 2, column = 3)
        pass
    
    def stopnow(self):
        pass
    
    def main(self):
        search = Entry(self.tk)
        search.focus_set()
        search.grid(row = 1, column = 1)
        
        show = Button(self.tk)
        show['text'] = 'Show'
        show['command'] = lambda: self.show_videos(search.get())
        show.grid(row = 1, column = 2)
        
        setdir = Button(self.tk)
        setdir['text'] = 'Directory'
        setdir['command'] = lambda: self.add_directory()
        setdir.grid(row = 1, column = 3)
        
        self.files = Listbox(self.tk)
        self.files.grid(row = 2, column = 1)
        
        play = Button(self.tk)
        play['text'] = 'Play MP3'
        play['command'] = lambda: self.playnow()
        play.grid(row = 2, column = 2)
        pass
    
    def update_list(self):
        if self.directory:
            for i in os.listdir(self.directory):
                if i.endswith(".mp3"):
                    self.files.delete(0, END)
                    self.files.insert(END, i)
        pass
    
    def ready(self):
        #self.add_directory()
        self.main()
        self.update_list()
        self.configure_gui()
        pass
    
    def configure_gui(self):
        self.tk.geometry(self.gui_scale)
        self.tk.title(self.gui_title)
        self.tk.mainloop()
        pass

gui = Gui()
gui.ready()