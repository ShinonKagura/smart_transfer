import os
import threading
from tkinter import Tk, filedialog
from compression_manager import CompressionManager
from sender import SmartTransferSender
from receiver import SmartTransferReceiver

if __name__ == "__main__":
    Tk().withdraw()

    # Lade Plugins
    compression_manager = CompressionManager()
    compression_manager.load_plugins()

    # Zeige verfügbare Plugins
    print("Available compression methods:")
    plugins = compression_manager.list_plugins()
    for idx, plugin_name in enumerate(plugins, start=1):
        print(f"{idx}. {plugin_name}")

    choice = int(input("Select a compression method: ")) - 1
    if choice < 0 or choice >= len(plugins):
        print("Invalid choice. Exiting.")
        exit()

    compression_plugin = compression_manager.get_plugin(plugins[choice])

    # Datei auswählen
    print("Please select the file to process:")
    input_file_path = filedialog.askopenfilename(title="Select File")
    if not input_file_path:
        print("No file selected. Exiting.")
        exit()

    default_output_name = os.path.splitext(os.path.basename(input_file_path))[0] + "_compressed"
    print("Please select where to save the compressed file:")
    output_file_path = filedialog.asksaveasfilename(title="Save File As", defaultextension=".bin", initialfile=default_output_name)
    if not output_file_path:
        print("No output location selected. Exiting.")
        exit()

    # Komprimieren
    sender = SmartTransferSender(input_file_path, plugin=compression_plugin)
    sender.analyze_and_compress()
    sender.save_compression_data(output_file_path)

    print("Do you want to send the file now?")
    send_choice = input("Enter Y to send, or N to exit: ").lower()

    if send_choice == "y":
        receiver = SmartTransferReceiver(total_blocks=len(sender.blocks))
        sender.send(receiver)
        threading.Event().wait(1)
        receiver.request_missing_blocks(sender)
        threading.Event().wait(1)
        receiver.reconstruct_file(output_file_path, compression_plugin)

    print("Process completed.")