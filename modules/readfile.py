import os
import logging

def list_file_names_in_folder(folder_path):
    file_names = []
    try:
        # Iterate through all files in the folder
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                # Extract just the file name
                file_names.append(file_name)
    except FileNotFoundError:
        logging.error(f'Folder not found: {folder_path}')
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
    return file_names