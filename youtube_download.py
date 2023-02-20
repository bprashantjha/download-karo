from tkinter import *
from tkinter.ttk import Progressbar, Combobox
from tkinter import ttk
from pytube import YouTube, Playlist

root = Tk()
root.geometry('500x500')
root.resizable(0, 0)
root.title("DownloadKaro")

# Apply custom style to the progress bar
style = ttk.Style()
style.theme_use('clam')
style.configure('custom.Horizontal.TProgressbar', troughcolor='black', background='pale violet red')

# Labels and entry fields
Label(root, text='DownloadKaro', font='Arial 25 bold', fg='white', bg='pale violet red', width=20).pack(pady=10)

link = StringVar()
Label(root, text='Paste Link Here:', font='Arial 12 bold').place(x=150, y=90)
link_enter = Entry(root, width=50, textvariable=link).place(x=32, y=120)

video_selection_dropdown = Combobox(root, width=50, state='readonly')
video_selection_dropdown.place(x=32, y=200)

video_format_selection_dropdown = Combobox(root, width=50, state='readonly')
video_format_selection_dropdown.place(x=32, y=250)

progress_bar = Progressbar(root, orient='horizontal', length=300, mode='determinate', style='custom.Horizontal.TProgressbar')
progress_bar.place(x=100, y=350)

# Download function and progress callback
def Downloader():
    url = str(link.get())
    if 'playlist' in url:
        playlist = Playlist(url)
        video_links = [video_url for video_url in playlist.video_urls]
        video_titles = [video.title for video in playlist.videos]
        video_selection_dropdown['values'] = video_titles
        video_selection_dropdown.current(0)
        selected_video_index = video_selection_dropdown.current()
        video_url = video_links[selected_video_index]
        video = YouTube(video_url)
    else:
        video = YouTube(url)

    video_formats = video.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc()
    video_format_labels = [f'{stream.resolution} ({stream.fps} fps)' for stream in video_formats]
    video_format_selection_dropdown['values'] = video_format_labels
    video_format_selection_dropdown.current(0)
    selected_format_index = video_format_selection_dropdown.current()
    selected_video_format = video_formats[selected_format_index]

    video.register_on_progress_callback(progress_function)
    video_format = video_formats[selected_format_index]
    video_format.download()
    Label(root, text='DOWNLOADED', font='Arial 15', fg='pale violet red').place(x=200, y=420)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percent
    root.update_idletasks()

# Download button
Button(root, text='DOWNLOAD', font='Arial 15 bold', bg='pale violet red', padx=2, command=Downloader).place(x=190, y=300)

root.mainloop()
