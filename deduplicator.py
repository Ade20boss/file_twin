"""
Duplicate File Hunter
---------------------
A utility script to identify duplicate files within a directory tree.

Methodology:
1. Fast Filter: Groups files by file size. (O(N) complexity)
2. Slow Filter: Generates MD5 hashes only for files that share the same size.
   This avoids the expensive operation of hashing every single file.

Author: KernelGhost
"""

import os
import hashlib
import time

def file_hasher(file):
    """
    Generates an MD5 hash (digital fingerprint) for a specific file.
    
    Args:
        file (str): The full path to the file.
        
    Returns:
        str: The hexadecimal MD5 hash string, or None if the file cannot be read.
    """
    hasher = hashlib.md5()
    try:
        # Open file in 'rb' (Read Binary) mode to handle all file types (images, videos, text)
        # without encoding errors.
        with open(file, "rb") as f:
            
            # Read the file in small chunks (8KB) instead of loading the whole file into RAM.
            # This prevents memory crashes when hashing large files (e.g., 4GB movies).
            while chunk := f.read(8192):
                hasher.update(chunk)
               
        return hasher.hexdigest()
        
    except OSError:
        # Gracefully handle system errors (e.g., file locked by another process)
        print("An error occured while hashing a file.")
        return None

def find_duplicate(directory):
    """
    Scans a directory recursively to find duplicate files based on content.
    
    Args:
        directory (str): The root directory path to scan.
        
    Returns:
        list: A list of lists, where each inner list contains the paths of identical files.
    """
    print(f"\nScanning {directory}...")
    time.sleep(1)
    
    # --- PHASE 1: DIRECTORY VALIDATION ---
    # We attempt to list the directory first to catch common path errors
    # before starting the expensive scan operation.
    try:
        directory_entries = os.listdir(directory)
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' was not found.")
        exit()
    except NotADirectoryError:
        print(f"Error: '{directory}' is a file, not a directory.")
        exit()
    except PermissionError:
        print(f"Error: You do not have permission to access '{directory}'.")
        exit() 
    print("Directory scanned successfully.")
    
    # Dictionary to map { File Size (int) : [List of File Paths] }
    files_by_size = {}
    true_duplicates = []

    print("\nAnalyzing files by sizes...")
    time.sleep(1)
    # --- PHASE 2: GROUPING BY SIZE (FAST) ---
    # We walk the entire directory tree.
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                # Get file size in bytes
                file_size = os.path.getsize(full_path)
                
                # OPTIMIZATION: Skip empty files (0 bytes).
                # All empty files have the same hash, so they are technically duplicates,
                # but usually not relevant for cleanup.
                if file_size == 0:
                    continue
                
                # Group files. If we have seen this size before, add path to the list.
                # If not, create a new list entry.
                if file_size not in files_by_size:
                    files_by_size[file_size] = [full_path]
                else:
                    files_by_size[file_size].append(full_path)
            except OSError:
                # Skip files we cannot access/read stats for
                continue
    print("Size analysis complete")

    # --- PHASE 3: VERIFYING HASHES (SLOW) ---
    duplicates_found = False
    
    print("\nProceeding to verifying potential duplicates by hashing...")
    print("This may take a while depending on the number and size of files...")
    time.sleep(1)
    # Iterate through our size groups.
    for size, paths in files_by_size.items():
        
        # LOGIC CHECK: We only need to check hashes if there is more than 1 file 
        # with this specific size. If there's only 1 file, it cannot be a duplicate.
        if len(paths) > 1:
            
            # Mini-dictionary for this specific size group: { MD5 Hash : [List of Paths] }
            files_by_hash = {}
            print("Hashing files")
            time.sleep(1)
            for path in paths:
                file_hash = file_hasher(path)
                
                if file_hash:
                    # Group by content hash
                    if file_hash not in files_by_hash:
                        files_by_hash[file_hash] = [path]
                    else:
                        files_by_hash[file_hash].append(path)
            print("Hashing complete")


            print("\nChecking for duplicates...")
            time.sleep(1)
            print("___________________")           
            # Check the hash groups to identify True Duplicates
            for file_hash, file_list in files_by_hash.items():
                if len(file_list) > 1:
                    duplicates_found = True
                    true_duplicates.append(file_list)     
                    
                    # Print result immediately for user feedback
                    print(f"___________________")
                    print(f"[DUPLICATE SET] Hash: {file_hash} (Size: {size} bytes)")
                    for p in file_list:
                        print(f"  -> {p}")
    print("Duplicate verification complete.")
    
    # --- PHASE 4: REPORTING ---
    if not duplicates_found:
        print("No duplicate files found.")
        return []
        
    return true_duplicates
   
# Example Usage:
if __name__ == "__main__":
    scan_path = input("Enter file path: ")
    print(find_duplicate(scan_path))
