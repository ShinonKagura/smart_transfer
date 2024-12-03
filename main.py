import os
from tkinter import Tk, filedialog
from compression_manager import CompressionManager
from packer import Packer
from unpacker import Unpacker

def main():
    Tk().withdraw()

    # Lade Plugins
    compression_manager = CompressionManager()
    compression_manager.load_plugins()

    # Hauptmenü
    while True:
        print("\nAvailable operations:")
        print("1. Pack a file")
        print("2. Unpack a file")
        print("3. Transfer a file")
        print("4. Exit")
        choice = input("Select an operation: ")

        if choice == "1":
            handle_packing(compression_manager)
        elif choice == "2":
            handle_unpacking(compression_manager)
        elif choice == "3":
            handle_transfer(compression_manager)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def handle_packing(compression_manager):
    print("\nAvailable compression methods:")
    plugins = compression_manager.list_plugins()
    for idx, plugin_name in enumerate(plugins, start=1):
        print(f"{idx}. {plugin_name}")

    choice = int(input("Select a compression method: ")) - 1
    if choice < 0 or choice >= len(plugins):
        print("Invalid choice. Returning to main menu.")
        return

    plugin = compression_manager.get_plugin(plugins[choice])
    if not plugin:
        print("Selected plugin not available.")
        return

    print("\nPlease select the file to pack:")
    input_file = filedialog.askopenfilename(title="Select File")
    if not input_file:
        print("No file selected.")
        return

    print("Please select where to save the packed file:")
    output_file = filedialog.asksaveasfilename(title="Save Packed File As", defaultextension=".bin")
    if not output_file:
        print("No output location selected.")
        return

    packer = Packer(plugin)
    packer.pack_file(input_file, output_file)

def handle_unpacking(compression_manager):
    print("\nPlease select the file to unpack:")
    input_file = filedialog.askopenfilename(title="Select File")
    if not input_file:
        print("No file selected.")
        return

    print("Please select the output folder:")
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        print("No output folder selected.")
        return

    unpacker = Unpacker(compression_manager)
    unpacker.unpack_file(input_file, output_folder)

def handle_transfer(compression_manager):
    print("\nTransfer functionality will be implemented later.")
    # Hier kannst du die Transfer-Optionen ergänzen, wenn sie bereit sind.

if __name__ == "__main__":
    main()
