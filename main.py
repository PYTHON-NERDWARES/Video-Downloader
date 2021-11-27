from tkinter import *

import pytube.extract
from moviepy.editor import *
from tkinter import messagebox, ttk
from pytube import *
import _thread

from cefpython3 import cefpython as cef
import ctypes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
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
saved_link =link.get()
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

is_run =False
pre_frame =None
pre_frame_flag = False
def pre_view(event=None):
    global pre_frame_flag, browser, pre_frame

    if pre_frame_flag == False:
        pre_frame_flag = True
        global is_run, saved_link
        url =link.get()
        id = pytube.extract.video_id(url)
        pre_frame = Frame(frame1)
        pre_frame.pack(fill='both', expand=True)

        WindowUtils = cef.WindowUtils()

        # Platforms
        WINDOWS = (platform.system() == "Windows")
        LINUX = (platform.system() == "Linux")
        MAC = (platform.system() == "Darwin")

        # Globals
        logger = _logging.getLogger("tkinter_.py")

        # Constants
        # Tk 8.5 doesn't support png images
        IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"

        class MainFrame(tk.Frame):
            def __init__(self, root):

                self.browser_frame = None
                self.navigation_bar = None
                self.old_frame = None

                tk.Grid.rowconfigure(root, 0, weight=1)
                tk.Grid.columnconfigure(root, 0, weight=1)

                # MainFrame
                tk.Frame.__init__(self, root)


                # BrowserFrame
                self.browser_frame = BrowserFrame(self, self.navigation_bar)
                self.browser_frame.grid(row=1, column=0,
                                        sticky=(tk.N + tk.S + tk.E + tk.W))
                tk.Grid.rowconfigure(self, 1, weight=1)
                tk.Grid.columnconfigure(self, 0, weight=1)

                # Pack MainFrame

                self.pack(fill=tk.BOTH, expand=tk.YES)

            def on_root_configure(self, _):
                logger.debug("MainFrame.on_root_configure")
                if self.browser_frame:
                    self.browser_frame.on_root_configure()

            def on_configure(self, event):
                logger.debug("MainFrame.on_configure")
                if self.browser_frame:
                    width = event.width
                    height = event.height
                    if self.navigation_bar:
                        height = height - self.navigation_bar.winfo_height()
                    self.browser_frame.on_mainframe_configure(width, height)



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


        class BrowserFrame(tk.Frame):

            def __init__(self, master, navigation_bar=None):
                self.navigation_bar = navigation_bar
                self.closing = False
                self.browser = None
                tk.Frame.__init__(self, master)

                self.bind("<Configure>", self.on_configure)
                self.focus_set()

            def embed_browser(self):
                    window_info = cef.WindowInfo()
                    rect = [110, 20, 900, 400]
                    window_info.SetAsChild(self.winfo_id(), rect)
                    # https://youtu.be/adJFT6_j9Uk?list=LL
                    self.browser = cef.CreateBrowserSync(window_info,
                                                         url=f"http://youtube.com/embed/{id}?rel=0&loop=1")
                    assert self.browser
                    self.browser.SetClientHandler(LoadHandler(self))
                    # self.browser.SetClientHandler(FocusHandler(self))
                    self.message_loop_work()

            def get_window_handle(self):
                if self.winfo_id() > 0:
                    return self.winfo_id()
                elif MAC:
                    # On Mac window id is an invalid negative value (Issue #308).
                    # This is kind of a dirty hack to get window handle using
                    # PyObjC package. If you change structure of windows then you
                    # need to do modifications here as well.
                    # noinspection PyUnresolvedReferences
                    from AppKit import NSApp
                    # noinspection PyUnresolvedReferences
                    import objc
                    # Sometimes there is more than one window, when application
                    # didn't close cleanly last time Python displays an NSAlert
                    # window asking whether to Reopen that window.
                    # noinspection PyUnresolvedReferences
                    return objc.pyobjc_id(NSApp.windows()[-1].contentView())
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
                    elif LINUX:
                        self.browser.SetBounds(0, 0, width, height)
                    self.browser.NotifyMoveOrResizeStarted()


            def on_root_close(self):
                if self.browser:
                    self.browser.CloseBrowser(True)
                    self.clear_browser_references()
                self.destroy()

            def clear_browser_references(self):
                # Clear browser references that you keep anywhere in your
                # code. All references must be cleared for CEF to shutdown cleanly.
                self.browser = None

        class LoadHandler(object):

            def __init__(self, browser_frame):
                self.browser_frame = browser_frame

            def OnLoadStart(self, browser, **_):
                if self.browser_frame.master.navigation_bar:
                    self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())


        if not is_run or link.get() != saved_link:
            is_run = True
            saved_link=link.get()
            logger.setLevel(_logging.INFO)
            stream_handler = _logging.StreamHandler()
            formatter = _logging.Formatter("[%(filename)s] %(message)s")
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            logger.info("CEF Python {ver}".format(ver=cef.__version__))
            logger.info("Python {ver} {arch}".format(
                ver=platform.python_version(), arch=platform.architecture()[0]))
            logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
            assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
            sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error


            MainFrame(pre_frame)
            # Tk must be initialized before CEF otherwise fatal error (Issue #306)
            cef.Initialize()

    else:
        pre_frame.pack_forget()
        pre_frame_flag = False
        pre_view()


view_Button = Button(frame1, text="Review", font="arial 12", fg="white",
                    bg="green",  width=10, height=1, command=pre_view)
view_Button.place(x=620, y=60)


Button(frame1, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2, command=download_page).pack()
link_entry.bind('<Return>', pre_view)


root.mainloop()
cef.Shutdown()

# https://youtu.be/adJFT6_j9Uk?list=LL



