### Security


> Perspective: this page covers database access and SQL injection risks; for the broader official security stance see the [security and crypto notes](/security/Security.md), and for the file/IO side see the [IO security notes](/io/Security.md).
#### 12.1 Concepts of database security

Database security involves protecting the data in a database from unauthorized access, data leakage, tampering, and destruction. The main areas:

- **Access control**: limit access permissions to the database, so only authorized users can reach the data.
- **Data encryption**: protect data in transit and at rest, so it cannot be stolen or tampered with.
- **Defending against injection attacks**: prevent common attacks such as SQL injection to keep the data safe.
- **Regular backups**: back up the database on a schedule to avoid data loss.
- **Monitoring and auditing**: monitor database activity and record access logs so events can be traced and audited.

#### 12.2 Preventing SQL injection attacks

SQL injection is a common attack in which the attacker crafts malicious SQL statements to alter database queries, in order to gain unauthorized access or damage the data. The main ways to prevent it:

- **Use prepared statements**: prepared statements avoid SQL injection, because the query and the data are separated, so malicious code in the data is not executed.

##### Example: using prepared statements to prevent SQL injection
```go
func GetUserByEmail(db *sql.DB, email string) (*User, error) {
    stmt, err := db.Prepare("SELECT id, name, email FROM users WHERE email = ?")
    if err != nil {
        return nil, err
    }
    defer stmt.Close()

    row := stmt.QueryRow(email)
    user := new(User)
    err = row.Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        return nil, err
    }
    return user, nil
}

type User struct {
    ID    int
    Name  string
    Email string
}
```

- **Input validation**: validate user input strictly, so the data matches the expected format and range.

##### Example: simple input validation
```go
func validateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return errors.New("invalid email address")
    }
    return nil
}
```

- **Principle of least privilege**: ensure database users hold only the minimal permissions needed for their job, shrinking the potential attack surface.

#### 12.3 Data encryption

Data encryption protects data in transit and at rest, so it cannot be accessed or stolen without authorization. The main approaches:

- **Transport-layer encryption**: use SSL/TLS to encrypt the database connection, so data stays safe while it is in transit.

##### Example: configuring an SSL connection to MySQL
```go
package main

import (
    "crypto/tls"
    "database/sql"
    "log"

    "github.com/go-sql-driver/mysql"
)

func main() {
    dsn := "user:password@tcp(localhost:3306)/dbname?tls=custom"
    mysql.RegisterTLSConfig("custom", &tls.Config{
        InsecureSkipVerify: true,
        ServerName:         "localhost",
    })

    db, err := sql.Open("mysql", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}
```

- **Storage-layer encryption**: encrypt sensitive data before storing it in the database, so even if the data files are stolen, the data cannot be read.

##### Example: encrypting data with AES
```go
import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/hex"
    "io"
)

func encrypt(data, key string) (string, error) {
    block, err := aes.NewCipher([]byte(key))
    if err != nil {
        return "", err
    }

    ciphertext := make([]byte, aes.BlockSize+len(data))
    iv := ciphertext[:aes.BlockSize]
    if _, err := io.ReadFull(rand.Reader, iv); err != nil {
        return "", err
    }

    stream := cipher.NewCFBEncrypter(block, iv)
    stream.XORKeyStream(ciphertext[aes.BlockSize:], []byte(data))

    return hex.EncodeToString(ciphertext), nil
}

func decrypt(encrypted, key string) (string, error) {
    ciphertext, err := hex.DecodeString(encrypted)
    if err != nil {
        return "", err
    }

    block, err := aes.NewCipher([]byte(key))
    if err != nil {
        return "", err
    }

    iv := ciphertext[:aes.BlockSize]
    ciphertext = ciphertext[aes.BlockSize:]

    stream := cipher.NewCFBDecrypter(block, iv)
    stream.XORKeyStream(ciphertext, ciphertext)

    return string(ciphertext), nil
}
```

#### 12.4 Secure database access

Database access can be kept secure with the following measures:

- **Use strong passwords**: set complex, unique passwords for database users and change them regularly.
- **Restrict IP access**: use a firewall and database configuration to limit the range of IP addresses that can reach the database.
- **Enable audit logs**: record all database access and operation logs so activity can be monitored and audited.
- **Update and patch regularly**: update the database software and operating system on a schedule and apply security patches so known vulnerabilities cannot be exploited.

##### Example: restricting IP access for a MySQL user
```sql
CREATE USER 'user'@'192.168.1.100' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dbname.* TO 'user'@'192.168.1.100';
```

The single most important one is SQL injection: always use parameter placeholders in queries and never concatenate user input. Add the rest as needed: TLS in transit, encrypted storage for sensitive fields, accounts created with least privilege, and access recorded in the audit log.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [SQL](/db/SQL.md)
- [Sharding](/db/Sharding.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SQL](/db/SQL.md)
- [Sharding](/db/Sharding.md)
