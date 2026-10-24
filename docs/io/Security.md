### File and IO Security


> Perspective: this page discusses file permissions and IO input/output risks; for the official Go security line see the [security and crypto notes](/zh/security/Security.md), and for database risks see the [database security notes](/db/Security.md).
File and IO security comes down to two things: keeping data away from unauthorized readers, and keeping data from being tampered with in transit or storage. Four sections follow: file permissions, encryption and decryption, injection and tampering prevention, and integrity verification.

#### 7.1 File Permissions and Security

File permissions decide who can read or modify a file; the common ones are read, write, and execute.

**Go example code**:

```go
package main

import (
    "fmt"
    "os"
)

func checkPermissions(filePath string) {
    fileInfo, err := os.Stat(filePath)
    if err != nil {
        fmt.Println("Error getting file info:", err)
        return
    }

    mode := fileInfo.Mode()
    fmt.Printf("File permissions: %v\n", mode)
}

func setPermissions(filePath string, mode os.FileMode) {
    err := os.Chmod(filePath, mode)
    if err != nil {
        fmt.Println("Error setting file permissions:", err)
        return
    }

    fmt.Println("File permissions updated successfully")
}

func main() {
    filePath := "example.txt"
    checkPermissions(filePath)
    setPermissions(filePath, 0644)
    checkPermissions(filePath)
}
```

#### 7.2 Encryption and Decryption

Encryption is a common way to protect sensitive data and keep it away from unauthorized users. Common algorithms include symmetric and asymmetric encryption.

**Go example code** (symmetric encryption example):

```go
package main

import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/base64"
    "fmt"
    "io"
)

func encrypt(data, key []byte) (string, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return "", err
    }

    ciphertext := make([]byte, aes.BlockSize+len(data))
    iv := ciphertext[:aes.BlockSize]
    if _, err := io.ReadFull(rand.Reader, iv); err != nil {
        return "", err
    }

    stream := cipher.NewCFBEncrypter(block, iv)
    stream.XORKeyStream(ciphertext[aes.BlockSize:], data)

    return base64.URLEncoding.EncodeToString(ciphertext), nil
}

func decrypt(encrypted string, key []byte) (string, error) {
    ciphertext, _ := base64.URLEncoding.DecodeString(encrypted)

    block, err := aes.NewCipher(key)
    if err != nil {
        return "", err
    }

    iv := ciphertext[:aes.BlockSize]
    ciphertext = ciphertext[aes.BlockSize:]

    stream := cipher.NewCFBDecrypter(block, iv)
    stream.XORKeyStream(ciphertext, ciphertext)

    return string(ciphertext), nil
}

func main() {
    key := []byte("mysecretpasswordmysecretpassword") // 32 bytes for AES-256
    plaintext := "Hello, secure world!"

    encrypted, err := encrypt([]byte(plaintext), key)
    if err != nil {
        fmt.Println("Error encrypting data:", err)
        return
    }
    fmt.Println("Encrypted:", encrypted)

    decrypted, err := decrypt(encrypted, key)
    if err != nil {
        fmt.Println("Error decrypting data:", err)
        return
    }
    fmt.Println("Decrypted:", decrypted)
}
```

#### 7.3 Preventing Injection and Tampering

Preventing injection and tampering rests on two things: validate input strictly, and use battle-tested approaches for encoding.

**Go example code** (a simple input validation example):

```go
package main

import (
    "fmt"
    "regexp"
)

func validateFileName(fileName string) bool {
    validName := regexp.MustCompile(`^[a-zA-Z0-9_\-\.]+$`)
    return validName.MatchString(fileName)
}

func main() {
    fileName := "example.txt"
    if validateFileName(fileName) {
        fmt.Println("File name is valid")
    } else {
        fmt.Println("File name is invalid")
    }
}
```

#### 7.4 Data Integrity Verification

Data integrity verification ensures data has not been tampered with in transit or storage. Common methods include checksums and digital signatures.

**Go example code** (checksum verification with SHA-256):

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "io"
    "os"
)

func calculateChecksum(filePath string) (string, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return "", err
    }
    defer file.Close()

    hasher := sha256.New()
    if _, err := io.Copy(hasher, file); err != nil {
        return "", err
    }

    return hex.EncodeToString(hasher.Sum(nil)), nil
}

func main() {
    filePath := "example.txt"
    checksum, err := calculateChecksum(filePath)
    if err != nil {
        fmt.Println("Error calculating checksum:", err)
        return
    }

    fmt.Printf("SHA-256 checksum: %s\n", checksum)
}
```

The four snippets map to four tasks: `os.Chmod` sets permissions, AES-CFB encrypts and decrypts, the regex validates file names, and SHA-256 computes a checksum — all runnable as-is.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [ModPath](/io/ModPath.md)
- [Utils](/io/Utils.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ModPath](/io/ModPath.md)
- [Utils](/io/Utils.md)
