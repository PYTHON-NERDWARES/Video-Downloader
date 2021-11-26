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
root.geometry('800x500')
root.resizable(0, 0)

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# create frames
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)

# add frames to notebook

notebook.add(frame1, text='Main')
notebook.add(frame2, text='Download')


# Heading
Label(frame1, text="Youtube Video Downloader", font="arial 20 bold").pack()

# url entry
Label(frame1, text="Paste the link here", font='arial 15 bold').pack()
link = StringVar(frame1)
link_entry = Entry(frame1, textvariable=link, width=70)
link_entry.pack()
# url error message
urlErr = Label(frame1, font='arial 12', fg='red')
urlErr.pack()

# quality
Label(frame2, text="select the quality of video", font='arial 12 bold').pack(pady=10)
choices = ["low", "high", "audio"]
ytbchoices = ttk.Combobox(frame2, values=choices)
ytbchoices.current(0)
ytbchoices.pack()

def show_progress_bar(stream, chunk, bytes_remaining):
    progress = int(((stream.filesize - bytes_remaining) / stream.filesize) * 100)
    bar["value"] = progress

def download():
    try:
        quality = ytbchoices.get()
        url = link.get()
        if len(url) > 0:
            ytb_url = YouTube(url, on_progress_callback=show_progress_bar)
            video = ytb_url.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            msg['text'] = 'Extracting video from youtube...'
            widget.bind('<Button-1>', pro)
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
                video.close()
                video_path = os.path.join(basePath + ".mp4")
                os.remove(video_path)
            msg["text"] = "Downloaded Successfully"
            messagebox.showinfo("Download info", "Downloaded Successfully and saved to\n" + storagePath)
        else:
            urlErr["text"] = "Please Enter the URL"
            notebook.select(frame1)
    except:
        messagebox.showinfo('Error',"Please Enter a YouTube URL")


def download_page():
    if not link_entry.get():
        urlErr["text"] = "Please Enter the URL"
    else:
        urlErr["text"] = ""
        notebook.select(frame2)



# progress bar
bar = ttk.Progressbar(frame2, length=300)

def pro(event):
    bar.pack(pady=10)



# msg
msg = Label(frame2, font="arial 12", fg="green")
msg.pack()



widget = Button(frame2, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2,
                command=lambda: _thread.start_new_thread(download, ()))
widget.pack()


Button(frame1, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2, command=download_page).pack()





root.mainloop()

# https://youtu.be/adJFT6_j9Uk?list=LL
