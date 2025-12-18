# Duplicate File Hunter

A high-performance Python utility designed to detect and report duplicate files within complex directory structures. It employs a two-stage filtering process (Size grouping + MD5 Hashing) to ensure 100% accuracy while minimizing CPU and I/O usage.

## 🚀 Features

* **Two-Stage Algorithm:**
* **Fast Filter:** Groups files by byte size first (O(N) complexity), instantly eliminating unique files from further processing.
* **Precise Filter:** Generates MD5 hashes (Digital Fingerprints) *only* for potential duplicates, ensuring zero false positives.


* **Recursive Scanning:** deeply scans all sub-directories and nested folders using `os.walk`.
* **Memory Efficient:** Uses chunked reading (8KB buffers) to safely hash large files (e.g., 4GB movies) without consuming excessive RAM.
* **Robust Error Handling:** Gracefully handles permission errors, missing directories, and system files.
* **Cross-Platform:** Works on Linux, Windows, and macOS.

## 🛠️ Installation

No external dependencies are required. This script runs on standard Python 3.

```bash
# Clone the repository
git clone https://github.com/Ade20boss/file_twin.git

# Navigate to the directory
cd file_twin

```

## 📖 Usage

1. Open the script `deduplicator.py`.
2. Modify the function call at the bottom to point to the directory you want to scan:

```python
# At the bottom of duplicate_hunter.py
print(find_duplicate("/path/to/your/folder"))

```

3. Run the script:

```bash
python deduplicator.py

```

### Example Output

```text
Scanning /home/user/Downloads...
___________________
[DUPLICATE SET] Hash: 5d41402abc4b2a76b9719d911017c592 (Size: 1048576 bytes)
  -> /home/user/Downloads/image.png
  -> /home/user/Downloads/backup/image_copy.png

___________________
[DUPLICATE SET] Hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 (Size: 512 bytes)
  -> /home/user/Downloads/notes.txt
  -> /home/user/Documents/notes_final.txt

```

## 🧠 How It Works

This tool avoids the common performance pitfall of hashing every single file (which is slow). Instead, it uses a logic funnel:

1. **Validation:** It first verifies the directory exists and is accessible.
2. **Grouping (The "Lazy" Check):** It walks the tree and groups files into buckets based on their exact byte size.
* *Logic:* If File A is 100 bytes and File B is 100 bytes, they *might* be duplicates. If File C is 101 bytes, it is definitely unique and is ignored immediately.


3. **Hashing (The "Deep" Check):** It calculates the MD5 hash only for the buckets that contain more than one file.
4. **Reporting:** It compares the hashes. If the hashes match, the files are mathematically identical.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
