from tkinter import *
import os
from moviepy.editor import *
import tkinter

# playlist = os.fspath(storagePath)
# Get the list of all videos
# in the video downloader directory
storagePath = r"C:\Users\eslam\Documents\Downloads\Vide_Downloader"
playlist = os.listdir(storagePath)
# print the list
print(playlist)

top1 = Tk()
Label(top1, text="Video Downloaded Media", font="arial 20 bold").pack()
lb = Listbox(top1)
for i,video in enumerate(playlist):
    lb.insert(i,video)
    lb.pack()
    clip = VideoFileClip(video)

    # clipping of the video
    # getting video for only starting 10 seconds
    clip = clip.subclip(0, 10)

    # rotating video by 180 degree
    clip = clip.rotate(180)

    # Reduce the audio volume (volume x 0.5)
    clip = clip.volumex(0.5)

    # showing clip
    clip.ipython_display(width=280)
top1.mainloop()

###  delete video:
import os

# File name
# file = 'file1.txt'
#
# # File location
# location = "D:/Pycharm projects/GeeksforGeeks/Authors/Nikhil/"
#
# # Path
# path = os.path.join(location, file)
#
# # Remove the file
# # 'file.txt'
# os.remove(path)
# size = os.path.getsize("filename")


