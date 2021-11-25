from tkinter import *
from moviepy.editor import *
from tkinter import messagebox, ttk
from pytube import YouTube
import _thread
import os

storagePath = r"C:\Users\STUDENT\Documents\Downloads\Vide_Downloader"

# main window
root = Tk()
root.title("Youtube Downloader")
root.geometry('700x400')
root.resizable(0, 0)


def show_progress_bar(stream, chunk, bytes_remaining):
    progress = int(((stream.filesize - bytes_remaining) / stream.filesize) * 100)
    bar["value"] = progress


# download window


def download():
    quality = ytbchoices.get()
    url = link.get()
    if len(url) > 0:
        msg['text'] = 'Extracting video from youtube...'
        ytb_url = YouTube(url, on_progress_callback=show_progress_bar)
        video = ytb_url.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        audio = ytb_url.streams.filter(only_audio=True).first()

        msg["text"] = "Downloading " + ytb_url.title
        if quality == choices[0]:
            video.last().download(storagePath)
        elif quality == choices[1]:
            video.first().download(storagePath)
        else:
            freshDownload = video.first().download(storagePath)
            basePath, extension = os.path.splitext(freshDownload)
            video = VideoFileClip(os.path.join(basePath + ".mp4"))
            video.audio.write_audiofile(os.path.join(basePath + ".mp3"))
        msg["text"] = "Downloaded Successfully"
        messagebox.showinfo("Download info", "Downloaded Successfully and saved to\n" + storagePath)
    else:
        urlErr["text"] = "Please Enter the URL"


# Heading
Label(root, text="Youtube Video Downloader", font="arial 20 bold").pack()

# url entry
Label(root, text="Paste the link here", font='arial 15 bold').pack()
link = StringVar(root)
link_entry = Entry(root, textvariable=link, width=70).pack()

# url error message
urlErr = Label(root, font='arial 12', fg='red')
urlErr.pack()

# quality
Label(root, text="select the quality of video", font='arial 12 bold').pack(pady=10)
choices = ["low", "high", "audio"]
ytbchoices = ttk.Combobox(root, values=choices)
ytbchoices.pack()

# progress bar
bar = ttk.Progressbar(root, length=300)
bar.pack(pady=10)

# msg
msg = Label(root, font="arial 12", fg="green")
msg.pack()

# download button
Button(root, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2,
       command=lambda: _thread.start_new_thread(download, ())).pack(pady=10)

root.mainloop()
