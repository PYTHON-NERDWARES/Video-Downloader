from tkinter import *
import os
import tkinter

# playlist = os.fspath(storagePath)
# Get the list of all videos
# in the video downloader directory
storagePath = r"C:\Users\eslam\Documents\Downloads\Vide_Downloader"
playlist = os.listdir(storagePath)
# print the list
print(playlist)

top1 = Tk()
lb = Listbox(top1)
for i,video in enumerate(playlist):
    lb.insert(i,video)

lb.insert(1, "Bangalore")
lb.insert(2, "Mysore")
lb.insert(3, "Mangalore")
lb.insert(4, "Hubli")
lb.insert(5, "Dharwad")
lb.insert(6, "Belgaum")
lb.pack()
top1.mainloop()



# size = os.path.getsize()
# print(size)


# # search
# # from tkinter import *
# import pytube
#
# root = Tk()
#
# from pytube import *
# import urllib.request
# import requests
# import re
#
# Label(root, text="", font='arial 15 bold').pack()
# link = StringVar(root)
# link_entry = Entry(root, textvariable=link, width=40).pack()
#
# # ******************************
# # https://www.youtube.com/results?search_query=mozart
# search_keyword = "Physics Explained in Ten Seconds"
# main_search_keyword = search_keyword.replace(' ','')
# html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+main_search_keyword)
# video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
# print(video_ids)
# print("https://www.youtube.com/watch?v="+video_ids[0])
# # ******************************
#         # watch_url = "https://www.youtube.com/watch?v="+video_ids[0]
#         # get_info = pytube.extract.video_info_url(video_ids[0],watch_url)
#         # print(get_info)
#
# thumbnail_url = 'https://img.youtube.com/vi/'+video_ids[0]+'/maxresdefault.jpg'
#
# r = requests.get(thumbnail_url)
# with open(video_ids[0] +'.jpg','wb') as f:
#       f.write(r.content)
