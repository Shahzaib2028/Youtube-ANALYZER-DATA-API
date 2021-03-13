from tkinter import *
import PIL
from PIL import Image , ImageTk
from apiclient.discovery import build
import vlc
import pafy
import time
from tkinter import messagebox , ttk
import io
import requests
from pytube import YouTube


api_key = 'Enter your key here'
youtube = build('youtube' , 'v3', developerKey = api_key)

window = Tk()
window.title("YouTube Analyzer")
window.state("zoomed")
window.configure(background = "#4E0707")
window.iconbitmap('icon.ico')

pic1 = Image.open('yt_image.png')
resize1 = pic1.resize((150,150) , Image.ANTIALIAS)
final_pic1 = ImageTk.PhotoImage(resize1)
l2 = Label(window, image = final_pic1 , bg = '#4E0707')
l2.place(x = 80 , y = 20)

pic2 = Image.open('py_image.png')
resize3 = pic2.resize((150,150) , Image.ANTIALIAS)
final_pic2 = ImageTk.PhotoImage(resize3)
l3 = Label(window, image = final_pic2 , bg = '#4E0707')
l3.place(x = 1300 , y = 20)

def btn_hover(e):
    btn1['bg'] = 'gold'

def btn_hover_leave(e):
    btn1['bg'] = 'yellow'

def search():
    time.sleep(1)
    messagebox.showinfo("showinfo", "fetching data please wait...")
    req1 = youtube.search().list(q=e1.get(), part='snippet', type='channel', maxResults=1)
    execute1 = req1.execute()
    channel_id = execute1['items'][0]['id']['channelId']

    def videoLink():
        get = lstbx.get(ANCHOR)
        search_video1 = youtube.search().list(q=get, part='snippet', type='video', maxResults=1)
        execute3 = search_video1.execute()
        get_video_id = execute3['items'][0]['id']['videoId']
        link = 'https://www.youtube.com/watch?v=' + get_video_id
        return link

    def btn2_hover(e):
        btn2['bg'] = 'gold'

    def btn2_hover_leave(e):
        btn2['bg'] = 'yellow'

    def btn3_hover(e):
        btn3['bg'] = 'gold'

    def btn3_hover_leave(e):
        btn3['bg'] = 'yellow'

    def back():
        lstbx.destroy()
        btn2.destroy()
        btn3.destroy()
        s.destroy()

    def get_channel_videos(channel_id):
        # get Uploads playlist id
        res = youtube.channels().list(id=channel_id,
                                      part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos = []
        next_page_token = None

        while 1:
            res = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='snippet',
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
            videos += res['items']
            next_page_token = res.get('nextPageToken')

            if next_page_token is None:
                break

        return videos

    videos = get_channel_videos(channel_id)

    s = Scrollbar(window)
    s.pack(side='right', fill='y')
    lstbx = Listbox(window, bg="#4E0707", fg = "yellow" ,  bd = 10, relief = 'ridge', selectbackground ='#FF7F50',  font="Times 14 bold", yscrollcommand = s.set)
    lstbx.pack(fill = BOTH, expand=True)
    s.config(command=lstbx.yview)

    for video in videos:
        lstbx.insert(END, video['snippet']['title'])

    def submit():
        get_title = lstbx.get(ANCHOR)
        #search for video details by title
        search_video = youtube.search().list(q=get_title,
                                             part='snippet', type='video', maxResults=1)
        execute2 = search_video.execute()
        #getting thumbnail link
        thumbnail_link = execute2['items'][0]['snippet']['thumbnails']['high']['url']
        #display thumbnail on tkinter window
        root = Toplevel()
        root.title("YouTube Video")
        root.geometry('500x700')
        root.configure(background="#4E0707")
        root.iconbitmap('icon.ico')
        l6 = Label(root, text=get_title, bg="#4E0707", fg="yellow", font="Times 12 bold")
        l6.place(x=0 , y = 10)
        response = requests.get(thumbnail_link)
        image_bytes = io.BytesIO(response.content)

        img = PIL.Image.open(image_bytes)
        image = ImageTk.PhotoImage(img)

        thmb = Label(root, image = image)
        thmb.place(x = 10 , y = 40)

        #Gettings stats of the video and display on window
        video_id = execute2['items'][0]['id']['videoId']
        stats = youtube.videos().list(part='statistics, snippet', id=video_id).execute()
        views_count = stats['items'][0]['statistics']['viewCount']
        dislikes_count = stats['items'][0]['statistics']['dislikeCount']
        likes_count = stats['items'][0]['statistics']['likeCount']
        comment_count = stats['items'][0]['statistics']['commentCount']

        # Getting Duration of the video and display
        stats = youtube.videos().list(part='contentDetails, snippet', id=video_id).execute()
        filter_time = stats['items'][0]['contentDetails']['duration']
        Time_slice = filter_time[2:]

        #display all  the stats and duration as a label
        l7 = Label(root, text="DURATION: " + Time_slice, bg="#4E0707", fg="yellow", font="Times 12 bold")
        l7.place(x=10, y=500)
        l8 = Label(root, text= "VIEWS: " + views_count , bg="#4E0707", fg="yellow", font="Times 12 bold")
        l8.place(x=10, y=540)
        l9 = Label(root, text="LIKES: " + likes_count , bg="#4E0707", fg="yellow", font="Times 12 bold")
        l9.place(x=10, y=580)
        l10 = Label(root, text="DISLIKES: " + dislikes_count, bg="#4E0707", fg="yellow", font="Times 12 bold")
        l10.place(x=10, y=620)
        l11 = Label(root, text="COMMENTS: " + comment_count, bg="#4E0707", fg="yellow", font="Times 12 bold")
        l11.place(x=10, y=660)

        def download():
            root.destroy()
            messagebox.showinfo("Downloading" , 'Press OK and wait for downloading until you get a success message')
            save_to = "C:/Users/Dell/Downloads"
            yt = YouTube(videoLink())
            yt.streams.get_highest_resolution().download(save_to)
            messagebox.showinfo('Downloaded', 'downloaded successfully')

        def play():
            root.destroy()
            # for play on vlc
            video_v = pafy.new(videoLink())
            best = video_v.getbest()
            playurl = best.url
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(playurl)
            media.get_mrl()
            player.set_media(media)
            player.play()
            while True:
                time.sleep(1)

        def btn4_hover(e):
            btn4['bg'] = 'gold'

        def btn4_hover_leave(e):
            btn4['bg'] = 'yellow'

        def btn5_hover(e):
            btn5['bg'] = 'gold'

        def btn5_hover_leave(e):
            btn5['bg'] = 'yellow'

        btn4 = Button(root, text='Play', bg='yellow', font="Times 14", bd=4, relief='ridge' , width = 10 , command = play)
        btn4.place(x=120 ,y = 430)
        btn4.bind('<Enter>', btn4_hover)
        btn4.bind('<Leave>', btn4_hover_leave)

        btn5 = Button(root, text='Download', bg='yellow', font="Times 14", bd=4, relief='ridge' , width = 10 , command = download)
        btn5.place(x=270, y=430)
        btn5.bind('<Enter>', btn5_hover)
        btn5.bind('<Leave>', btn5_hover_leave)

        root.mainloop()

    btn2 = Button(window, text='Select', bg='yellow', font="Times 14", bd=4, relief='ridge' , command = submit)
    btn2.pack(pady = 30)
    btn2.bind('<Enter>', btn2_hover)
    btn2.bind('<Leave>', btn2_hover_leave)

    btn3 = Button(window, text='Back', bg='yellow', font="Times 14", bd=4, relief='ridge' , command = back)
    btn3.pack(pady=30)
    btn3.bind('<Enter>', btn3_hover)
    btn3.bind('<Leave>', btn3_hover_leave)

l1 = Label(window , text = "YOUTUBE ANALYZER" , bg = "#4E0707" , fg = "white" , font = "Times 70 bold italic")
l1.pack(pady = 30)

l4 = Label(window , text= 'Search Channel' , bg = "#4E0707" , fg = "white" , font = "Times 30 bold")
l4.place(x = 400, y= 300)
e1 = Entry(window, width = 25, font = "Times 16")
e1.insert(0, 'enter channel name')
e1.place(x = 720, y= 310)

btn1 = Button(window, text= 'search' , bg = 'yellow' , font = "Times 14", bd = 4 , relief = 'ridge' , width = 10, command = search)
btn1.place(x = 700, y= 400)

btn1.bind('<Enter>', btn_hover)
btn1.bind('<Leave>', btn_hover_leave)

window.mainloop()