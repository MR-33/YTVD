import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import os
import threading


def download_video():
    video_url = url_entry.get().strip()
    if not video_url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return

    quality = quality_var.get()
    download_button.config(state="disabled", text="Downloading...")
    # Perform download in a separate thread
    threading.Thread(target=perform_download, args=(video_url, quality)).start()


def perform_download(video_url, quality):
    try:
        # Set download options based on quality selection
        if quality == "Highest":
            format_opt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif quality == "1080p":
            format_opt = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best'
        elif quality == "720p":
            format_opt = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'
        else:  # 480p
            format_opt = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'

        ydl_opts = {
            'format': format_opt,
            'outtmpl': os.path.join(os.path.expanduser("~/Downloads"), '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'video')

            # Update status label
            root.after(0, lambda: status_label.config(
                text=f"Downloading: {title}...",
                fg="blue"
            ))

            # Download video
            ydl.download([video_url])

            # Show success message
            root.after(0, lambda: status_label.config(
                text=f"Successfully downloaded: {title}",
                fg="green"
            ))
            messagebox.showinfo("Success", f"Video '{title}' downloaded successfully!")

    except Exception as e:
        root.after(0, lambda: status_label.config(
            text="Download failed!",
            fg="red"
        ))
        messagebox.showerror("Error", f"Download failed.\n{e}")
    finally:
        root.after(0, lambda: download_button.config(state="normal", text="Download"))


# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x300")

# URL Entry
tk.Label(root, text="Enter YouTube URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=50, font=("Arial", 10))
url_entry.pack(pady=5)

# Quality Selection
quality_frame = tk.Frame(root)
quality_frame.pack(pady=10)
tk.Label(quality_frame, text="Quality:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
quality_var = tk.StringVar(value="Highest")
quality_choices = ["Highest", "1080p", "720p", "480p"]
quality_menu = ttk.Combobox(quality_frame, textvariable=quality_var, values=quality_choices, state="readonly", width=10)
quality_menu.pack(side=tk.LEFT)

# Download Button
download_button = tk.Button(root, text="Download", font=("Arial", 12), command=download_video)
download_button.pack(pady=20)

# Status Label
status_label = tk.Label(root, text="Ready to download", font=("Arial", 10))
status_label.pack(pady=10)

# Run the application
root.mainloop()
