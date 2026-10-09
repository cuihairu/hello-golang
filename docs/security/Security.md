# 官方安全口径与 `crypto` 标准库

官方把安全单列成 Why Go 下的一个板块，标题是 How Go can help keep you secure by default。本仓此前没有任何 `crypto/` 相关内容，这一页把官方口径抄下来并给出后续阅读入口。抓取于 2026-10-08。

## 一、官方列的四件事

1. **漏洞库**：Go Vulnerability Database（Go 漏洞数据库），可以浏览报告、查文档，也可以公开提交漏洞。安全策略页（Security Policy）写明安全团队怎么跟踪问题、怎么对公众披露，并指向发布历史里的安全修复记录。
2. **修复范围**：按发布策略，安全修复发到**最近两个大版本**。这条与 `docs/introduction/ReleaseNotes.md` 里的支持策略是同一条。
3. **fuzzing**：用自动测试不断变换输入来找 bug，Go 从 **1.18** 起在标准工具链里内置原生 fuzzing，原生 fuzz 测试被 OSS-Fuzz 支持。
4. **加密库**：官方说 Go 的加密库目标是帮开发者构建安全应用，入口是标准库的 `crypto` 包和 `golang.org/x/crypto/`；此外 Go 的加密库可以在 **FIPS 140-3 合规模式**下使用，面向有合规要求的环境。

## 二、和应用相关的 `crypto` 包怎么找

标准库包文档是 pkg.go.dev 上的 `crypto` 分组，`golang.google.cn/pkg/` 也能直接打开。按用途分：

| 用途 | 包 |
| --- | --- |
| 传输加密 | `crypto/tls`（HTTPS 的底层）、`crypto/x509`（证书） |
| 摘要 | `crypto/sha256`、`crypto/sha512`、`crypto/md5`（只用于校验旧数据，不用于安全场景） |
| 消息认证与对称加密 | `crypto/hmac`、`crypto/aes`、`crypto/chacha20poly1305` |
| 非对称与签名 | `crypto/rsa`、`crypto/ecdsa`、`crypto/ed25519`、`crypto/rand` |
| 随机数 | `crypto/rand`（密钥、token 必须用它，不能用 `math/rand`） |

`docs/math/MathRand.md` 讲的 `math/rand` 是可复现的伪随机数，适合打散与模拟；密钥、nonce、token 一律走 `crypto/rand`，两者不要混。

## 三、本仓已有的相关页面

| 页面 | 覆盖到哪 |
| --- | --- |
| `docs/io/Security.md` | 文件与输入输出侧的安全做法 |
| `docs/db/Security.md` | 数据库侧，含防 SQL 注入 |
| `docs/net/Socket.md` | 底层 socket，TLS 在其之上 |
| `docs/encoding/Base64.md`、`docs/encoding/Hex.md` | 编码，不是加密 |

缺口是 `crypto/tls` 服务端配置、证书与握手这块，本页只给入口，不展开：展开需要官方 `crypto/tls` 包文档支撑，这次调研没取到足够的原文。

## 四、依赖侧的注意点

官方漏洞库查的是 Go 标准库与已收录的模块。本仓页面里出现的第三方库（Gin、gORM、Kafka 客户端等）不在标准库范围内，升级前用 `govulncheck` 这类工具对着自己的依赖图跑一遍，结论以工具输出为准。

## 来源

1. https://golang.google.cn/security/ — 官方安全页：漏洞数据库、安全策略、两个大版本的修复范围、fuzzing、加密库与 FIPS 140-3（2026-10-08 抓取）
2. https://golang.google.cn/doc/fuzz/ — 原生 fuzzing 起于 Go 1.18、OSS-Fuzz 支持
3. https://golang.google.cn/doc/devel/release — 发布策略中的安全修复范围
4. https://golang.google.cn/pkg/ — 标准库包文档入口
