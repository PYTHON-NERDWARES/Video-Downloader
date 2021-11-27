from tkinter import *

import pytube.extract
from moviepy.editor import *
from tkinter import messagebox, ttk
from pytube import *
import _thread
from cefpython3 import cefpython as cef
import ctypes
import tkinter as tk
import sys
import os
import platform
import logging as _logging



storagePath = r"C:\Users\STUDENT\Documents\Downloads\Vide_Downloader"

# main window
root = Tk()
root.title("Youtube Downloader")
root.geometry('1024x600')
root.resizable(0, 0)
root.iconbitmap('logo.ico')

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


# Review

def pre_view():
    url =link.get()
    id = pytube.extract.video_id(url)

    WINDOWS = (platform.system() == "Windows")

    IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"

    class MainFrame(tk.Frame):

        def __init__(self, root):
            self.browser_frame = None

            tk.Grid.rowconfigure(root, 0, weight=1)
            tk.Grid.columnconfigure(root, 0, weight=1)

            tk.Frame.__init__(self, frame1)


            # BrowserFrame
            self.browser_frame = BrowserFrame(self)
            self.browser_frame.grid(row=1, column=0,
                                    sticky=(tk.N + tk.S + tk.E + tk.W))
            tk.Grid.rowconfigure(self, 1, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)

            # Pack MainFrame
            self.pack(fill=tk.BOTH, expand=tk.YES)

        def on_root_configure(self, _):
            if self.browser_frame:
                self.browser_frame.on_root_configure()

        def on_configure(self, event):
            if self.browser_frame:
                width = event.width
                height = event.height

        def on_focus_in(self, _):
            pass

        def on_focus_out(self, _):
            pass

        def on_close(self):
            if self.browser_frame:
                self.browser_frame.on_root_close()
            self.master.destroy()

        def get_browser(self):
            if self.browser_frame:
                return self.browser_frame.browser
            return None

        def get_browser_frame(self):
            if self.browser_frame:
                return self.browser_frame
            return None

        def setup_icon(self):
            resources = os.path.join(os.path.dirname(__file__), "resources")
            icon_path = os.path.join(resources, "tkinter" + IMAGE_EXT)
            if os.path.exists(icon_path):
                self.icon = tk.PhotoImage(file=icon_path)
                # noinspection PyProtectedMember
                self.master.call("wm", "iconphoto", self.master._w, self.icon)

    class BrowserFrame(tk.Frame):

        def __init__(self, master):
            self.closing = False
            self.browser = None
            tk.Frame.__init__(self, master)
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)
            self.bind("<Configure>", self.on_configure)
            self.focus_set()

        def embed_browser(self):
            window_info = cef.WindowInfo()
            rect = [0, 0, self.winfo_width(), self.winfo_height()]
            window_info.SetAsChild(self.get_window_handle(), rect)
            self.browser = cef.CreateBrowserSync(window_info,
                                                 url=f"http://www.youtube.com/embed/{id}")

            self.message_loop_work()

        def get_window_handle(self):
            if self.winfo_id() > 0:
                return self.winfo_id()

            else:
                raise Exception("Couldn't obtain window handle")

        def message_loop_work(self):
            cef.MessageLoopWork()
            self.after(10, self.message_loop_work)

        def on_configure(self, _):
            if not self.browser:
                self.embed_browser()

        def on_root_configure(self):
            # Root <Configure> event will be called when top window is moved
            if self.browser:
                self.browser.NotifyMoveOrResizeStarted()

        def on_mainframe_configure(self, width, height):
            if self.browser:
                if WINDOWS:
                    ctypes.windll.user32.SetWindowPos(
                        self.browser.GetWindowHandle(), 0,
                        0, 0, width, height, 0x0002)

        def on_focus_in(self, _):
            pass
            if self.browser:
                self.browser.SetFocus(True)

        def on_focus_out(self, _):
            pass
            if self.browser:
                self.browser.SetFocus(False)

        def on_root_close(self):
            if self.browser:
                self.browser.CloseBrowser(True)
            self.destroy()

    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)

    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

    app = MainFrame(frame1)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()


view_Button = Button(frame1, text="Review", font="arial 12",fg="white",
                    bg="green",  width=10, height=1, command=pre_view)
view_Button.place(x=620, y=60)

Button(frame1, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2, command=download_page).pack()


root.mainloop()

# https://youtu.be/adJFT6_j9Uk?list=LL



























