# 术语表

本仓核心术语的中英对照、一句话定义与权威出处。出处均为官方文档、官方博客、语言规范或原论文，逐条可点；未能找到权威出处的条目如实标注。相关页链接指向本仓正文。

## 并发与运行时

### Goroutine（Go 协程）
轻量级执行单元，由 Go 运行时调度而非操作系统线程，初始栈很小、可大量并存。
**出处**：[语言规范 · Go 语句](https://go.dev/ref/spec#Go_statements)、[Effective Go · Goroutines](https://go.dev/doc/effective_go#goroutines)
**相关页**：[Goroutine](/concurrency/Goroutine.md)、[GoroutineImpl](/concurrency/GoroutineImpl.md)

### GMP 调度模型
Go 运行时调度器的抽象：G（goroutine）、M（机器线程）、P（处理器，持有可运行 G 队列）。
**出处**：[官方 · Go 调度器设计文档（golang.org/s/go11sched）](https://golang.org/s/go11sched)
**相关页**：[GMP](/concurrency/GMP.md)、[Runtime](/sync/Runtime.md)

### Channel（通道）
带类型的并发安全管道，可在 goroutine 之间收发值；无缓冲通道收发双方同步会合。
**出处**：[语言规范 · 通道类型](https://go.dev/ref/spec#Channel_types)、[Go 内存模型 · 通道](https://go.dev/ref/mem#chan)、[Effective Go · Channels](https://go.dev/doc/effective_go#channels)
**相关页**：[Chan](/concurrency/Chan.md)、[ChanImpl](/concurrency/ChanImpl.md)

### Select
多路等待多个通道操作的控制结构，可就绪的分支中随机选择一个执行。
**出处**：[语言规范 · Select 语句](https://go.dev/ref/spec#Select_statements)
**相关页**：[Select](/concurrency/Select.md)

### CSP（通信顺序进程）
Tony Hoare 提出的并发模型，Go 的并发设计哲学来源：「不要通过共享内存来通信，而要通过通信来共享内存」。
**出处**：[Hoare 1978 原论文（CACM，DOI）](https://dl.acm.org/doi/10.1145/359576.359585)、[CSP 概览 · Wikipedia](https://en.wikipedia.org/wiki/Communicating_sequential_processes)
**相关页**：[CSP](/concurrency/CSP.md)、[Actor](/concurrency/Actor.md)

### 数据竞争（Data Race）
两个 goroutine 并发访问同一内存位置、至少一个是写、且没有同步协调——行为未定义。
**出处**：[Go 内存模型](https://go.dev/ref/mem)、[官方博客 · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
**相关页**：[RaceCondition](/sync/RaceCondition.md)

### Go 内存模型（Memory Model）
规定一个 goroutine 能否观察到另一个 goroutine 写入的值，核心是 happens-before 关系。
**出处**：[Go 内存模型](https://go.dev/ref/mem)
**相关页**：[MemoryModel](/gc/MemoryModel.md)、[MemorySynchronization](/sync/MemorySynchronization.md)

### Happens-before
内存模型中的偏序关系：若 A happens-before B，则 A 的写对 B 可见。
**出处**：[Go 内存模型](https://go.dev/ref/mem)
**相关页**：[MemoryModel](/gc/MemoryModel.md)

### Mutex（互斥锁）
保证同一时刻只有一个 goroutine 进入临界区的锁，`sync.Mutex`。
**出处**：[sync 标准库](https://pkg.go.dev/sync)
**相关页**：[Mutex](/sync/Mutex.md)

### RWMutex（读写锁）
允许多读单写的锁，读多写少场景吞吐更高，`sync.RWMutex`。
**出处**：[sync 标准库](https://pkg.go.dev/sync)
**相关页**：[RWMutex](/sync/RWMutex.md)

### WaitGroup
等待一组 goroutine 结束的计数栅栏，`sync.WaitGroup`。
**出处**：[sync 标准库](https://pkg.go.dev/sync)
**相关页**：[WaitGroup](/concurrency/WaitGroup.md)

### Atomic（原子操作）
不可分割的底层内存原语，`sync/atomic`，是无锁算法的基石。
**出处**：[sync/atomic 标准库](https://pkg.go.dev/sync/atomic)、[Go 内存模型 · 原子](https://go.dev/ref/mem#atomic)
**相关页**：[Atomic](/sync/Atomic.md)

### 临界区（Critical Section）
访问共享资源的代码段，需要互斥保护。
**出处**：[Go 内存模型 · 锁](https://go.dev/ref/mem#locks)
**相关页**：[CriticalSection](/sync/CriticalSection.md)

### Context（上下文）
跨 API 边界传递取消信号、超时与请求范围值的标准载体，`context.Context`。
**出处**：[context 标准库](https://pkg.go.dev/context)、[官方博客 · Go Concurrency Patterns: Context](https://go.dev/blog/context)
**相关页**：[Context](/sync/Context.md)

### errgroup
`golang.org/x/sync/errgroup`：带错误传播与取消的 goroutine 组管理。
**出处**：[golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)
**相关页**：[ErrorGroup](/concurrency/ErrorGroup.md)

### Goroutine 泄漏
goroutine 因阻塞在永不到来的通道操作上而无法退出，累积泄漏内存。
**出处**：[官方博客 · Goroutine Leak Profiles](https://go.dev/blog/goroutine-leak-profiles)
**相关页**：[GoroutineImpl](/concurrency/GoroutineImpl.md)、[Pprof](/debug/Pprof.md)

### Race Detector（竞态检测器）
基于 ThreadSanitizer 的动态竞态检测工具，`go test -race`。
**出处**：[官方博客 · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
**相关页**：[RaceCondition](/sync/RaceCondition.md)、[Test](/test/Test.md)

## 内存与垃圾回收

### GC（垃圾回收）
Go 运行时自动回收不可达堆内存的机制；并发、三色标记、低暂停。
**出处**：[官方 · A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)
**相关页**：[GC](/gc/GC.md)、[GC（内存分配篇）](/alloc/GC.md)

### 三色标记
GC 可达性分析的抽象：白（未访问）、灰（待扫描）、黑（已扫描）。
**出处**：[官方 GC 指南 · GC 循环](https://go.dev/doc/gc-guide#The_GC_cycle)
**相关页**：[GC](/gc/GC.md)

### 混合写屏障
Go 1.8 起的写屏障策略，把栈重扫需要的时间降到接近零。
**出处**：[官方博客 · Go GC: Prioritizing low latency and simplicity](https://go.dev/blog/go15gc)
**相关页**：[GC](/gc/GC.md)

### GOGC
控制 GC 触发时机的环境变量/参数：堆增长百分比。
**出处**：[官方 GC 指南 · GOGC](https://go.dev/doc/gc-guide#GOGC)
**相关页**：[Practice](/alloc/Practice.md)

### GOMEMLIMIT
堆内存软上限，`GOMEMLIMIT` 环境变量，防内存失控。
**出处**：[官方 GC 指南 · Memory limit](https://go.dev/doc/gc-guide#Memory_limit)
**相关页**：[Practice](/alloc/Practice.md)

### 逃逸分析（Escape Analysis）
编译器判定对象分配在栈还是堆的分析；逃逸的对象由 GC 管理。
**出处**：[官方 GC 指南 · 逃逸分析](https://go.dev/doc/gc-guide#Escape_analysis)、[官方博客 · Allocating on the Stack](https://go.dev/blog/allocation-optimizations)
**相关页**：[Segment](/var/Segment.md)、[Alloc](/alloc/Alloc.md)

### 零值（Zero Value）
变量声明后未显式赋值时的默认值，Go 保证变量总有确定初值。
**出处**：[语言规范 · 零值](https://go.dev/ref/spec#The_zero_value)
**相关页**：[VarAndInit](/var/VarAndInit.md)

### nil
预定义标识符：指针、通道、映射、切片、接口、函数类型的零值。
**出处**：[语言规范 · 预定义标识符](https://go.dev/ref/spec#Predeclared_identifiers)
**相关页**：[Nil](/const/Nil.md)

## 类型系统

### Slice（切片）
对底层数组的抽象：指针 + 长度 + 容量，可动态增长。
**出处**：[语言规范 · 切片类型](https://go.dev/ref/spec#Slice_types)、[官方博客 · Go Slices: usage and internals](https://go.dev/blog/slices-intro)
**相关页**：[Slice](/type/Slice.md)

### Append 扩容
`append` 在容量不足时分配更大的底层数组并迁移元素。
**出处**：[官方博客 · append 的机制](https://go.dev/blog/slices)
**相关页**：[Slice](/type/Slice.md)

### Map（映射）
哈希表实现的键值容器，遍历顺序故意随机化，`map[K]V`。
**出处**：[语言规范 · 映射类型](https://go.dev/ref/spec#Map_types)、[官方博客 · Go maps in action](https://go.dev/blog/maps)
**相关页**：[Map](/type/Map.md)

### Interface（接口）
方法签名的集合；Go 的隐式实现（结构化类型）不同于其他语言的名义实现。
**出处**：[语言规范 · 接口类型](https://go.dev/ref/spec#Interface_types)、[Effective Go · Interfaces](https://go.dev/doc/effective_go#interfaces)
**相关页**：[Interface](/type/Interface.md)、[Interface（OOP 篇）](/oop/Interface.md)

### 方法集（Method Set）
类型关联的方法集合，决定接口满足关系；值接收者与指针接收者的方法集不同。
**出处**：[语言规范 · 方法集](https://go.dev/ref/spec#Method_sets)
**相关页**：[PointerReceiver](/oop/PointerReceiver.md)

### 类型断言（Type Assertion）
从接口值取出其动态类型的具体值，`x.(T)`，可带 comma-ok 形式。
**出处**：[语言规范 · 类型断言](https://go.dev/ref/spec#Type_assertions)
**相关页**：[Assertion](/type/Assertion.md)、[TypeAssertion](/oop/TypeAssertion.md)

### 类型开关（Type Switch）
对接口动态类型做多路分派的 `switch x.(type)`。
**出处**：[语言规范 · 类型开关](https://go.dev/ref/spec#Type_switches)
**相关页**：[Switch](/type/Switch.md)

### 反射（Reflection）
运行时检视类型与值的能力，`reflect` 包；官方用「三定律」阐述。
**出处**：[官方博客 · The Laws of Reflection](https://go.dev/blog/laws-of-reflection)、[reflect 标准库](https://pkg.go.dev/reflect)
**相关页**：[Reflection](/reflection/Reflection.md)

### 泛型（Generics）
类型参数化，Go 1.18 起；函数与类型可带类型参数与约束。
**出处**：[官方博客 · An Introduction To Generics](https://go.dev/blog/intro-generics)、[语言规范 · 类型参数声明](https://go.dev/ref/spec#Type_parameter_declarations)
**相关页**：[Generics](/generics/Generics.md)

### 约束（Constraint）
类型参数必须满足的接口型条件，可用近似元素（`~T`）与联合（`A|B`）表达。
**出处**：[官方博客 · When To Use Generics](https://go.dev/blog/when-generics)
**相关页**：[Constraints](/generics/Constraints.md)

### 类型推断（Type Inference）
编译器从实参推导类型参数的机制，泛型语法糖的核心。
**出处**：[官方博客 · Type Inference](https://go.dev/blog/type-inference)
**相关页**：[TypeInference](/type/TypeInference.md)

### 嵌入（Embedding）
命名类型不带字段名地写入结构体/接口，获得转发与组合，Go 的「继承替代」。
**出处**：[Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
**相关页**：[Embedding](/oop/Embedding.md)

### 闭包（Closure）
引用外层变量的函数字面量，`func` 表达式即函数值。
**出处**：[语言规范 · 函数字面量](https://go.dev/ref/spec#Function_literals)
**相关页**：[AnonymousFunc](/func/AnonymousFunc.md)

### 变参（Variadic Parameter）
参数列表末尾的 `...T` 参数，调用方可传任意个数实参。
**出处**：[语言规范 · 函数类型（变参）](https://go.dev/ref/spec#Function_types)
**相关页**：[VariadicParameters](/func/VariadicParameters.md)

### Iota
常量声明中的自增计数器，配合常量表达式生成枚举。
**出处**：[语言规范 · Iota](https://go.dev/ref/spec#Iota)、[官方博客 · Constants](https://go.dev/blog/constants)
**相关页**：[Iota](/const/Iota.md)

### 无类型常量（Untyped Constant）
不受具体类型约束的常量，精度无限，可隐式适配多种类型。
**出处**：[官方博客 · Constants](https://go.dev/blog/constants)
**相关页**：[Cant](/const/Cant.md)

### 结构体标签（Struct Tag）
结构体字段上的元数据字符串，编码/解码与映射的约定载体。
**出处**：[encoding/json 标准库 · 标签约定](https://pkg.go.dev/encoding/json)、[官方博客 · JSON and Go](https://go.dev/blog/json)
**相关页**：[StructTags](/idioms/StructTags.md)

## 错误处理

### Error（错误）
`error` 内建接口：非 nil 即出错；Go 的错误是值，显式检查。
**出处**：[语言规范 · Errors](https://go.dev/ref/spec#Errors)、[官方博客 · Error handling and Go](https://go.dev/blog/error-handling-and-go)
**相关页**：[Error](/error/Error.md)

### 错误包装（Error Wrapping）
`fmt.Errorf` 的 `%w` 动词与 `errors.Is/As/Unwrap` 链式检查。
**出处**：[errors 标准库](https://pkg.go.dev/errors)
**相关页**：[Errors](/error/Errors.md)

### Defer
延迟到函数返回前执行的调用，栈式 LIFO，常配资源释放。
**出处**：[语言规范 · Defer 语句](https://go.dev/ref/spec#Defer_statements)、[官方博客 · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
**相关页**：[Defer](/func/Defer.md)

### Panic / Recover
不可恢复错误的中断机制与捕获机制，成对出现于延迟调用中。
**出处**：[官方博客 · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)、[Effective Go · Recover](https://go.dev/doc/effective_go#recover)
**相关页**：[PanicAndRecover](/error/PanicAndRecover.md)

## 工程化

### Module（模块）
带版本号的包集合，`go.mod` 声明路径与依赖，Go 的依赖单元。
**出处**：[官方 · Go Modules 使用指南](https://go.dev/doc/modules/)、[Go Modules Reference](https://go.dev/ref/mod)
**相关页**：[Mod](/mod/Mod.md)

### go.mod
模块根目录的声明文件：模块路径、Go 版本、require/exclude/retract。
**出处**：[Go Modules Reference](https://go.dev/ref/mod)
**相关页**：[Init](/mod/Init.md)

### 最小版本选择（MVS）
Go 的依赖解析算法：为每个依赖选出满足所有需求的最小（最保守）版本。
**出处**：[Go Modules Reference · 最小版本选择](https://go.dev/ref/mod)
**相关页**：[Mod](/mod/Mod.md)

### Workspace（工作区）
`go.work` 聚合多个本地模块协同开发，无需改 go.mod。
**出处**：[Go 官方文档 · Workspaces（外部链接）](https://go.dev/doc/tutorial/workspaces)
**相关页**：[Work](/mod/Work.md)

### 工具链（Toolchain）
go 命令、编译器、标准库与相关工具的整体；支持多版本安装与自动切换。
**出处**：[官方 · 安装与管理 Go 工具链](https://go.dev/doc/manage-install)
**相关页**：[Env](/env/Env.md)、[Install](/env/Install.md)

### Pprof
运行时性能剖析工具集：CPU、堆、goroutine、锁、trace。
**出处**：[runtime/pprof 标准库](https://pkg.go.dev/runtime/pprof)、[官方博客 · Profiling Go Programs](https://go.dev/blog/pprof)
**相关页**：[Pprof](/debug/Pprof.md)

### PGO（按配置优化）
用生产 profile 反哺编译器内联与布局决策的优化，Go 1.21 起。
**出处**：[官方 · Profile-guided optimization](https://go.dev/doc/pgo)、[官方博客 · PGO in Go 1.21](https://go.dev/blog/pgo)
**相关页**：[PGO](/debug/PGO.md)

### Fuzzing（模糊测试）
覆盖率引导的随机化测试，`FuzzXxx(*testing.F)`，Go 1.18 起内建。
**出处**：[官方 · Fuzzing](https://go.dev/doc/security/fuzz/)
**相关页**：[Fuzz](/test/Fuzz.md)

### 死锁（Deadlock）
多个执行流互相等待对方持有的资源而永久阻塞。未找到官方单页权威出处（待核），运行时对全部 goroutine 均不可调度时会以 `fatal error: all goroutines are asleep` 报告；相关标准库口径见 [sync 标准库](https://pkg.go.dev/sync)。
**相关页**：[CriticalSection](/sync/CriticalSection.md)、[Chan](/concurrency/Chan.md)

## 算法与数据结构

### 动态数组
容量按需倍增的变长数组，Go 切片即其工程化形态。
**出处**：[动态数组 · Wikipedia](https://en.wikipedia.org/wiki/Dynamic_array)、[官方博客 · Go Slices](https://go.dev/blog/slices-intro)
**相关页**：[DynamicArray](/algo/array/DynamicArray.md)

### 哈希表
平均 O(1) 的键值容器，冲突处理决定性能形态。
**出处**：[哈希表 · Wikipedia](https://en.wikipedia.org/wiki/Hash_table)
**相关页**：[Hash](/algo/hash/Hash.md)、[Map](/type/Map.md)

### 红黑树
自平衡二叉搜索树，插入/删除/查找 O(log n)，Go map 的底层结构之一。
**出处**：[红黑树 · Wikipedia](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
**相关页**：[RedBlackTree](/algo/tree/RedBlackTree.md)

### 跳表（Skip List）
多级链表实现的对数查找结构，Redis 有序集合的底层实现。
**出处**：[跳表 · Wikipedia](https://en.wikipedia.org/wiki/Skip_list)
**相关页**：[SkipList](/algo/list/SkipList.md)

---

**维护口径**：新增条目必须给出可点的权威出处（官方文档/规范/官方博客/原论文/标准库）；查不到就写「未找到权威出处（待核）」，不得凭印象编造链接。

<!-- BACKLINKS-AUTO -->
## 相关页面

- [DynamicArray](/algo/array/DynamicArray.md)
- [Hash](/algo/hash/Hash.md)
- [SkipList](/algo/list/SkipList.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [Alloc](/alloc/Alloc.md)
- [GC](/alloc/GC.md)
- [Practice](/alloc/Practice.md)
- [Actor](/concurrency/Actor.md)
- [CSP](/concurrency/CSP.md)
- [Chan](/concurrency/Chan.md)
- [ChanImpl](/concurrency/ChanImpl.md)
- [ErrorGroup](/concurrency/ErrorGroup.md)
- [GMP](/concurrency/GMP.md)
- [Goroutine](/concurrency/Goroutine.md)
- [GoroutineImpl](/concurrency/GoroutineImpl.md)
- [Select](/concurrency/Select.md)
- [WaitGroup](/concurrency/WaitGroup.md)
- [Cant](/const/Cant.md)
- [Iota](/const/Iota.md)
- [Nil](/const/Nil.md)
- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [Error](/error/Error.md)
- [Errors](/error/Errors.md)
- [PanicAndRecover](/error/PanicAndRecover.md)
- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [GC](/gc/GC.md)
- [MemoryModel](/gc/MemoryModel.md)
- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [StructTags](/idioms/StructTags.md)
- [knowledge](knowledge.md)
- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [TypeAssertion](/oop/TypeAssertion.md)
- [Reflection](/reflection/Reflection.md)
- [Atomic](/sync/Atomic.md)
- [Context](/sync/Context.md)
- [CriticalSection](/sync/CriticalSection.md)
- [MemorySynchronization](/sync/MemorySynchronization.md)
- [Mutex](/sync/Mutex.md)
- [RWMutex](/sync/RWMutex.md)
- [RaceCondition](/sync/RaceCondition.md)
- [Runtime](/sync/Runtime.md)
- [Fuzz](/test/Fuzz.md)
- [Test](/test/Test.md)
- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Slice](/type/Slice.md)
- [Switch](/type/Switch.md)
- [TypeInference](/type/TypeInference.md)
- [Segment](/var/Segment.md)
- [VarAndInit](/var/VarAndInit.md)
