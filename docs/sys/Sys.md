System programming means developing and maintaining software at the level of the computer system: operating system kernels, device drivers, file systems, network protocol stacks, system tools. It sits close to the hardware and the operating system, and is usually written in low-level languages such as C or assembly.

Below is a brief introduction to the three common operating systems: Windows, Linux, and macOS.

### Windows
#### Overview
- **Developer**: Microsoft Corporation
- **Kernel type**: hybrid kernel
- **Main languages**: C, C++, C#

#### Features
- **Graphical user interface (GUI)**: Windows is known for its friendly graphical user interface, where users operate through icons and menus.
- **Scope of use**: in use on personal computers in homes, businesses, and schools.
- **Software compatibility**: a large number of third-party applications and games, most of which can be installed and used directly.
- **Development tools**: provides integrated development tools such as Visual Studio for building Windows applications.

#### Core components
- **NT kernel**: the core component of Windows, providing memory management, process management, file system, and networking.
- **Win32 API**: the application interface for developers to build Windows applications.
- **File system**: uses the NTFS (New Technology File System) file system, providing efficient, secure data storage and retrieval.

### Linux
#### Overview
- **Developer**: originally developed by Linus Torvalds, now maintained collaboratively by the global community
- **Kernel type**: monolithic kernel
- **Main languages**: C, C++

#### Features
- **Open source**: Linux is open source; users are free to modify and distribute its source code.
- **Variety**: many distributions exist (Ubuntu, Fedora, Debian, for example), so users can pick the version that fits.
- **Security and stability**: owing to its open-source nature, its security and stability are widely recognized, and it is often used in servers and development environments.
- **Package managers**: each distribution has its own package manager (apt, yum, for example), making software installation and management convenient.

#### Core components
- **Linux kernel**: provides the low-level hardware abstraction layer, process management, memory management, and network stack.
- **GNU toolchain**: includes the compiler, debugger, and other development tools, and is the foundation of Linux systems.
- **File system**: supports multiple file systems such as ext4, Btrfs, and XFS, providing flexible data storage solutions.

### macOS
#### Overview
- **Developer**: Apple Inc.
- **Kernel type**: hybrid kernel (based on the XNU kernel)
- **Main languages**: Objective-C, Swift

#### Features
- **Paired with Apple hardware**: the system is tightly integrated with Apple hardware, giving a consistent user experience.
- **Graphical user interface**: menus and window operations, easy to pick up.
- **Development tools**: provides the Xcode integrated development environment (IDE), supporting the Objective-C and Swift languages, widely used for building macOS and iOS applications.
- **Unix foundation**: macOS is Unix-based, with a complete set of command-line tools, so the development environment is usable as is.

#### Core components
- **XNU kernel**: combines the Mach microkernel and the BSD subsystem, providing efficient memory and process management.
- **File system**: uses APFS (Apple File System), providing fast, secure file storage and retrieval.
- **Cocoa framework**: an object-oriented application framework for developers to build macOS applications.

### Comparison
- **Windows**: suited to personal and commercial use, with broad software support and a friendly user interface.
- **Linux**: suited to servers and development environments; open source, stable, and secure, with many distributions to choose from.
- **macOS**: suited to Apple hardware users, paired with the Xcode development toolset.

Choice depends on use: Windows for desktop and commercial software, Linux for servers and development environments, macOS for building applications on Apple hardware.

## References

- [syscall standard library](https://pkg.go.dev/syscall)
- [os standard library](https://pkg.go.dev/os)

## Sibling pages

- [Plugin](/sys/Plugin.md)
- [Syscall](/sys/Syscall.md)
- [Unsafe](/sys/Unsafe.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Plugin](/sys/Plugin.md)
- [Syscall](/sys/Syscall.md)
- [Unsafe](/sys/Unsafe.md)
