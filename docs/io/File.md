### File fundamentals

Here are the basic concepts that file operations build on: what a file is made of, what a file system is, and how paths and permissions are expressed. The read/write code in the chapters that follow all rests on these concepts.

#### 2.1 The concept of a file

A file is the basic unit of data storage. In a computer system, files are used to store data persistently. A file typically consists of the following parts:

- **File name**: The file's unique identifier. It can contain letters, digits, and special characters.
- **File extension**: Part of the file name, usually used to indicate the file's type (such as `.txt`, `.jpg`, `.pdf`).
- **File content**: The actual data stored in the file, which can be text, binary data, and so on.
- **File metadata**: Extra information describing the file, such as creation time, modification time, size, permissions, and so on.

The file system is responsible for managing files and their metadata. Different operating systems use different file systems (such as NTFS, FAT32, ext4), and each has its own characteristics and limitations.

#### 2.2 File system fundamentals

A file system is the structure an operating system uses to manage files and directories. It provides the mechanisms for storing and retrieving files and handles operations such as creating, deleting, reading from, and writing to files. Here are some common file system concepts:

- **Directory (folder)**: A container used to organize files. A directory can contain other directories (subdirectories) and files.
- **Path**: How a file's location in the file system is expressed. A path can be absolute (starting from the root directory) or relative (relative to the current directory).
- **Permissions**: A file's access control, including read, write, and execute permissions. Permission settings can restrict how different users or programs access a file.

#### 2.3 File operation fundamentals

There are roughly six file operations. Creating a file makes a new empty file; what happens when the file already exists is decided by the operating system and the language implementation. Opening a file requires specifying an access mode — read-only, write, and append are each one mode. Reading and writing both happen at the current position of the "file pointer," and the pointer advances after you're done reading or writing; when writing, you can either overwrite existing content or append to the end. Close the file when you're done so system resources are released; after closing, you can no longer read or write it. Deleting a file permanently removes it and its content from the file system.

#### 2.4 File paths and permissions

**File path**: A file path specifies where a file lives in the file system. Paths can be:

- **Absolute path**: The full path starting from the root of the file system, such as `/home/user/file.txt`.
- **Relative path**: A path relative to the current working directory, such as `file.txt` or `../file.txt`.

**File permissions**: File permissions control access to a file. Common permission settings include:

- **Read permission**: Allows the file content to be read.
- **Write permission**: Allows the file content to be modified or deleted.
- **Execute permission**: Allows the file to be executed (for executable programs).

File permissions can be set for:

- **Owner**: The permissions held by the file's owner.
- **Group**: The permissions held by users in the same group as the file's owner.
- **Others**: The permissions held by all other users.

On Unix and Linux systems, you can use the `chmod` command to change file permissions. For example:

```bash
chmod 644 file.txt
```

On Windows systems, you can change file permissions through the file properties dialog or the `icacls` command.

#### Summary

This section lays out the division of labor among file name, extension, and metadata; the difference between absolute and relative paths; and how the three permission types — read, write, execute — combine across the three Owner/Group/Others dimensions. The next chapter starts on actual read/write code.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [Example](/io/Example.md)
- [FileAdvanced](/io/FileAdvanced.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FileAdvanced](/io/FileAdvanced.md)
