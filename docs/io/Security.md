### 文件与 IO 的安全性

文件与 IO 的安全性是确保数据完整性和防止未经授权访问的重要环节。本章将探讨文件权限、安全性、加密与解密、防止注入与篡改以及数据完整性验证等方面的内容。

#### 7.1 文件权限与安全

文件权限控制访问文件的权限，确保只有授权用户能够读取或修改文件。常见的文件权限包括读取、写入和执行权限。

**Go 示例代码**：

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

#### 7.2 加密与解密

加密是保护敏感数据的常用方法，防止数据被未经授权的用户访问。常见的加密算法包括对称加密和非对称加密。

**Go 示例代码**（对称加密示例）：

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

#### 7.3 防止注入与篡改

防止注入和篡改是确保文件和数据安全的关键。常见的方法包括对输入进行严格验证和使用安全的编码方法。

**Go 示例代码**（简单的输入验证示例）：

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

#### 7.4 数据完整性验证

数据完整性验证确保数据在传输或存储过程中没有被篡改。常用的方法包括校验和和数字签名。

**Go 示例代码**（使用 SHA-256 进行校验和验证）：

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

通过学习本章内容，读者将能够掌握文件权限控制、数据加密与解密、防止注入与篡改以及数据完整性验证等技术，从而在实际开发中确保文件与 IO 的安全性。