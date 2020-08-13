import os
import time                                   #for changing current working directory to user selected directory, selecting files in directory
from tkinter.filedialog import askdirectory #ask user for directory
import pygame                               #audio playback
from mutagen.id3 import ID3                 #import song title from metadata
from mutagen.mp3 import MP3                 #import song duration in seconds
from tkinter import *                       #all GUI components

pygame.init()
pygame.mixer.init()                         #initialize pygame


class App:
    def __init__(self, root):

        self.root = root                    #initializing main window and configuration
        self.root.title("MP3 Player")
        self.root.configure(bg='#002B36')
        self.root.wm_iconbitmap('icon.ico')
        self.root.minsize(650, 550)

        self.songs_list = []                #required arrays/lists, variables and string variables in the program
        self.names = []
        self.index = 0
        self.v = StringVar()
        self.duration = 0
        self.paused = False
        self.nextt = pygame.USEREVENT + 1   #initializing a user created event, that'll be called when a song ends

        self.playlisticon = PhotoImage(file="Playlist.png")
        self.playicon = PhotoImage(file="Play.png")
        self.pauseicon = PhotoImage(file='Pause.png')
        self.nexticon = PhotoImage(file="Next.png")
        self.previcon = PhotoImage(file="Previous.png")

        self.label = Label(self.root, bg='#002B36', fg='SkyBlue2', font=("Arial", 10), text='Playlist')
        self.label.pack()

        self.listbox = Listbox(self.root, bg='#002B36', fg='SkyBlue2', highlightbackground='SkyBlue2',
                               highlightthickness=1, font=("Arial", 10), width=80, height=15, selectbackground='#002B36',
                               selectmode='SINGLE')
        self.listbox.pack(pady=4)

        self.buttonframe = Frame(self.root, bg='#002B36')
        self.buttonframe.pack()

        self.playlistbutton = Button(self.buttonframe, text='Add to Playlist', activebackground='#002B36',
                                     image=self.playlisticon, border=0, bg='#002B36', fg='white',
                                     command=self.directorychooser)
        self.playlistbutton.pack(pady=2)

        self.prevbutton = Button(self.buttonframe, text='Previous', activebackground='#002B36', image=self.previcon,
                                 border=0, bg='#002B36', fg='white', command=self.prevsong)
        self.prevbutton.pack(pady=2, padx=2, side=LEFT)

        self.togglebutton = Button(self.buttonframe, text='Pause/Play', activebackground='#002B36', image=self.pauseicon,
                                   border=0, bg='#002B36', width=40, height=46, fg='white', command=self.toggle)
        self.togglebutton.pack(pady=2, padx=2, side=LEFT)

        self.nextbutton = Button(self.buttonframe, text='Next', activebackground='#002B36', image=self.nexticon,
                                 border=0, bg='#002B36', fg='white', command=self.nextsong)
        self.nextbutton.pack(pady=2, padx=2, side=LEFT)

        self.durationscale = Scale(self.root, bg='#002B36', fg='SkyBlue2', length=400, highlightbackground='#002B36',
                                   activebackground='black', highlightthickness=1, sliderrelief=FLAT,
                                   troughcolor='SkyBlue2', bd=0, orient=HORIZONTAL, from_=0, to=100, sliderlength=10,
                                   width=5)
        self.durationscale.pack(padx=4, pady=4)

        self.bottomframe = Frame(self.root, bg='#002B36')
        self.bottomframe.pack(side=BOTTOM)

        self.playinglabel = Label(self.bottomframe, bg='#002B36', fg='SkyBlue2', font=("Arial", 10), text="Now Playing: ")
        self.playinglabel.pack(side=LEFT, pady=2)

        self.songlabel = Label(self.bottomframe, bg='#002B36', font=("Arial", 10), fg='SkyBlue2', width=45,
                               textvariable=self.v)
        self.songlabel.pack(side=LEFT, pady=2)

        self.volumescale = Scale(self.bottomframe, bg='#002B36', fg='SkyBlue2', length=100, resolution=2,
                                 activebackground='#002B36', font=("Arial", 10), label='Volume', highlightthickness=0,
                                 troughcolor='SkyBlue2', bd=0, orient=HORIZONTAL, from_=0, to=100, width=10,
                                 sliderlength=20, sliderrelief=GROOVE, command=self.volume)
        self.volumescale.pack(side=LEFT, pady=4)
        self.volumescale.set(80)

        self.root.bind("<p>", self.prevsong)   #functions bound to keyboard and mouse buttons
        self.root.bind("<n>", self.nextsong)
        self.root.bind("<Right>", self.forward)
        self.root.bind("<Left>", self.backward)
        self.root.bind("<Control-Right>", self.forward2)
        self.root.bind("<Control-Left>", self.backward2)
        self.root.bind("<space>", self.toggle)
        self.root.bind("<Up>", self.incvol)
        self.root.bind("<Down>", self.decvol)
        self.durationscale.bind("<ButtonRelease-1>", self.forback)

    def directorychooser(self, _=None):
        directory = askdirectory()           #ask user for directory
        os.chdir(directory)                  #change current working directory to user selected directory
        for files in os.listdir(directory):  #os.listdir returns list of files in the current wrokin directory
            if files.endswith(".mp3"):
                realdir = os.path.realpath(files) #returns canonical form of directory plus file name and format
                audio = ID3(realdir)              #save metadata in audio
                self.names.append(audio['TIT2'].text[0])       #append title of song to names list
                self.songs_list.append(files)                  #append mp3 file to songs_list list

        self.names.reverse()
        for items in self.names:                 #insert elements of names list in listbox
            self.listbox.insert(0, items)

        self.names.reverse()
        self.play()
        return 'break'

    def updatelabel(self, _=None):
        self.v.set(self.names[self.index])     #import title to string variable v at current index

    def nextsong(self):
        length = len(self.songs_list)
        if self.index < length - 1:
            self.index += 1
            self.play()

        elif self.index == length - 1:
            self.index = 0
            self.play()

    def prevsong(self, _=None):
        if self.index > 0:
            self.index -= 1
            self.play()

        elif self.index == 0:
            self.index = len(self.songs_list) - 1
            self.play()

    def toggle(self, _=None):                 #pause or unpause the current playing song depending on the bool variable paused
        if self.paused:
            pygame.mixer.music.unpause()
            self.togglebutton.configure(image=self.pauseicon)
            self.paused = False
            self.progress()
        elif not self.paused:
            pygame.mixer.music.pause()
            self.togglebutton.configure(image=self.playicon)
            self.paused = True

    def play(self):
        audio = MP3(self.songs_list[self.index])        #get duration of mp3 file at current index
        self.duration = int(audio.info.length)
        pygame.mixer.music.load(self.songs_list[self.index]) #load the song at current index
        self.updatelabel()
        pygame.mixer.music.play()                           #play song at current label
        pygame.mixer.music.set_endevent(self.nextt)         #set song end event to user created event called nextt
        self.durationscale.configure(to=self.duration)      #change the divisions of the durationscale according to the duration of the song
        self.duration *= 100                                #convert duration to milliseconds
        self.durationscale.set(0)                           #start duration scale from 0
        self.progress()

    def check(self):
        for event in pygame.event.get(): #check for nextt user created event, when event occurs the nextsong function will be called
            if self.paused:
                break
            if event.type == self.nextt:
                self.nextsong()

    def volume(self, _=None):
        vol = self.volumescale.get()      #get new position of the volumescale and set the playback volume according to that position
        vol = vol / 100
        pygame.mixer.music.set_volume(vol)

    def incvol(self, _=None):
        vol = self.volumescale.get()
        vol += 10
        self.volumescale.set(vol)
        vol = vol / 100
        pygame.mixer.music.set_volume(vol)

    def decvol(self, _=None):
        vol = self.volumescale.get()
        vol -= 10
        self.volumescale.set(vol)
        vol = vol / 100
        pygame.mixer.music.set_volume(vol)

    def progress(self):
        d = self.durationscale.get()
        d *= 100                              #get current position of durationscale and convert to milliseconds
        for i in range(d, self.duration + 1):
            time.sleep(0.01)                  #sleep loop for one millisecond or loop reiterates after one milliesecond
            if i % 100 == 0:
                self.durationscale.set(i / 100) #update durationscale after one second/100 milliseconds
            if self.paused:
                break
            self.check()                       #call check function and update the gui
            root.update()

    def forward(self, _=None):                  #skip forward song by 10 seconds if incremented value is smaller than duration
        f = self.durationscale.get()            #bound to right arrow
        if f + 10 <= self.duration / 100:
            f += 10
            self.durationscale.set(f)
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(f)
            self.progress()

    def forward2(self, _=None):
        f = self.durationscale.get()          #skip forward by 60 seconds if incremented value is smaller than duration
        if f + 60 <= self.duration / 100:     #bound to control + right arrow
            f += 60
            self.durationscale.set(f)
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(f)
            self.progress()

    def backward(self, _=None):
        f = self.durationscale.get()
        if f - 10 >= 0:
            f -= 10
            self.durationscale.set(f)
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(f)
            self.progress()

    def backward2(self, _=None):
        f = self.durationscale.get()
        if f - 60 >= 0:
            f -= 60
            self.durationscale.set(f)
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(f)
            self.progress()

    def forback(self, _=None):
        f = self.durationscale.get()
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(f)
        self.progress()


root = Tk()
app = App(root)
root.mainloop()
