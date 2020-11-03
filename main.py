import os
import mutagen
from mutagen.mp3 import MP3

import pygame
from pygame import mixer

from tkinter import *
from tkinter import filedialog

pygame.mixer.init()

root = Tk()
root.geometry('500x300')
root.title('Music Player')
root.resizable(False, False)

closed = False

default_primary_color = '#000'
default_seconday_color = '#00ff00'
default_third_color = '#404040'

class AudioBox(Frame):

    def __init__(self, master=None):
        super().__init__()

        #Setting up the frame
        self.master = master
        self.config(padx=10, pady=10)

        #Listbox
        self.listbox = Listbox(self, width=35, height=9)

        self.listbox.bind('<<ListboxSelect>>', self.set_song)
        #Scrollbar
        self.scrollbar = Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand = self.scrollbar.set)

        #Song time
        self.timeView = Label(self, text = '---- | ----', bg='#DCDCDC', font=(None, 12))
        self.timeView.pack(side=BOTTOM, fill=X)

        self.listbox.pack(side=LEFT)
        self.scrollbar.config(command=self.listbox.yview)


        #Audio variables
        self.songList = [] # Item = (File name, File path)

    def play_song(self):
        if mixer.music.get_busy() == False:
            if self.listbox.curselection():
                path = self.songList[self.listbox.curselection()[0]][1]
                mixer.music.unload()
                mixer.music.load(path)
                mixer.music.play()
        else:
            mixer.music.stop()

    def set_song(self, event):
        if mixer.music.get_busy(): mixer.music.stop()

    def in_audiobox(self, song):
        for track in self.songList:
            if track[0] == os.path.basename(song):
                for i in range(self.listbox.size()+1):
                    if track[0] == self.listbox.get(i):
                        return True
        return False

    def add_playlist(self):
        playlist = filedialog.askdirectory()
        if playlist:
            files = os.listdir(playlist)

            for file in files:
                if file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.ogg'):
                    noExtension = os.path.splitext(file)[0]
                    self.songList.append([noExtension, os.path.realpath(playlist)+'\\'+file])
                    self.listbox.insert(len(self.listbox.get(0, END)), noExtension)

    def add_song(self):
        song = filedialog.askopenfilename(filetypes = [('Music files', '.wav .mp3 .ogg')])
        noExtension = os.path.splitext(os.path.basename(song))[0]
        if song:    
            self.songList.append([noExtension, song])
            self.listbox.insert(len(self.listbox.get(0, END))+1 ,noExtension)

    def next_song(self):
        if self.listbox.curselection():
            currentIndex = self.listbox.curselection()[0]+1
            self.listbox.selection_clear(0, END)
            
            if currentIndex > len(self.songList)-1:
                currentIndex = 0

            self.listbox.selection_set(currentIndex)
            self.listbox.activate(currentIndex)

            if mixer.music.get_busy() == True:
                mixer.music.stop()
                self.play_song()
        else:
            if len(self.songList)>0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
            

    def prev_song(self):
        if self.listbox.curselection():
            currentIndex = self.listbox.curselection()[0]-1
            self.listbox.selection_clear(0, END)
            
            if currentIndex < 0:
                currentIndex = 0

            self.listbox.selection_set(currentIndex)
            self.listbox.activate(currentIndex)

            if mixer.music.get_busy() == True:
                mixer.music.stop()
                self.play_song()

        else:
            if len(self.songList)>0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
        

class InputPannel(Frame):

    def __init__(self, master=None):
        super().__init__()

        ppnFrame = Frame(self)
        
        self.master = master
        self.config(width=235, height=170)
        self.pack_propagate(0)

        self.playBttn = Button(ppnFrame, text='Play / Stop', font=(None, 10))
        self.prevBttn = Button(ppnFrame, text= 'Prev', font=(None, 11))
        self.nextBttn = Button(ppnFrame, text= 'Next', font=(None, 11))
        self.removeBttn = Button(self, text='Remove Track', font=(None, 9))


        #Slider
        self.volume = Scale(self, from_=100, to=0, command= lambda f:
                            pygame.mixer.music.set_volume(self.volume.get()/100))
        self.volume.set(100)

        #Autoplay
        self.autoplay = IntVar()
        autoplay = Checkbutton(self, variable=self.autoplay, text='Autoplay', anchor='w', font=(None, 11))
        
        self.volume.pack(side=RIGHT, fill=Y)
        ppnFrame.pack(side=BOTTOM, fill=X)
        self.removeBttn.pack(side=BOTTOM, fill=X)
        autoplay.pack(side=BOTTOM, fill=X)

        self.prevBttn.pack(side=LEFT, fill=BOTH, expand=1)
        self.playBttn.pack(side=LEFT, fill=BOTH, expand=1)
        self.nextBttn.pack(side=LEFT, fill=BOTH, expand=1)
        

#Customization

#Audio Storage
audioBox = AudioBox(master = root)
audioBox.grid(row=0, column=0)

inputPannel = InputPannel(master=root)
inputPannel.grid(row=0, column=1, sticky='n', pady=10)
inputPannel.playBttn.config(command=audioBox.play_song)

inputPannel.nextBttn.config(command=audioBox.next_song)
inputPannel.prevBttn.config(command=audioBox.prev_song)

#Menubar
menuBar = Menu(root)
root.config(menu=menuBar)

def clear():
    pygame.mixer.music.stop()
    audioBox.listbox.select_clear(0,END);
    audioBox.listbox.delete(0, END);
    audioBox.songList = []

def removeTrack():
    pygame.mixer.music.stop()
    currentIndex = audioBox.listbox.curselection()[0]
    audioBox.listbox.delete(currentIndex)
    audioBox.songList.pop(currentIndex)


fileTab = Menu(menuBar, tearoff=0)
fileTab.add_command(label='Add Track', command=audioBox.add_song)
fileTab.add_command(label = 'Add Playlist', command=audioBox.add_playlist)

editTab= Menu(menuBar, tearoff=0)
editTab.add_command(label='Clear Audiobox', command=clear)

inputPannel.removeBttn.config(command=removeTrack)
menuBar.add_cascade(label='File', menu=fileTab)
menuBar.add_cascade(label='Edit', menu=editTab)

#Making the credits
Label(root, text='Made by Onuelito').grid(sticky='s')
Label(root, text='Powered by Tkinter, Pygame and OS').grid(sticky='s')

def update():
    if audioBox.listbox.curselection():
        song = audioBox.songList[audioBox.listbox.curselection()[0]][1]
        startTime = '00:00'
        audio = MP3(song)

        #Start Time
        if mixer.music.get_busy():
            currentTime = mixer.music.get_pos()/1000
            
            minutes = int(currentTime//60)
            seconds = int(currentTime%60)

            if minutes < 10: minutes = '0'+str(minutes)
            if seconds < 10: seconds = '0'+str(seconds)

            startTime = str(minutes)+':'+str(seconds)

            if round(audio.info.length/currentTime, 2) <=1 and inputPannel.autoplay.get() == 1:
                audioBox.next_song()
        
        #End time
        minutes = int(audio.info.length//60)
        seconds = int(audio.info.length%60)

        if minutes < 10: minutes = '0'+str(minutes)
        if seconds < 10: seconds = '0'+str(seconds)

        minutes = str(minutes)
        seconds = str(seconds)

        audioBox.timeView.config(text =startTime+ ' | '+minutes+':'+seconds)
        
    root.after(250, update)

root.after(250, update)

root.bind('<Destroy>', lambda f: pygame.mixer.music.stop())
root.mainloop()
