import time
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
from tkhtmlview import HTMLLabel
import urllib.request
import re
import datetime

storagePath = r"C:\Users\STUDENT\Documents\Downloads\Vide_Downloader"

# main window
root = Tk()
root.title("Youtube Downloader")
root.geometry('1200x600')
root.resizable(0, 0)
root.iconbitmap('assets/img/logologo (1).ico')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# create frames
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

# add frames to notebook

notebook.add(frame1, text='Main')
notebook.add(frame2, text='Download')
notebook.add(frame3, text='Search')
notebook.add(frame4, text='Downloaded Media')

# Heading
Label(frame1, text="Youtube Video Downloader", font="arial 20 bold").pack()

Frame(frame1,width=1200, height=70).pack()

# url entry
link = StringVar(frame1)
saved_link = link.get()
link_entry = Entry(frame1, textvariable=link, width=60, font="arial 12 ")
link_entry.insert(0, 'Paste the link here')
link_entry.bind("<FocusIn>", lambda args: link_entry.delete('0', 'end'))
link_entry.place(x=200, y=65)

# quality
Label(frame2, text="Select The Quality of Video", font='arial 25 bold').pack(pady=10)
choices = ["Low Resolution", "High Resolution", "Audio(MP3)"]
ytbchoices = ttk.Combobox(frame2, width=50, values=choices, font='arial 12 bold')
ytbchoices.current(0)
ytbchoices.pack()

live_download = 0
speed = 1


def show_progress_bar(stream, chunk, bytes_remaining):
    global live_download, speed
    progress = float(
        (float(stream.filesize - bytes_remaining) / float(stream.filesize)) * float(100))

    while live_download < progress:
        time.sleep(0.05)
        bar["value"] += (speed / 100) * 100
        live_download += speed
        msg3['text'] = str(int(live_download)) + '%  Downloaded'


# msg

msg = Label(frame2, font="arial 12", fg="green")
msg.pack()
msg2 = Label(frame2, font="arial 12", fg="green")
msg2.pack()
msg3 = Label(frame2, font="arial 12", fg="green")
msg3.pack()



def search_download(preview_link):
    global link
    notebook.select(frame2)
    link.set(preview_link)


def download():
    try:
        global msg4
        quality = ytbchoices.get()
        url = link.get()
        if len(url) > 0:
            msg['text'] = 'Extracting video from youtube...'
            widget["state"] = "disabled"
            ytb_url = YouTube(url, on_progress_callback=show_progress_bar)
            video = ytb_url.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            msg["text"] = "Downloading " + ytb_url.title
            img = ytb_url.thumbnail_url
            msg4 = HTMLLabel(frame2, html=f"<img width='800' height='350' src ='{img}'>", width=800,height=350)
            msg4.place(x=200, y=250)

            if quality == choices[0]:
                stream = video.last()
                msg2['text'] = 'FileSize : ' + str(round(stream.filesize / (1024 * 1024))) + 'MB'
                video.last().download(storagePath)
            elif quality == choices[1]:
                stream = video.first()
                msg2['text'] = 'FileSize : ' + str(round(stream.filesize / (1024 * 1024))) + 'MB'
                video.first().download(storagePath)
            else:
                stream = video.last()
                msg2['text'] = 'FileSize : ' + str(round(stream.filesize / (1024 * 1024))) + 'MB'
                fresh_download = video.first().download(storagePath)
                base_path, extension = os.path.splitext(fresh_download)
                video = VideoFileClip(os.path.join(base_path + ".mp4"))
                video.audio.write_audiofile(os.path.join(base_path + ".mp3"))
                video.close()
                video_path = os.path.join(base_path + ".mp4")
                os.remove(video_path)
            msg["text"] = "Downloaded Successfully"
            widget["state"] = "normal"
            x.mp3()

            messagebox.showinfo("Download info", "Downloaded Successfully and saved to\n" + storagePath)
        else:
            messagebox.showinfo('Error', "Please Enter a YouTube URL")
            notebook.select(frame1)

    except:
        messagebox.showinfo('Error', "Please Enter a YouTube URL")
        widget["state"] = "normal"



def download_page():
    if not link_entry.get():
        messagebox.showinfo('Error', "Please Enter a YouTube URL")
    else:
        notebook.select(frame2)


# progress bar
bar = ttk.Progressbar(frame2, length=600)
bar.pack(pady=10)

widget = Button(frame2, text="DOWNLOAD", fg="white", bg="#E21717", width=17, height=2,
                command=lambda: _thread.start_new_thread(download, ()))
widget.pack()


# Review

is_run = False
is_run2 = False

pre_frame = None
pre_frame2 = None

pre_frame_flag = False
pre_frame_flag2 = False


def pre_view(e=None):
    try:
        global pre_frame_flag, pre_frame
        if not pre_frame_flag:
            url = link.get()
            video_id = pytube.extract.video_id(url)
            pre_frame_flag = True
            global is_run, saved_link
            pre_frame = Frame(frame1)
            pre_frame.pack(fill='both', expand=True)

            cef.WindowUtils()

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
                    rect = [100, 15, 1100, 440]
                    window_info.SetAsChild(self.winfo_id(), rect)
                    # https://youtu.be/adJFT6_j9Uk?list=LL
                    self.browser = cef.CreateBrowserSync(window_info,
                                                         url=f"http://youtube.com/embed/{video_id}?rel=0")
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
                saved_link = link.get()
                # logger.setLevel(_logging.INFO)
                # stream_handler = _logging.StreamHandler()
                # formatter = _logging.Formatter("[%(filename)s] %(message)s")
                # stream_handler.setFormatter(formatter)
                # logger.addHandler(stream_handler)
                # logger.info("CEF Python {ver}".format(ver=cef.__version__))
                # logger.info("Python {ver} {arch}".format(
                #     ver=platform.python_version(), arch=platform.architecture()[0]))
                # logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
                assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
                sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

                MainFrame(pre_frame)
                # Tk must be initialized before CEF otherwise fatal error (Issue #306)
                cef.Initialize()

        else:
            pre_frame.pack_forget()
            pre_frame_flag = False
            is_run = False
            pre_view()
    except:
        # raise Exception
        messagebox.showinfo('Error', "Please Enter a YouTube URL")


view_Button = Button(frame1, text="Preview", font="arial 12", fg="white",
                     bg="green", command=lambda: pre_view())
view_Button.place(x=750, y=60)

Button(frame1, text="DOWNLOAD PAGE", font="arial 12", fg="white", bg="#E21717", command=download_page).place(x=825, y=60)
link_entry.bind('<Return>', pre_view)

# https://youtu.be/adJFT6_j9Uk?list=LL


search_link = StringVar()
search_entry = Entry(frame3, textvariable=search_link, width=50, font=12)
search_entry.pack(pady=13)

searched_flag = False


def search():
    global searched_flag, canvas1, scroll, pre_frame2

    if not searched_flag:
        canvas2 = Canvas(frame3, width=740, height=550)
        canvas2.create_window((0, 0), window=pre_frame2, anchor='nw')
        canvas2.pack(fill=BOTH, expand=True)

        canvas1 = Canvas(frame3, width=460, height=550)
        scroll = Scrollbar(canvas2, orient=VERTICAL, command=canvas1.yview)
        scroll.pack(side=RIGHT, fill=Y)
        canvas1.configure(yscrollcommand=scroll.set)
        search_list_frame = Frame(canvas1)
        canvas1.create_window((0, 0), window=search_list_frame, anchor='nw')
        canvas1.place(x=0, y=50)

        searched_flag = True
        search_keyword = search_link.get()
        main_search_keyword = search_keyword.replace(' ', '')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + main_search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        j = 1
        url_arr = []
        search_Button_in = {}
        for i, video in enumerate(video_ids):
            try:
                ############################################################
                item_frame = Frame(search_list_frame, width=450, height=110)
                item_frame.pack(fill='both', expand=True)
                watch_url = "https://www.youtube.com/watch?v=" + video

                def search_view(search_link=watch_url):  ##############################
                    try:
                        global pre_frame_flag2, pre_frame2
                        if pre_frame_flag2 == False:
                            widget = Button(frame3, text="DOWNLOAD", fg="white", font="arial 11", bg="#E21717",
                                            width=15,
                                            command=lambda:search_download(search_link))
                            widget.place(x=1017, y=20)
                            url = search_link
                            print(url)
                            video_id = pytube.extract.video_id(url)
                            pre_frame_flag2 = True
                            global is_run2, saved_link
                            pre_frame2 = Frame(canvas2)
                            pre_frame2.pack(fill=BOTH, expand=True)

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

                                    self.pack(fill=BOTH, expand=True)

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
                                    rect = [460, 10, 1160, 500]
                                    window_info.SetAsChild(self.winfo_id(), rect)
                                    # https://youtu.be/adJFT6_j9Uk?list=LL
                                    self.browser = cef.CreateBrowserSync(window_info,
                                                                         url=f"http://youtube.com/embed/{video_id}?rel=0")
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

                            if not is_run2:
                                is_run2 = True
                                # saved_link = link.get()
                                # logger.setLevel(_logging.INFO)
                                # stream_handler = _logging.StreamHandler()
                                # formatter = _logging.Formatter("[%(filename)s] %(message)s")
                                # stream_handler.setFormatter(formatter)
                                # logger.addHandler(stream_handler)
                                # logger.info("CEF Python {ver}".format(ver=cef.__version__))
                                # logger.info("Python {ver} {arch}".format(
                                #     ver=platform.python_version(), arch=platform.architecture()[0]))
                                # logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
                                assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
                                sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

                                MainFrame(pre_frame2)

                                # Tk must be initialized before CEF otherwise fatal error (Issue #306)
                                cef.Initialize()

                        else:
                            pre_frame2.pack_forget()
                            pre_frame_flag2 = False
                            is_run2 = False
                            search_view(search_link)

                    except:
                        messagebox.showinfo('Error', "Please Enter a YouTube URL")

                ############################################################

                yt = YouTube(watch_url)
                img = yt.thumbnail_url
                img_lable = HTMLLabel(item_frame, html=f"<img width='200' height='100' src ='{img}'>", width=40,
                                      height=7)
                img_lable.place(x=0, y=0)
                title = yt.title
                rating = yt.rating
                rate = round(rating, 1)
                length = yt.length
                length_min = str(datetime.timedelta(seconds=length))
                # # add data
                title_lable = Label(item_frame, text=f'{title}\nRating: {rate}\nLength: {length_min}', wraplength=240,
                                    justify='left')
                title_lable.place(x=210, y=10)
                search_Button_in[watch_url] = Button(item_frame, text="PreView", font="arial 9", fg="white",
                                                     bg="green", width=10, command=search_view)
                url_arr.append(search_Button_in)
                search_Button_in[watch_url].place(x=365, y=70)

                if i > 4:
                    canvas1.configure(scrollregion=(0, 0, 0, 550 + (j * 115)))
                    j += 1
            except:
                print("break")
                break
    else:
        scroll.pack_forget()
        canvas1.destroy()
        searched_flag = False
        search()


search_Button = Button(frame3, text="Search", font="arial 10", fg="white",
                       bg="green", width=10, command=lambda: _thread.start_new_thread(search, ()))
search_Button.place(x=750, y=10)

# playlist

from tkinter import simpledialog
from tkVideoPlayer import TkinterVideo
from pyffmpeg import FFmpeg

#####################################################################


# playlist

import pygame



img_frame4 = Frame(frame4)
image = PhotoImage(file="assets/img/logologo (5).png")
Label(img_frame4, image=image).pack()
img_frame4.place(x=120, y=220)

img_frame1 = Frame(frame1)
Label(img_frame1, image=image).pack()
img_frame1.place(x=379, y=135)

img_frame2 = Frame(frame2)
Label(img_frame2, image=image).pack()
img_frame2.place(x=379, y=250)

img_frame3 = Frame(frame3)
Label(img_frame3, image=image).pack()
img_frame3.place(x=379, y=120)

# Defining MusicPlayer Class
class MP3Player:

    # Defining Constructor
    def __init__(self, root):
        self.root = root
        # Title of the window
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()

        self.song = None
        self.play_image = PhotoImage(file="assets/img/play.png")
        self.pause_image = PhotoImage(file="assets/img/pause.png")
        self.unpause_image = PhotoImage(file="assets/img/unpause.png")
        self.delete_image = PhotoImage(file="assets/img/delet.png")
        self.folder_image = PhotoImage(file="assets/img/folder.png")

        # Creating Track Frame for Song label & status label
        trackframe = LabelFrame(self.root, text="Track", font=("times new roman", 15, "bold"), bg="grey", fg="white",
                                bd=5, relief=GROOVE)
        trackframe.place(x=0, y=0, width=800, height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe, textvariable=self.track, width=20, font=("times new roman", 24, "bold"),
                          bg="grey", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Status Label
        trackstatus = Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="grey",
                            fg="gold").grid(row=0, column=1, padx=10, pady=5)

        # Creating Button Frame
        buttonframe = LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), bg="grey",
                                 fg="white", bd=5, relief=GROOVE)
        buttonframe.place(x=0, y=100, width=800, height=100)
        # # Inserting Play Button
        Button(buttonframe, command=lambda: _thread.start_new_thread(self.playsong, ()),bg="grey", width=60,
                         height=60, border = 0,image=self.play_image, fg="navyblue").grid(row=0, column=0,
                                                                                                        padx=35, pady=5)
        # Inserting Pause Button
        Button(buttonframe, command=self.pausesong, width=60, height=60,
                         border = 0,image=self.pause_image, fg="navyblue", bg="grey").grid(row=0, column=1, padx=35,
                                                                                              pady=5)
        # Inserting Unpause Button
        Button(buttonframe, border = 0, command=self.unpausesong, width=60, height=60,
                         image=self.unpause_image, fg="navyblue", bg="grey").grid(row=0, column=2, padx=35,
                                                                                              pady=5)
        # Inserting delete Button
        Button(buttonframe, border = 0, command=self.delete, width=60, height=60,
                         image=self.delete_image, fg="navyblue", bg="grey").grid(row=0, column=3, padx=35,
                                                                                             pady=5)

        def directory():
            os.startfile(storagePath)

        # Inserting Open in Folder
        Button(buttonframe, border = 0, command=directory, width=60, height=60,image=self.folder_image,
                          fg="navyblue", bg="grey").grid(row=0, column=5, padx=35,
                                                                                              pady=5)

        # Creating Playlist Frame
        songsframe = LabelFrame(self.root, text="Audio list", font=("times new roman", 15, "bold"), bg="grey",
                                fg="white", bd=5, relief=GROOVE)
        songsframe.place(x=670, y=0, width=530, height=290)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)

        # Inserting Playlist listbox
        def list1(e):
            self.song = 1

        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,
                                font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH, expand=True)
        self.playlist.bind("<<ListboxSelect>>", list1)
        self.mp3()
        # Changing Directory for fetching Songs
    def mp3(self):
        os.chdir(storagePath)
        # Fetching Songs
        MP3tracks = os.listdir()
        # Inserting Songs into Playlist
        for track in MP3tracks:
            if track.endswith('.mp3'):
                self.playlist.insert(END, track)
        # ******************  MP4 *********************************************
        MP4frame = LabelFrame(self.root, text="Videos list", font=("times new roman", 15, "bold"), bg="grey",
                              fg="white",
                              bd=5, relief=GROOVE)
        MP4frame.place(x=670, y=285, width=530, height=295)
        # Inserting scrollbar
        scrol_y = Scrollbar(MP4frame, orient=VERTICAL)

        # Inserting Playlist listbox
        def list2(e):
            self.song = 2

        self.playlist2 = Listbox(MP4frame, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,
                                 font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist2.yview)
        self.playlist2.pack(fill=BOTH, expand=True)
        self.playlist2.bind("<<ListboxSelect>>", list2)
        # Changing Directory for fetching Songs
        os.chdir(storagePath)
        # Fetching Songs
        MP4tracks = os.listdir()
        # Inserting Songs into Playlist
        for track in MP4tracks:
            if not track.endswith('.mp3'):
               self.playlist2.insert(END, track)

    def playsong(self):
        # Displaying Selected Song title
        if self.song == 1:
            self.track.set(self.playlist.get(ACTIVE))
            # Displaying Status
            self.status.set("-Playing")
            # Loading Selected Song
            pygame.mixer.music.load(self.playlist.get(ACTIVE))
            # Playing Selected Song
            pygame.mixer.music.play()

        elif self.song == 2:
            self.pausesong()
            # Displaying Selected Song title
            self.track.set(self.playlist2.get(ACTIVE))
            # Displaying Status
            self.status.set("-Playing")
            # Loading Selected Song
            # pygame.mixer.music.load(self.playlist2.get(ACTIVE))
            # Playing Selected Song
            # pygame.mixer.music.play()
            os.startfile(os.path.join(storagePath, self.playlist2.get(ACTIVE)))

    def delete(self):
            if self.song == 1:
                self.track.set(self.playlist.get(ACTIVE))
                # Displaying Status
                self.status.set("- Deleted")
                # deleting Selected Song
                os.remove(os.path.join(storagePath, self.playlist.get(ACTIVE)))
                self.playlist.delete(ACTIVE)

            else:
                # Displaying Selected Song title
                self.track.set(self.playlist2.get(ACTIVE))
                # Displaying Status
                self.status.set("- Deleted")
                # deleting Selected Song
                os.remove(os.path.join(storagePath, self.playlist2.get(ACTIVE)))
                self.playlist2.delete(ACTIVE)


    def pausesong(self):
            # Displaying Status
            self.status.set("-Paused")
            # Paused Song
            pygame.mixer.music.pause()

    def unpausesong(self):
            # Displaying Status
            self.status.set("-Playing")
            # Playing back Song
            pygame.mixer.music.unpause()





# Passing Root to MusicPlayer Class
x = MP3Player(frame4)
# Root Window Looping





# ####################################################################

root.mainloop()
cef.Shutdown()
