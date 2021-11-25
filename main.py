from tkinter import *
from tkinter import messagebox ,ttk
from pytube import *

root = Tk()
root.title('Viedo Downloader')
root.geometry("800x600")
root.resizable(False, False)
root.config(background='#D5DBDB')
root.iconbitmap('logo.ico')

# ------- title ------
title = Label(root, text='Welcome To Your Video Downloader', font=('Courier', 25), bg='black', fg='white')
title.pack(fill=X)

title2 = Label(root, text='https://youtu.be/adJFT6_j9Uk?list=LL', font=('Courier', 25), bg='white', fg='white')
title2.pack(fill=X)

# -------- Frame ------
# fr1 = Frame(root, width='300', height = '350' , bg = 'whitesmoke')
# fr1.pack(pady = 30)
# --------- image -------

# photo = PhotoImage(file = 'Prey-logo-1-icon.png')
# panel = Label(root, image = photo)
# panel.pack()

# --------- Lable ---------
# Url_lable = Label(root, text="URL   :", font=('Courier', 20))
# Url_lable.place(x=10, y=110)

list_Button = Button(root, text="PlayList", bg="green", font=('Courier', 25))
list_Button.place(x=610, y=70, width=180, height=37)




# ------- Entry _____
url_path = Entry(root)
url_path.place(x=40, y=240, width=500, height=37)

def init_cal():
    calc = Toplevel()
    calc.title('Viedo Downloader')
    calc.geometry("800x600")
    calc.resizable(False, False)
    calc.config(background='#D5DBDB')
    calc.iconbitmap('logo.ico')

    root.withdraw()
    path = str(url_path.get())
    yt = YouTube(path)
    print(yt.title)
    video_lable = Label(calc, text=f'{yt.title}')
    video_lable.pack()

    video_Quality = yt.streams.filter(progressive=True)
    audio_Quality = yt.streams.filter(only_audio=True)
    # if video_Quality and audio_Quality:
    #     for stream in video_Quality:
    #         stream_lable = Label(calc, text=stream)
    #         stream_lable.pack()
    #
    #     for audio in audio_Quality:
    #         audio_lable = Label(calc, text=audio)
    #         audio_lable.pack()

    res = Label(calc, text='Resolution')
    res.pack(width=500, height=37)

    resolution =ttk.Combobox(calc, textvariable=video_Quality)
    resolution.bind('<<ComboboxSelected>>', callback)

    variable = StringVar(calc)
    variable.set("one")  # default value
    w = OptionMenu(calc, variable, "one", "two", "three")
    w.pack(w)
        # stream = yt.streams.get_by_itag(22)
        # stream.download(output_path=r'C:\Users\STUDENT\Documents\Downloads\Vide_Downloader')



    def on_closing():
        calc.destroy()
        root.deiconify()
    calc.protocol("WM_DELETE_WINDOW", on_closing)

# https://youtu.be/adJFT6_j9Uk?list=LL

def handler():
    if url_path.get() :
        myButton = Button(root, text="Download", command=init_cal, bg="green", font=('Courier', 25))
        myButton.place(x=300, y=350, width=200, height=37)

    else:
        messagebox.showwarning(title='Error', message='Please Enter The Video URL ')


Enter_Button = Button(root, text="Enter", bg="green", font=('Courier', 25), command=handler)
Enter_Button.place(x=560, y=240, width=140, height=37)

root.mainloop()


