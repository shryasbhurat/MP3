from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()

root.title("Mp3 PLayer")
root.geometry("500x400")


#initailize pygame
pygame.mixer.init()




# Create a function to deal with time
def play_time():
	#song is stopped?
	if stopped:
		return


	#Grab current song time
	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert current song timeto the format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))



	# Reconstruct song with directory structure
	song =playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'



	# current song length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length

	#converted song length
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	#check to see if song is over
	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused:
		#check to see if paused
		pass
	else:
		#move slider along 1 second ata time
		next_time = int(song_slider.get()) + 1
		# Output new time value to slider and to length of song
		song_slider.config(to=song_length,value= next_time)

		#convert time position to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime((song_slider.get())))

		#output slider
		status_bar.config(text = f'Tme Elapsed {converted_current_time} of {converted_song_length}   ')



	if current_time >= 1:
		#add current time to status bar
		status_bar.config(text = f'Tme Elapsed {converted_current_time} of {converted_song_length}   ')


	#create loop to check the time every second
	status_bar.after(1000, play_time)

#1 song function
def add_song():
	song = filedialog.askopenfilename(initialdir = 'audio/',title="Choose A Song",filetypes=(( "mp3 Files", "*.mp3" ),) )
	#my_label.config(text=song)

	#strip out directory structure and .mp3 fromsong
	song = song.replace("C:/mp3/audio", "")
	song = song.replace(".mp3", "")
	song = song.replace("/", "")

	playlist_box.insert(END, song)

# add many songs
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir = 'audio/',title="Choose A Song",filetypes=(( "mp3 Files", "*.mp3" ),) )
	#my_label.config(text=song)
	#loop through song list and mp3 from song name
	for song in songs:
	#strip out directory structure and .mp3 fromsong
		song = song.replace("C:/mp3/audio", "")
		song = song.replace(".mp3", "")
		song = song.replace("/", "")
		#add to playlist
		playlist_box.insert(END, song)


#cretae functiojn to delete eone song
# delete highlighted song
def delete_song():
	playlist_box.delete(ANCHOR)



#delete all songs
def delete_all_songs():
	playlist_box.delete(0, END)


#create play function
def play():
	#set stopped to false
	global stopped
	stopped = False
	# Reconstruct song with directory structure
	song =playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	#load song
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops= 0)

	#Get song time
	play_time()


#create stop variable
global stopped
stopped = False

#function to stop song
def stop():
	#stop song
	pygame.mixer.music.stop()
	#clear playlist
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text = '')
	#set the slider to 0
	song_slider.config(value=0)

	global stopped
	stopped = True


#paused variable creation
global paused
paused = False


#to pause a song
def pause(is_paused):
	global paused
	paused = is_paused


	if paused:
		#unpause true
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause  false
		pygame.mixer.music.pause()
		paused = True



#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#create a slide function for song positioning
def slide(x):
	song =playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'

	#load song
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops= 0, start=song_slider.get())


#main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)




#create functon to play the next song
def next_song():
	#set the slider and status bar to 0
	status_bar.config(text='')
	song_slider.config(value=0)
	#GEt current song number 
	next_one = playlist_box.curselection()
	# add one to the current tuple / list
	next_one = next_one[0] + 1

	#grab the song title
	song = playlist_box.get(next_one)
	# add directory stuff
	song = f'C:/mp3/audio/{song}.mp3'

	#load song
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops= 0)

	# CLear active BAr in playlist
	playlist_box.selection_clear(0, END)

	# MOve Active bar to next song
	playlist_box.activate(next_one)

	#set the active bar to the next bar
	playlist_box.selection_set(next_one, last=None)



# back song
def back_song():
	#set the slider and status bar to 0
	status_bar.config(text='')
	song_slider.config(value=0)
	#GEt current song number 
	next_one = playlist_box.curselection()
	# subtract one to the current tuple / list
	next_one = next_one[0] - 1

	#grab the song title
	song = playlist_box.get(next_one)
	# add directory stuff
	song = f'C:/mp3/audio/{song}.mp3'

	#load song
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops= 0)

	# CLear active BAr in playlist
	playlist_box.selection_clear(0, END)

	# MOve Active bar to next song
	playlist_box.activate(next_one)

	#set the active bar to the next bar
	playlist_box.selection_set(next_one, last=None)





# create Playllst box
playlist_box = Listbox(main_frame, bg="black", fg="teal",width=60, selectbackground="green",selectforeground="black")
playlist_box.grid(row= 0,column=0,pady=10)

#create volume slider frame
volume_frame = LabelFrame(main_frame,text="volume")
volume_frame.grid(row=0,column=1,padx=20)


#create a sogns slider
song_slider = ttk.Scale(main_frame, from_=0, to=100 , orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2,column=0,pady=20)


# volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1 , orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)





# define button images
Back = PhotoImage(file = "images/back.png")
Forward = PhotoImage(file = "images/forward.png")
Play = PhotoImage(file = "images/play.png")
Pause = PhotoImage(file = "images/pause.png")
Stop = PhotoImage(file = "images/stop.png")

#create butoon frame
control_frame = Frame(main_frame)
control_frame.grid(row= 1 , column=0)

#create buttons
back_button = Button(control_frame,image=Back, borderwidth=0, command=back_song)
forward_button = Button(control_frame,image=Forward, borderwidth=0,command=next_song)
play_button = Button(control_frame,image=Play, borderwidth=0, command=play)
pause_button = Button(control_frame,image=Pause, borderwidth=0, command= lambda: pause(paused))
stop_button = Button(control_frame,image=Stop, borderwidth=0, command=stop)

back_button.grid(row=0,column=0, padx=10)
forward_button.grid(row=0,column=1, padx=10)
play_button.grid(row=0,column=2, padx=10)
pause_button.grid(row=0,column=3, padx=10)
stop_button.grid(row=0,column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create add song
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label = "Add Songs",menu =add_song_menu)
#1 song
add_song_menu.add_command(label ="Add One Song To playlist", command = add_song)
#many Song
add_song_menu.add_command(label ="Add Many Songs To playlist", command = add_many_songs)
#delete song

remove_song_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist",command=delete_all_songs)

#create status bar
status_bar = Label(root, text= '', bd=1, relief=GROOVE, anchor= E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)




#temp label
my_label = Label(root, text='')
my_label.pack(pady = 20)

root.mainloop()