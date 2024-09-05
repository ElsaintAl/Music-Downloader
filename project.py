from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import TclError

from pytube import YouTube
from pytube.exceptions import PytubeError, ExtractError

import configparser
from configparser import NoOptionError, NoSectionError

import os


# The main function that starts the program
def main():
    create_config_file('config.txt')
    set_root(280, 220)
    main_page()
    root.mainloop()


def set_root(width, height):
    """Creates the settings for the Gui"""

    global root
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    root.title("YouTube Music Downloader")
    root.config(background="PaleGreen1")


# GUI for main menu
def main_page():
    """4 OPTIONS: Music Page, Lyrics Page, Info message box, Exit  """

    # Create labels and buttons for the first page
    head_label = Label(root, text="YouTube Music\nDownloader", padx=10, pady=10,
                       font=("SegoeUI 14 bold", 18), bg="palegreen1", fg="red")
    head_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    get_song = Button(root, text='Get Song', bg="salmon", pady=13, padx=15,
                      command=lambda: [root.destroy(), music_page()])  # Call song download page function
    get_song.place(relx=0.25, rely=0.5, anchor=CENTER)

    get_lyrics = Button(root, text='Get Lyrics', bg="salmon", pady=13, padx=15,
                        command=lambda: [root.destroy(), lyrics_page()])  # Call lyrics download page function
    get_lyrics.place(relx=0.75, rely=0.5, anchor=CENTER)

    info = Button(root, text='Info', bg="salmon", pady=13, padx=31, command=lambda: information())
    info.place(relx=0.25, rely=0.8, anchor=CENTER)

    close_main_page = Button(root, text='Exit', bg="salmon", pady=13, padx=31,
                             command=root.destroy)  # Call lyrics download page function
    close_main_page.place(relx=0.75, rely=0.8, anchor=CENTER)


# GUI for  music page
def music_page():
    """3 Bars: Song w/o youtube-link,
               youtube-link and download path
       4 Buttons: Browse (sets download path),
                  Song List (new page for song list search),
                  Download Music and Back (Returns to Main Page)
    """

    set_root(530, 280)

    song_name = StringVar()
    video_link = StringVar()
    download_path = StringVar()

    head_label = Label(root, text="YouTube Music Downloader", padx=15, pady=15,
                       font="SegoeUI 14 bold", bg="palegreen1", fg="red")
    head_label.grid(row=1, column=1, pady=10, padx=5, columnspan=3)

    song_label = Label(root, text='Song by Artist:', bg='salmon', pady=5, padx=5)
    song_label.grid(row=2, column=0, pady=5, padx=5)
    root.songText = Entry(root, width=35, borderwidth=3, textvariable=song_name, font="Arial 14")
    root.songText.grid(row=2, column=1, pady=5, padx=5, columnspan=2)

    link_label = Label(root, text="YouTube link :", bg="salmon", pady=5, padx=5)
    link_label.grid(row=3, column=0, pady=5, padx=5)
    root.linkText = Entry(root, width=35, borderwidth=3, textvariable=video_link, font="Arial 14")
    root.linkText.grid(row=3, column=1, pady=5, padx=5, columnspan=2)

    destination_label = Label(root, text="Destination :", bg="salmon", pady=5, padx=9)
    destination_label.grid(row=4, column=0, pady=5, padx=5)
    root.destinationText = Entry(root, width=27, borderwidth=3, textvariable=download_path, font="Arial 14")
    root.destinationText.grid(row=4, column=1, pady=5, padx=5)

    browse_B = Button(root, text="Browse", command=lambda: browse_download_folder(download_path),
                      width=10, bg="bisque", relief=GROOVE)
    browse_B.grid(row=4, column=2, pady=1, padx=1)

    song_list = Button(root, text="Song List", width=10, bg='plum1',
                       command=lambda: [root.destroy(), list_of_songs()])
    song_list.grid(row=5, column=0, pady=20, padx=20)

    Download_B = Button(root, text="Download Music", width=20, bg="plum1",
                        command=lambda: [song_download(song_name, video_link, download_path),
                                         root.destroy(), music_page()],
                        pady=10, padx=15, relief=GROOVE, font="Georgia, 13")
    Download_B.grid(row=5, column=1, pady=20, padx=20)

    back = Button(root, text='Back', bg="thistle1", pady=6, padx=6,
                  command=lambda: [root.destroy(), main()])  # Call lyrics download page function
    back.place(relx=0.86, rely=0.86, anchor=CENTER)

    root.mainloop()


# GUI the list of songs from a specific folder
def list_of_songs():
    """ 2-Buttons: Browse Directory (Directory to be searched) and Back (Returns to Music Page)
        A treeview for list for songs
        A specific browse function that incorporates the treeview and a function for searching
        and putting into a list the available songs
    """

    def browse_directory():
        folder_path = filedialog.askdirectory()
        if folder_path:
            current_dir.set(folder_path)
            list_files(folder_path)

    def list_files(folder_path):
        for item in tree_view.get_children():
            tree_view.delete(item)

        for filename in os.listdir(folder_path):
            if '.mp3' in filename:
                if os.path.isfile(os.path.join(folder_path, filename)):
                    tree_view.insert("", "end", values=(filename,))

    set_root(210, 310)

    current_dir = tk.StringVar()

    browse_button = tk.Button(root, text="Browse Directory", command=lambda: [browse_directory()],
                              width=15, bg="bisque", relief=GROOVE)
    browse_button.grid(row=1, column=0, padx=3, pady=5)

    back_button = tk.Button(root, text='Back', command=lambda: [root.destroy(), music_page()])
    back_button.grid(row=1, column=1, )

    folder_label = tk.Label(root, textvariable=current_dir, bg="salmon")
    folder_label.grid(row=2, columnspan=2, padx=5, pady=5)

    tree_view = ttk.Treeview(root, columns=("Files",), show="headings", selectmode="browse", )
    tree_view.heading("Files", text="Files in Directory", )
    tree_view.grid(row=3, column=0, columnspan=2, padx=4, pady=0.5)
    root.mainloop()


# GUI for lyric page
def lyrics_page():
    """ 2 Bars: Song and download path
        3 Buttons: Browse (sets download path), Download Lyrics and Back (Returns to Main Page)
    """

    set_root(520, 240)

    song_name = StringVar()
    download_path = StringVar()

    head_label = Label(root, text="Lyrics Downloader", padx=15, pady=15,
                       font=("SegoeUI 14 bold", 18), bg="palegreen1", fg="red")
    head_label.grid(row=1, column=0, pady=10, padx=5, columnspan=3)

    song_label = Label(root, text='Song by Artist:', bg='salmon', pady=5, padx=5)
    song_label.grid(row=2, column=0, pady=5, padx=5)
    root.songText = Entry(root, width=35, borderwidth=3, textvariable=song_name, font="Arial 14")
    root.songText.grid(row=2, column=1, pady=5, padx=5, columnspan=2)

    destination_label = Label(root, text="Destination :", bg="salmon", pady=5, padx=9)
    destination_label.grid(row=4, column=0, pady=5, padx=5)
    root.destinationText = Entry(root, width=27, borderwidth=3, textvariable=download_path, font="Arial 14")
    root.destinationText.grid(row=4, column=1, pady=5, padx=5)

    browse_B = Button(root, text="Browse", command=lambda: browse_download_folder(download_path),
                      width=10, bg="bisque", relief=GROOVE)
    browse_B.grid(row=4, column=2, pady=1, padx=1)
    Download_B = Button(root, text="Download Lyrics", width=20, bg="thistle1",
                        command=lambda: [lyrics_download(download_path, song_name),
                                         root.destroy(), lyrics_page()],
                        pady=10, padx=15, relief=GROOVE, font="Georgia, 13")
    Download_B.grid(row=5, column=1, pady=20, padx=20)

    back = Button(root, text='Back', bg="thistle1", pady=6, padx=6,
                  command=lambda: [root.destroy(), main()])  # Call lyrics download page function
    back.place(relx=0.86, rely=0.86, anchor=CENTER)

    root.mainloop()


# Sets the downloading directory path
def browse_download_folder(download_path):
    """The browse function for the Music and Lyrics page"""

    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Location")
    download_path.set(download_Directory)


# Downloads the lyrics of a song
# It can be improved further
def lyrics_download(download_path, song_name):
    """ Downloads the Lyrics with a specific name format (Artist - Song) in a .txt file
        to the chosen directory
    """

    if not download_path.get():
        messagebox.showerror("Error", "Please specify the download path.")
        return "MISSING_DOWNLOAD_PATH"
    elif not song_name.get():
        messagebox.showerror("Error", "Please specify the song.")
        return "MISSING_SONG_NAME"

    download_Folder = download_path.get()
    content, file_name = get_lyrics(song_name.get())

    if content is None:
        messagebox.showerror("Error", "Lyrics could not be found.")
        return 'LYRICS_NOT_FOUND_ERROR'

    name = f"{file_name}.txt"
    file1 = open(f"{download_Folder}/{name}", "w")
    file1.write(content)
    file1.close()
    messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + download_Folder)


# Finds the lyrics with selenium from https://www.azlyrics.com
# If the site changes it will cause problems
def get_lyrics(lyrics):
    """ Opens the https://www.azlyrics.com with Chrome WebDriver
        and returns the lyrics and the name of the file
    """

    try:
        driver = driver_initialization()
        driver.minimize_window()
        driver.get('https://www.azlyrics.com')
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

        search_1 = driver.find_element(By.CSS_SELECTOR, '#q')
        search_1.clear()
        search_1.send_keys(lyrics)
        search_1.send_keys(Keys.RETURN)

        search_2_xpath = (
            '/html/body/div[2]/div/div/div[1]/table/tbody/tr/td'
        )
        search_2 = driver.find_element(By.XPATH, search_2_xpath)
        search_2.click()

        artist_xpath = (
            '/html/body/div[2]/div[2]/div[2]/div[3]/h2/a/b'
        )
        artist = driver.find_element(By.XPATH, artist_xpath).text

        song_xpath = (
            '/html/body/div[2]/div[2]/div[2]/b'
        )
        song = driver.find_element(By.XPATH, song_xpath).text

        file_name = artist.replace(' Lyrics', '') + ' - ' + song.replace('"', '')

        content_xpath = (
            '/html/body/div[2]/div[2]/div[2]/div[5]'
        )

        try:
            content = driver.find_element(By.XPATH, content_xpath).text
        except NoSuchElementException:
            messagebox.showinfo('Error:', f"Lyrics not found for {lyrics}")
            return None, None

        return content, file_name
    except TimeoutException as e:
        messagebox.showinfo('Error:', f"Page load timed out: {str(e)}")
    except NoSuchElementException as e:
        messagebox.showinfo('Error:', f"Element not found: {str(e)}")
    except WebDriverException as e:
        messagebox.showinfo('Error:', f"Error using WebDriver: {str(e)}")  # Log the error
        return None, None  # Return empty values to indicate failure

    finally:
        if driver:
            driver.quit()


# Checks if the song already exists in the current folder and
# downloads the song if it doesn't
# It can be improved further
def song_download(song_name, video_link, download_path):
    """ Downloads a mp3 from the given youtube-link
        if the song doesn't already exist on the download folder
    """

    if not download_path.get():
        messagebox.showerror("Error", "Please specify the download path.")
        return "MISSING_DOWNLOAD_PATH"

    # Create YouTube object and filter for audio-only streams depending on the user input
    if not video_link.get() and not song_name.get():
        messagebox.showerror("Error", "Please specify either the song or the youtube link for the song.")
        return "MISSING_SONG"
    elif not video_link.get():
        youtube_object = YouTube(get_link(song_name.get()))
    else:
        youtube_object = YouTube(video_link.get())

    # select the optimal location for saving file's
    download_folder = download_path.get()
    audio_stream = youtube_object.streams.filter(only_audio=True).first()

    # Set up the name
    file_name = f'\\{youtube_object.author} - {youtube_object.title}.mp3'
    new_file = f'{download_folder}' + file_name

    os.chdir(download_path.get())
    try:
        if file_name[1:] in os.listdir():
            messagebox.showinfo('Info', 'The song already exists')
        else:
            # Downloading the video to destination directory
            out_file = audio_stream.download(download_folder)
            # save the file to mp3
            os.rename(out_file, new_file)
            # Displaying the message
            messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + download_folder)

    except ExtractError as e:
        messagebox.showerror("Download Error", f"Error downloading the song: {str(e)}")
    except OSError as e:
        messagebox.showerror("Error", f"Error saving the file: {str(e)}")
    except EXCEPTION as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# Finds the youtube-link if not link was given
def get_link(song_name):
    """ Opens the https://www.youtube.com/results?search_query={song_name} with Chrome WebDriver
            and returns the first youtube-link
    """

    driver = driver_initialization()
    driver.minimize_window()
    driver.get(f'https://www.youtube.com/results?search_query={song_name}')
    driver.implicitly_wait(5)

    try:
        link_webelement = driver.find_element(By.CSS_SELECTOR,
                                              'div#contents ytd-item-section-renderer>div#contents a#thumbnail')
        link = link_webelement.get_attribute('href')
    except NoSuchElementException:
        messagebox.showinfo('Error:', "No Youtube-link found for the given song name")
        return None

    driver.quit()
    return link


# Initializes the Chrome WebDriver with options
def driver_initialization():
    def get_chromedriver_path():
        """
        Gets the path of the chromedriver executable from a configuration file.
        """
        config = configparser.ConfigParser()
        try:
            config.read('config.txt')
            return config.get('chromedriver', 'path')
        except (FileNotFoundError, NoSectionError, NoOptionError) as e:
            messagebox.showinfo('Error', f"Error reading configuration file: {str(e)}")
            return None

    chromedriver_path = get_chromedriver_path()
    if chromedriver_path:
        try:
            service = Service(executable_path=chromedriver_path)
            options = Options()
            options.add_argument('start-maximized')
            options.add_argument('disable-infobars')
            options.add_argument('disable-search-engine-choice-screen')

            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except WebDriverException as e:
            messagebox.showinfo('Error', f"Error initializing WebDriver: {str(e)}")
    else:
        messagebox.showinfo('Error', "Please set the CHROME_DRIVER_PATH environment variable "
                                     "to the path of your chromedriver executable.")


def create_config_file(file_path):
    """Creates a configuration file with user input for the chromedriver path.

    Args:
        file_path (str): The path to the configuration file.
    """

    try:
        if not os.path.exists(file_path):
            root = tk.Tk()
            root.title()
            root.geometry('490x50')
            root.title("YouTube Music Downloader")

            user_input = tk.StringVar(root)

            def get_path():
                path = user_input.get()
                return path

            entry = tk.Entry(root, textvariable=user_input, width=450)
            entry.pack()
            # Pass the function itself as the command argument
            check = tk.Button(root, text='Path', command=lambda: [get_path(), root.destroy()])
            check.pack()
            root.mainloop()

            if get_path():
                with open(file_path, 'w') as f:
                    f.write(f'[chromedriver]\npath = {get_path()}')
            else:
                messagebox.showinfo('Error', f"Path is missing")

    except TclError as e:
        messagebox.showinfo('Error', f"Window closed without entering path: {e}")


# The information box
# I could write more
def information():
    messagebox.showinfo("Credits to Elsaint Aligiai", f"Work in progress")


if __name__ == "__main__":
    main()
