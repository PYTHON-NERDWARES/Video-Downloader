

my_game.insert(parent='', index='end', iid=i+1, text='',
                       values=(img, title, rating, length))


# game_frame = Frame(frame3)
# game_frame.pack(pady=15)

# scrollbar
game_scroll = Scrollbar(frame3)
game_scroll.pack(side=RIGHT, fill=Y)

my_game = ttk.Treeview(frame3, yscrollcommand=game_scroll.set)
my_game.pack()


# define our column

my_game['columns'] = ('img', 'title', 'rating', 'length')

# format our column
my_game.column("#0", width=0, stretch=NO)
my_game.column("img", anchor=CENTER, width=200)
my_game.column("title", anchor=CENTER, width=400)
my_game.column("rating", anchor=CENTER, width=50)
my_game.column("length", anchor=CENTER, width=50)
# my_game.column("label", anchor=CENTER, width=80)

# Create Headings
my_game.heading("#0", text="", anchor=CENTER)
my_game.heading("img", text="img", anchor=CENTER)
my_game.heading("title", text="title", anchor=CENTER)
my_game.heading("rating", text="rating", anchor=CENTER)
my_game.heading("length", text="length", anchor=CENTER)
# my_game.heading("player_city", text="States", anchor=CENTER)


###################################################################