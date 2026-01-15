import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# UPDATE THIS PATH to the folder you want to track (e.g., Downloads)
TRACKED_FOLDER = "/Users/YourName/Downloads"

# Define where files should go based on extension
EXTENSION_MAP = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.pdf': 'Documents',
    '.txt': 'Documents',
    '.docx': 'Documents',
    '.exe': 'Installers',
    '.dmg': 'Installers',
    '.zip': 'Archives',
    '.mp4': 'Videos'
}

class OrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        # We only care about files, not folders
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        name, ext = os.path.splitext(filename)
        
        # Check if the extension is one we are tracking
        # Convert to lowercase to handle .JPG vs .jpg
        target_folder_name = EXTENSION_MAP.get(ext.lower())

        if target_folder_name:
            self.move_file(event.src_path, filename, target_folder_name)

    def move_file(self, src_path, filename, folder_name):
        # Create the full path for the destination folder
        dest_folder = os.path.join(TRACKED_FOLDER, folder_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            print(f"📁 Created folder: {folder_name}")

        dest_path = os.path.join(dest_folder, filename)

        # Move the file
        try:
            # Wait a split second to ensure the file is fully written 
            # (sometimes large downloads trigger the event before they finish)
            time.sleep(1) 
            shutil.move(src_path, dest_path)
            print(f"✅ Moved: {filename} -> {folder_name}/")
        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")

if __name__ == "__main__":
    event_handler = OrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, TRACKED_FOLDER, recursive=False)
    
    print(f"👀 Watching folder: {TRACKED_FOLDER}")
    print("Press Ctrl+C to stop...")
    
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Stopping observer")
    observer.join()