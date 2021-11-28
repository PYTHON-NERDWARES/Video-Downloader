import tkinter as tk
from tkinter import simpledialog
from tkVideoPlayer import TkinterVideo
from pyffmpeg import FFmpeg
import os

root =tk.Tk()
root.geometry("400x400+400+400")
storagePath = r"C:\Users\eslam\Documents\Downloads\Vide_Downloader"
framePlayer = tk.Frame(root, borderwidth=1, relief='groove')
lable_menu = tk.Label(framePlayer,text="Related Videos",font=("Helvetica",18,"bold"), fg="black", bg="rosybrown")
lable_menu.pack(pady=5)
framePlayer.pack(pady=5)

list_video = tk.Listbox(root,width=35,height=5,font=("Times",15,"italic"),bg="wheat")
list_video.pack()

def mediaPlay(event):
    if list_video.curselection():
        video = list_video.curselection()[0]
        # os.startfile(os.path.join(storagePath,list_video.get(video)))
# try to tkVideoPlayer
        videoplayer = TkinterVideo(master=root, scaled=True, pre_load=False)
        videoplayer.load(os.path.join(storagePath,list_video.get(video)))
        videoplayer.pack(expand=True, fill="both")
        videoplayer.play()  # play the video

# from pyffmpeg import FFmpeg

        inf = os.path.join(storagePath,list_video.get(video))
        outf = 'thumb.jpg'
        ff = FFmpeg()
        ff.convert(inf, outf)


for video in os.listdir(storagePath):
    list_video.insert(tk.END,video)

start_button = tk.Button(root,text = "Play",font=("Arial",14),bg="Tan")
start_button.pack(fill="x", expand="no")
start_button.bind("<ButtonPress-1>",mediaPlay)

def top():
    root.destroy()

def delete(event):
    if list_video.curselection():
        video = list_video.curselection()[0]
        os.remove(os.path.join(storagePath,list_video.get(video)))
        list_video.delete(video)

exit_button = tk.Button(root,text = "Exit",font=("Arial",14),bg="Tan", command=top)
exit_button.pack(fill="x", expand="no")

delete_button = tk.Button(root,text = "Delete",font=("Arial",14),bg="Tan")
delete_button.pack(fill="x", expand="no")
delete_button.bind("<ButtonPress>",delete)

root.mainloop()




