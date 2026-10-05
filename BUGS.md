# BUGS.md — 全仓纠错台账

全仓文档示例逐块编译+运行后登记的问题清单。判定三档：已修（verify_one.py 实测 PASS）/ 非错误（有意为之，附理由）/ 页面级。工具：hg-verify/verify_one.py。


## algo/array/CircularBuffer.md

- [x] `algo_array_CircularBuffer_0` [片段] 非错误 — 不改：初始化片段（type RingBuffer + NewRingBuffer，自身即合法 Go 源码）；列表缩进的 fence 使验证器把顶层声明包进 func main 才产生伪语法错；本块是页面「基本操作」的增量片段，类型/方法在上方块定义，页尾「示例代码」合并全部操作，实测 PASS；验证：不适用(片段;同页 fence111 完整程序实测 PASS，输出 true/hello/false)
- [x] `algo_array_CircularBuffer_1` [片段] 非错误 — 不改：「写入数据」Write 方法片段，RingBuffer 在上方块定义；列表缩进的 fence 使验证器把顶层声明包进 func main 才产生伪语法错；本块是页面「基本操作」的增量片段，类型/方法在上方块定义，页尾「示例代码」合并全部操作，实测 PASS；验证：不适用(片段;同页 fence111 完整程序实测 PASS，输出 true/hello/false)
- [x] `algo_array_CircularBuffer_2` [片段] 非错误 — 不改：「读取数据」Read 方法片段，RingBuffer 在上方块定义；列表缩进的 fence 使验证器把顶层声明包进 func main 才产生伪语法错；本块是页面「基本操作」的增量片段，类型/方法在上方块定义，页尾「示例代码」合并全部操作，实测 PASS；验证：不适用(片段;同页 fence111 完整程序实测 PASS，输出 true/hello/false)
- [x] `algo_array_CircularBuffer_3` [片段] 非错误 — 不改：「检查缓冲区状态」IsFull/IsEmpty 片段，RingBuffer 在上方块定义；列表缩进的 fence 使验证器把顶层声明包进 func main 才产生伪语法错；本块是页面「基本操作」的增量片段，类型/方法在上方块定义，页尾「示例代码」合并全部操作，实测 PASS；验证：不适用(片段;同页 fence111 完整程序实测 PASS，输出 true/hello/false)

## algo/array/DynamicArray.md

- [x] `algo_array_DynamicArray_0` [未使用] 已修 — 块尾补 fmt.Println(slice) 展示切出结果，教学意图不变；验证：PASS(输出 [2 3 4])
- [x] `algo_array_DynamicArray_1` [未使用] 已修 — 块尾补 fmt.Println(slice, len, cap) 展示 make 长度与容量；验证：PASS(输出 [0 0 0] 3 5)
- [x] `algo_array_DynamicArray_2` [未使用] 已修 — 块尾补 fmt.Println(s2) 用起 s2；验证：PASS(输出 [2 3])
- [x] `algo_array_DynamicArray_7` [未使用] 已修 — 块尾补 fmt.Println(subSlice) 用起 subSlice；验证：PASS(输出 [2 3 4])

## algo/array/MultidimensionalArray.md

- [x] `algo_array_MultidimensionalArray_0` [未使用] 已修 — 补 fmt.Println(arr) 展示二维数组零值；验证：PASS(输出 [[0 0 0] [0 0 0]])
- [x] `algo_array_MultidimensionalArray_1` [未使用] 已修 — 补 fmt.Println(arr) 展示初始化后的二维数组；验证：PASS(输出 [[1 2 3] [4 5 6]])

## alloc/Alloc.md

- [x] `alloc_Alloc_1` [runtime示意] 非错误 — 不改：页面在本块前明示「（运行时内部伪代码示意，不可直接编译运行）」，mcentral.alloc/span.allocateObject 为运行时内部标识符；验证：不适用(页面明示的运行时伪代码；整合后的真实可运行示例在同页 fence132，实测 PASS)
- [x] `alloc_Alloc_3` [runtime示意] 非错误 — 不改：页面在本块前明示「（运行时内部伪代码示意，不可直接编译运行）」，span *mspan/span.allocate 为运行时内部标识符；验证：不适用(页面明示的运行时伪代码；整合后的真实可运行示例在同页 fence132，实测 PASS)
- [x] `alloc_Alloc_4` [runtime示意] 非错误 — 不改：页面在本块前明示「（运行时内部伪代码示意，不可直接编译运行）」，newHeapArena 为运行时内部标识符；验证：不适用(页面明示的运行时伪代码；整合后的真实可运行示例在同页 fence132，实测 PASS)

## alloc/GC.md

- [x] `alloc_GC_1` [片段] 已修 — 列表内缩进围栏原是 import+init 用法片段，块内补 package main 与空的 func main 使其成为完整可运行程序（教学点 init 里 SetMemoryLimit 不变）；验证：PASS(无输出，编译运行即退出)
- [x] `alloc_GC_2` [缺import] 已修 — import 块补 "sync"（sync.Pool 在用）；验证：PASS(总分配次数(Mallocs): 170)

## cgo/CGO.md

- [x] `cgo_CGO_1` [缺import] 已修 — 裸语句片段补成完整程序：加 package main、#include <stdlib.h> 前导注释、import "C"/"unsafe" 并包进 main，原三行转换代码原样保留；验证：PASS(可编译运行，无输出)
- [x] `cgo_CGO_2` [缺import] 已修 — 同上补全为完整程序，另补 import "fmt" 并加 fmt.Println(gostr) 消除 declared and not used；验证：PASS(输出 Hello)
- [x] `cgo_CGO_5` [片段] 非错误 — 多文件示例：myclass.h 与 myclass.cpp 的完整源码就在本节上方，Go 块 #include 工程内头文件，单块抽出来必然报头文件不存在；验证：不适用(实测报 myclass.h: No such file or directory，属多文件工程示例的预期结果)
- [x] `cgo_CGO_6` [代码错误] 已修 — §6 示例把 C 函数定义放进带 //export 的前置注释，违反 cgo「前置只放声明」规则，链接期 multiple definition of callGoHello，照抄编不过；改为前置仅声明、定义移到同目录 caller.c（go build 自动一起编译），补规则说明；验证：页面级拼装实测（go 文件+caller.c 同目录）：BUILD OK，运行输出 Hello from Go!；单块抽跑缺 caller.c 的链接失败属预期内
- [x] `cgo_CGO_8` [片段] 非错误 — 外部静态库示例：依赖读者自备的 libmylib.a 与 mylib.h（页面已说明前置条件），单块无法编译；验证：不适用(实测报 mylib.h: No such file or directory，属预期)
- [x] `cgo_CGO_9` [片段] 非错误 — 外部动态库示例：同上，依赖工程内的 libmylib.so 与 mylib.h；验证：不适用(实测报 mylib.h: No such file or directory，属预期)

## cmd/Design.md

- [x] `cmd_Design_1` [工程示意] 非错误 — cobra 命令文件引用 dbtool/internal/db，是多目录项目结构示意；验证器单块抽跑时模块路径不符 internal 包规则才报错；验证：不适用(需整个项目结构构建；包声明/导入写法与页面工程结构一致)
- [x] `cmd_Design_3` [片段] 非错误 — 6.5.1 是 package db 的 _test.go 文件，connectMySQL/connectPostgreSQL 定义在本页 6.4.4 internal/db/db.go 块中，页面按项目结构分块展示同一工程；验证：不适用(跨文件测试片段，验证器单块独立编译必然报 undefined；与 b03 compress_ErrHandleAndTest_1 同型判定)

## compress/Advanced.md

- [x] `compress_Advanced_0` [其他] 已修 — 块内补缺失的 addFileToZip 最小实现（zipWriter.Create + io.Copy），顺带让 io/path/filepath 两个未使用导入被真正用到；验证：PASS(无输出)
- [x] `compress_Advanced_2` [片段] 非错误 — 5.1.3 的 main 调用的 createZipParallel/extractZipParallel 在本页 5.1.1 两个相邻代码块中定义，同一示例分块展示；验证：不适用(跨块引用，单独抽块必然 undefined)
- [x] `compress_Advanced_5` [片段] 非错误 — 5.2.3 的 main 调用的 compressLargeFile/decompressLargeFile 在本页 5.2.1/5.2.2 两块中定义；验证：不适用(跨块引用)

## compress/Archive.md

- [x] `compress_Archive_0` [片段] 非错误 — 不改：3.1.1「基本使用」小节给出的是 archive/tar 所需 import 清单，服务于下方 create/extract 两块（两块实测 PASS）；验证：不适用(明示的导入示意片段)
- [x] `compress_Archive_3` [片段] 非错误 — 不改：实践案例 main 调用的 createTar/extractTar 定义在同页上方两块；把页面三块拼成完整程序实测运行，输出与页面「运行输出」逐行一致；验证：不适用(片段;组合程序实测输出 Tar file created/extracted successfully)
- [x] `compress_Archive_4` [片段] 非错误 — 不改：3.2.1「基本使用」小节给出的是 archive/zip 所需 import 清单，服务于下方 create/extract 两块（两块实测 PASS）；验证：不适用(明示的导入示意片段)
- [x] `compress_Archive_7` [片段] 非错误 — 不改：实践案例 main 调用的 createZip/extractZip 定义在同页上方两块；组合成完整程序实测运行，输出与页面「运行输出」逐行一致；验证：不适用(片段;组合程序实测输出 Zip file created/extracted successfully)

## compress/Composite.md

- [x] `compress_Composite_0` [片段] 已修 — 补上缺失的 addFileToTar 函数（与同页 zip 块的 addFileToZip 写法对齐，含 WriteHeader+io.Copy），io/path/filepath 两个原本未用的 import 随之被用上；验证：PASS(无输出，编译运行退出码 0)
- [x] `compress_Composite_2` [代码缺失] 已修 — 4.1.3 补实践 main：os.WriteFile 自造 file1/file2 输入（log.Fatal 收尾），正文写明与 4.1.1/4.1.2 函数同包编译；验证：PASS（拼装 comp_targz exit 0，输出与页面声明一致，产物核对一致）
- [x] `compress_Composite_5` [代码缺失] 已修 — 4.2.3 同上：补自造输入的实践 main，正文写明同包编译；验证：PASS（拼装 comp_zip exit 0，输出与页面声明一致，产物核对一致）

## compress/Compress.md

- [x] `compress_Compress_0` [片段] 非错误 — 「基本使用」的 import 清单块，只列本节要用的包，配合下方 compressToFile/decompressFromFile 函数块使用；单独成文件必然 unused import，无最小修法；验证：不适用(导入清单片段，教学形式即如此)
- [x] `compress_Compress_10` [代码缺失] 已修 — 2.3.2 只有函数定义没有调用块却声称输出；补实践案例 main（标准库 bzip2 无写入端，预置一段压缩数据，原始内容 "hello bzip2"），小节标题改「解压 bzip2 文件」，输出补解压内容行；验证：PASS（拼装 comp_bz2 实测输出逐字一致：File decompressed successfully / 解压内容: hello bzip2，生成文件内容核对一致）
- [x] `compress_Compress_3` [片段] 非错误 — 实践案例 main 调用的 compressToFile/decompressFromFile 在同节上方两块中定义，正文已写明「用上面的函数」；声称的输出与整页拼出的程序一致；验证：不适用(明示片段，函数在上方块定义)
- [x] `compress_Compress_4` [片段] 非错误 — 同 _0，zlib 节的 import 清单块；验证：不适用(导入清单片段)
- [x] `compress_Compress_7` [片段] 非错误 — 同 _3，zlib 实践案例 main，调用的函数在上方块定义；验证：不适用(明示片段)
- [x] `compress_Compress_8` [片段] 非错误 — 同 _0，bzip2 节的 import 清单块；验证：不适用(导入清单片段)
- [x] `compress_Compress_9` [缺import] 已修 — 块内补 import(compress/bzip2、io、os)：块内用了 bzip2.NewReader 但 normalize 的别名表没有 bzip2，推不进去；验证：PASS(编译运行退出码 0，无输出)

## compress/ErrHandleAndTest.md

- [x] `compress_ErrHandleAndTest_1` [片段] 非错误 — 6.2.1 测试块自带 import 区，仅引用的 compressFile 定义在本页 6.1 示例块；验证：不适用(跨块引用 compressFile)
- [x] `compress_ErrHandleAndTest_2` [片段] 非错误 — 已补 import 区（testing/os/io/ioutil，与 6.2.1 块对齐）；剩余 undefined: compressFile 为 6.1 的跨块引用；验证：不适用(跨块引用 compressFile，补导入后无法单独 PASS)
- [x] `compress_ErrHandleAndTest_3` [片段] 已修 — compressData/decompressFile 页内全无定义：块内补最小 gzip 实现与完整 import 区，测试示例自洽；验证：PASS(无输出)

## concurrency/Chan 1.md

- [x] `concurrency_Chan_1_0` [语法] 已修 — 原块 var c 后又 c := 同名重复声明且语句裸露在函数体外，改为完整 main 程序，第三种写法改用变量 d，末尾 fmt.Println 用起变量；验证：PASS(打印两个通道地址)
- [x] `concurrency_Chan_1_1` [语法] 已修 — 裸语句 c <- 42 / value := <-c 缺上下文与未使用 value，包成 main 并用容量 1 的缓冲通道避免发送阻塞，fmt.Println(value)；验证：PASS(42)
- [x] `concurrency_Chan_1_5` [陈述] 已修 — 死锁示例正文说「程序会卡死」不准确——Go 运行时会检测全局死锁并报 fatal error 退出；改写说法并补运行输出声明；验证：PASS（实跑输出 fatal error: all goroutines are asleep - deadlock! 与声明一致）

## concurrency/Chan.md

- [x] `concurrency_Chan_0` [runtime示意] 非错误 — close 通道的 runtime/chan.go 源码节选（c/lock/unlock/plainError 均为 runtime 内部标识符），正文明确写「从上面的源码可以看到」，不是可运行程序；验证：不适用(runtime 源码示意)
- [x] `concurrency_Chan_1` [有意演示] 非错误 — 重复 close 通道触发 panic 是本节主题，正文已写明「会引发 panic」并给出错误文案；验证：PASS(实跑 panic: close of closed channel，与页面声明文案一致)
- [x] `concurrency_Chan_8` [runtime示意] 非错误 — runtime hchan 结构简化示意，正文写「通道核心数据结构的简化示例」，waitq/mutex 是 runtime 内部类型；验证：不适用(runtime 源码示意)

## concurrency/ChanImpl.md

- [x] `concurrency_ChanImpl_0` [runtime示意] 非错误 — runtime/chan.go 的 hchan/waitq/sudog/chansend/chanrecv 讲解，waitq、mutex、lock、goready 等是运行时内部标识符，页面讲的是源码不是可运行程序；验证：不适用(runtime 源码示意)
- [x] `concurrency_ChanImpl_1` [runtime示意] 非错误 — runtime/chan.go 的 hchan/waitq/sudog/chansend/chanrecv 讲解，waitq、mutex、lock、goready 等是运行时内部标识符，页面讲的是源码不是可运行程序；验证：不适用(runtime 源码示意)
- [x] `concurrency_ChanImpl_2` [runtime示意] 非错误 — runtime/chan.go 的 hchan/waitq/sudog/chansend/chanrecv 讲解，waitq、mutex、lock、goready 等是运行时内部标识符，页面讲的是源码不是可运行程序；验证：不适用(runtime 源码示意)
- [x] `concurrency_ChanImpl_3` [runtime示意] 非错误 — runtime/chan.go 的 hchan/waitq/sudog/chansend/chanrecv 讲解，waitq、mutex、lock、goready 等是运行时内部标识符，页面讲的是源码不是可运行程序；验证：不适用(runtime 源码示意)
- [x] `concurrency_ChanImpl_4` [runtime示意] 非错误 — runtime/chan.go 的 hchan/waitq/sudog/chansend/chanrecv 讲解，waitq、mutex、lock、goready 等是运行时内部标识符，页面讲的是源码不是可运行程序；验证：不适用(runtime 源码示意)

## concurrency/GMP.md

- [x] `concurrency_GMP_0` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（type g/m/p/queue、stack、runq 等），不改代码;g.stack 的 stack 类型即运行时内部类型；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: stack
- [x] `concurrency_GMP_1` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（newGoroutine/startGoroutine、makeStack/initStack/getAvailableP/runnable 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: g/makeStack/runnable/getAvailableP
- [x] `concurrency_GMP_2` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（destroyGoroutine/freeStack 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: g/freeStack
- [x] `concurrency_GMP_3` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（schedule/executeGoroutine 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: p/executeGoroutine
- [x] `concurrency_GMP_4` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（contextSwitch/saveContext/loadContext 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: g/saveContext/loadContext
- [x] `concurrency_GMP_5` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（checkPreemption/getCurrentGoroutine/needsPreemption/rescheduleGoroutine 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: getCurrentGoroutine 等
- [x] `concurrency_GMP_6` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（schedulerTick/schedulingInterval/checkPreemption 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: schedulingInterval
- [x] `concurrency_GMP_7` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（blockGoroutine/blocked/moveToWaitingQueue 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: g/blocked/moveToWaitingQueue
- [x] `concurrency_GMP_8` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（unblockGoroutine/isResourceAvailable/getAvailableP 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: g/isResourceAvailable 等
- [x] `concurrency_GMP_9` [runtime示意] 非错误 — GMP 页为规则明列的 runtime 示意页，块内是调度器内部结构/流程示意（stealWork/工作窃取 等），不改代码；验证：不适用(runtime 示意：GMP 页讲 Go 运行时调度器源码，非可运行程序)；实测 BUILD-FAIL: undefined: p

## concurrency/Goroutine.md

- [x] `concurrency_Goroutine_0` [常驻服务] 非错误 — 双 goroutine 交替打印 + Sleep(6s) 设计内时长，非死锁；验证：PASS(12s 实测：Hello×5 + Goodbye×5)

## concurrency/GoroutineImpl.md

- [x] `concurrency_GoroutineImpl_0` [伪代码] 非错误 — 页面第 47 行明示「为便于理解而简化的示意伪代码，并非运行时的真实源码」；g、makeStack、sched 为示意标识符；验证：不适用(页面明示的伪代码)
- [x] `concurrency_GoroutineImpl_1` [伪代码] 非错误 — 同上，growStack 栈扩表示意；验证：不适用(页面明示的伪代码)
- [x] `concurrency_GoroutineImpl_2` [伪代码] 非错误 — 同上，Scheduler 结构示意，queue.Queue 为示意类型；验证：不适用(页面明示的伪代码)

## concurrency/Select.md

- [x] `concurrency_Select_3` [runtime示意] 非错误 — 正文明确标注该块是 selectgo 的「简化示意伪代码（不是真实源码）」，scase/caseCanProceed/fastrand/gopark/selectGoPark/parkResult 为 runtime 内部标识符，不按可运行程序处理，不改；验证：不适用(伪代码示意，页面括注声明非真实源码)

## const/Cant.md

- [x] `const_Cant_0` [其他] 非错误 — 整页主题即「有些东西不能定义为常量」，本块展示接口类型常量的非法写法（注释「不能将接口类型定义为常量」），invalid constant type error 正是教学内容，不修；验证：不适用(故意的编译错误反例)
- [x] `const_Cant_1` [其他] 非错误 — 函数类型常量的非法写法示范，invalid constant type func(int) int 即页面要讲的结论，不修；验证：不适用(故意的编译错误反例)
- [x] `const_Cant_2` [其他] 非错误 — 块内前两行是合法常量（含正文澄清 time.Second 是常量），第三行 const now = time.Now() 是页面要展示的运行时求值反例并带「不能」注释，不修；验证：不适用(故意的编译错误反例)
- [x] `const_Cant_3` [其他] 非错误 — 切片/映射不能作常量的示范，两行均带「不能」注释，报错即教学点，不修；验证：不适用(故意的编译错误反例)
- [x] `const_Cant_4` [其他] 非错误 — 对常量取地址的反例（注释写明 invalid operation: cannot take address of count），p 未使用是编译停在取地址错误的伴生现象，不修；验证：不适用(故意的编译错误反例)

## const/Const.md

- [x] `const_Const_0` [伪代码] 非错误 — 正文写明「语法为：」，块内 const identifier [type] = value 是语法模板，下方 bullet 逐项解释 identifier/type/value 占位符；验证：不适用(语法占位符，规则明示不改)

## const/Nil.md

- [x] `const_Nil_0` [语法] 已修 — 块把 var 声明和 fmt.Println 平铺在包级，属非法 Go；用 func main() 包住两行语句，教学意图不变；验证：PASS(<nil>)
- [x] `const_Nil_1` [语法] 已修 — 同上：func main() 包住切片/映射/通道零值示例；验证：PASS([] map[] <nil>)
- [x] `const_Nil_2` [语法] 已修 — 同上：func main() 包住接口零值示例；验证：PASS(<nil>)
- [x] `const_Nil_3` [语法] 已修 — 同上：func main() 包住函数零值示例；验证：PASS(<nil>)

## db/ConnectPool.md

- [x] `db_ConnectPool_0` [片段] 非错误 — 6.2.1 单行 API 示意 db.SetMaxOpenConns(10)，db 即 6.3.1 里 sql.Open 得到的 *sql.DB，正文逐条解释了参数含义；验证：不适用(单行 API 片段)
- [x] `db_ConnectPool_1` [片段] 非错误 — 同 _0，db.SetMaxIdleConns(5) 单行示意；验证：不适用(单行 API 片段)
- [x] `db_ConnectPool_2` [片段] 非错误 — 同 _0，db.SetConnMaxLifetime(time.Hour) 单行示意；验证：不适用(单行 API 片段)
- [x] `db_ConnectPool_3` [需真实凭据] 非错误 — 连接池示例用占位 DSN(user/password)，对本机真实 MySQL 认证被拒；验证：不适用(编译 PASS；Access denied 属占位凭据预期，换真实账号才可运行)
- [x] `db_ConnectPool_4` [语法] 已修 — 原来是裸语句躺在包级作用域：包成 func usePool(db *sql.DB) 并补 database/sql、log 两个 import，语句本体逐字未动；验证：PASS(编译运行退出码 0，无输出)

## db/GraphQL.md

- [x] `db_GraphQL_0` [片段] 非错误 — Resolver 骨架引用 gqlgen 生成的 QueryResolver/MutationResolver/model 包，页面 18.3.3/18.3.4 明示这些代码由 gqlgen 生成；验证：不适用(gqlgen 代码生成产物，工程其他处定义)
- [x] `db_GraphQL_1` [常驻服务] 非错误 — gqlgen 模板 main.go：Config{Resolvers:...} 与 gqlgen v0.17.95 真实 API 一致（已核对其自生成代码同款写法）；报错源于本地桩 github.com/myapp/graph 与真实生成代码不符；且 http.ListenAndServe 为常驻服务；验证：不适用(常驻服务+桩差异)

## db/Install.md

- [x] `db_Install_0` [片段] 非错误 — 「1. 导入包」步骤的 import 清单（database/sql + mysql 驱动空导入），与下一步「2. 建立连接」的 connectMySQL 配套；验证：不适用(导入清单片段)
- [x] `db_Install_1` [片段] 非错误 — connectMySQL 函数声明完整，所需 import 在紧邻上一步「导入包」块给出；报错源于列表内缩进代码块被验证器误包进 func main，属工具产物，两步拼起来即合法程序；验证：不适用(明示片段；缩进列表块的验证器伪错)
- [x] `db_Install_2` [片段] 非错误 — 同 _0，PostgreSQL 节导入清单；验证：不适用(导入清单片段)
- [x] `db_Install_3` [片段] 非错误 — 同 _1，connectPostgres；验证：不适用(明示片段；缩进列表块的验证器伪错)
- [x] `db_Install_4` [片段] 非错误 — 同 _0，SQLite 节导入清单；验证：不适用(导入清单片段)
- [x] `db_Install_5` [片段] 非错误 — 同 _1，connectSQLite；验证：不适用(明示片段；缩进列表块的验证器伪错)

## db/Lib.md

- [x] `db_Lib_0` [未使用] 已修 — import 块后补一行 var db *sql.DB，让 database/sql 有实际使用点（原块只 import 不用）；验证：PASS(空输出，退出 0)
- [x] `db_Lib_10` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: db)
- [x] `db_Lib_11` [片段] 非错误 — err 沿用 5.5.1 块中 db.Exec 的返回值，errors.Is 是对其的后续处理，属递进片段；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: err)
- [x] `db_Lib_4` [代码缺失] 已修 — 5.3.1 片段补成完整程序：package main + 空白导入 mysql 驱动（注释说明必须空白导入）+ func main + defer db.Close()；正文补 DSN 占位与 sql.Open 只校验格式的说明；验证：PASS（verify_one fence 47：sql.Open 不真正连接，占位 DSN 可构造成功）
- [x] `db_Lib_5` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: err/db)
- [x] `db_Lib_6` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: db)
- [x] `db_Lib_7` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: db)
- [x] `db_Lib_8` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: db)
- [x] `db_Lib_9` [片段] 非错误 — db 在 5.3.1「建立连接」块中由 sql.Open 创建，本块按小节递进沿用；独立成块缺 db 定义，且需真实 MySQL 才能运行（实测 DSN user:password@/dbname 被本地 3306 拒绝认证），补样板会重写示例，判片段；验证：不适用(BUILD-FAIL: undefined: db)

## db/Mock.md

- [x] `db_Mock_0` [测试文件] 非错误 — sqlmock 测试文件块，无 func main 属测试文件常态；测试体完整正确；验证：PASS(go test 实测：--- PASS: TestGetUserByID)
- [x] `db_Mock_1` [缺import] 已修 — 补 import（database/sql、testing）；验证：PASS(无输出)
- [x] `db_Mock_2` [片段] 非错误 — 被测函数 InsertUser 页内原本缺失：块内补最小实现与 import 区；剩余 setupTestDB/User 为本页上方块引用（整页拼装编译通过已实测）；验证：不适用(跨块引用 setupTestDB/User)
- [x] `db_Mock_4` [片段] 非错误 — 被测函数 UpdateUser 页内原本缺失：块内补最小实现与 import 区；prepareTestData/setupTestDB/User 为本页上方块引用（整页拼装编译通过已实测）；验证：不适用(跨块引用)

## db/Monitor.md

- [x] `db_Monitor_0` [缺import] 非错误 — 19.4.2 指标定义块缺少 prometheus import，但 github.com/prometheus/client_golang 不在 mod 依赖清单且禁止改 mod/go.mod，换标准库方案会毁掉 Prometheus 教学意图，保留原样并标记需要依赖；验证：不适用(缺 prometheus 依赖，无法实测)；需要依赖 github.com/prometheus/client_golang
- [x] `db_Monitor_1` [片段] 非错误 — 19.4.3 采集片段：queryDuration 定义于 19.4.2 的上一块，属同页连续示例；运行还需 prometheus 库与真实数据库，不修；验证：不适用(同页上文定义的片段 + 缺 prometheus 依赖)；需要依赖 github.com/prometheus/client_golang
- [x] `db_Monitor_2` [常驻服务] 非错误 — 两行展示暴露 /metrics 并 ListenAndServe 常驻监听（即使依赖齐备也不退出，TIMEOUT 判非错误），且 promhttp 依赖缺失，不修；验证：不适用(常驻服务示例 + 缺 promhttp 依赖)；需要依赖 github.com/prometheus/client_golang/prometheus/promhttp

## db/NoSQL.md

- [x] `db_NoSQL_0` [需真实服务] 非错误 — mongo-driver 插入示例，编译通过；无 MongoDB(:27017) 时按服务器选择超时退出；验证：不适用(编译 PASS；server selection timeout 属无服务预期)

## db/ORM.md

- [x] `db_ORM_0` [未使用] 已修 — 补 `_ = db` 用掉声明；另把 gorm.Open(mysql.Open(dsn)) 改为 mysql.New(mysql.Config{DSN, SkipInitializeWithVersion: true}) 并配 DisableAutomaticPing——mysql 驱动建连时必发 SELECT VERSION()，占位 DSN 无库可连会 log.Fatal，改后连接推迟到首次使用，log.Fatal 错误处理保留；验证：PASS(无输出，退出码 0)
- [x] `db_ORM_2` [片段] 非错误 — GORM CRUD 操作片段：db 来自 7.3.2 连接块、User 来自 7.3.3 模型块，页面按小节分块展示同一程序，不修；验证：不适用(同页上文定义的 CRUD 片段，跑通还需真实 MySQL)
- [x] `db_ORM_5` [片段] 非错误 — Ent CRUD 操作片段：client/ctx 来自 7.4.4 初始化块，entproject 有桩模块但补全后运行仍需真实 MySQL，保留分块片段形式，不修；验证：不适用(同页上文定义的 CRUD 片段)
- [x] `db_ORM_8` [片段] 非错误 — XORM CRUD 操作片段：engine 来自 7.5.2 连接块、User 来自 7.5.3 模型块，同页连续示例，不修；验证：不适用(同页上文定义的 CRUD 片段)

## db/Performance.md

- [x] `db_Performance_0` [缺import] 已修 — 连接池块补成完整可运行：package main、database/sql/log/time 导入、空白导入 _ "github.com/go-sql-driver/mysql"（原文照抄会 unknown driver），sql.Open 只校验 DSN 不连库，离线可跑；验证：PASS
- [x] `db_Performance_1` [片段] 非错误 — Redis 缓存 helper 节选（页面上下文完整），编译通过且无副作用；验证：编译 PASS

## db/Project.md

- [x] `db_Project_4` [服务型] 非错误 — echo 服务示例常驻；:8080 被本机 Docker 端口映射占用属环境冲突；验证：PASS(端口空闲时实测启动成功，12s 常驻不退)

## db/Security.md

- [x] `db_Security_0` [其他] 已修 — User 类型页面无定义：块内补最小 User 结构体（ID/Name/Email，与 Scan 字段一致），database/sql 由验证器自动推断；验证：PASS(无输出)
- [x] `db_Security_2` [缺import] 已修 — 语句级片段补成 package main 完整程序：显式导入 crypto/tls、database/sql、log、github.com/go-sql-driver/mysql，db 以 defer db.Close() 用起来；验证：PASS(无输出，sql.Open 惰性连接不触库)

## db/Sharding.md

- [x] `db_Sharding_0` [类型] 已修 — 补最小 type User struct{ ID int } 定义，分片路由示例 getShard/insertUser 随之可编译；验证：PASS(编译通过，无运行输出)

## db/Tx.md

- [x] `db_Tx_0` [片段] 非错误 — 9.2.1 是 db.Begin() 用法步骤，db 为既有连接句柄，Begin 需真实数据库连接；验证：不适用(API 步骤片段)
- [x] `db_Tx_1` [片段] 非错误 — 9.2.2 延续 9.2.1 的 tx/err 讲执行语句步骤；验证：不适用(API 步骤片段)
- [x] `db_Tx_2` [片段] 非错误 — 9.2.3 Commit 步骤片段；验证：不适用(API 步骤片段)
- [x] `db_Tx_3` [片段] 非错误 — 9.2.3 Rollback 步骤片段；验证：不适用(API 步骤片段)
- [x] `db_Tx_4` [片段] 非错误 — 9.2「完整示例」仍以既有 db 句柄为前提，事务 Begin/Commit 需真实数据库才能执行；验证：不适用(需真实数据库)
- [x] `db_Tx_5` [片段] 非错误 — GORM Transaction 用法片段：db *gorm.DB 与 User/Account 为工程侧定义；gorm v1.31.2 已在依赖中，事务执行需真实数据库；验证：不适用(API 用法片段)
- [x] `db_Tx_6` [片段] 非错误 — Ent Tx 用法片段：tx.Commit()/tx.Rollback() 无参签名已对照 entgo v0.14.6 生成模板确认一致；client/ctx 为工程侧；验证：不适用(API 用法片段)
- [x] `db_Tx_7` [片段] 非错误 — XORM NewSession 用法片段：engine 为既有 *xorm.Engine，User/Account 为业务模型；验证：不适用(API 用法片段)
- [x] `db_Tx_8` [片段] 非错误 — sql.TxOptions + BeginTx 用法片段，需真实数据库执行；验证：不适用(API 步骤片段)

## debug/Expvar.md

- [x] `debug_Expvar_0` [片段] 非错误 — 「1. 导入 expvar 包」步骤的 import 清单块，本身就是教学目标；验证：不适用(导入清单片段)
- [x] `debug_Expvar_1` [缺import] 已修 — 块内补 import(expvar、net/http)；expvar 不在验证器别名表里推不出来，请求计数示例补齐后编译通过，属常驻 http 服务写法；验证：PASS(http.ListenAndServe 在沙箱里立即返回，退出码 0)
- [x] `debug_Expvar_2` [缺import] 已修 — 同 _1，expvar.Map 示例补 import(expvar、net/http)；验证：PASS(同上，退出码 0)

## debug/Pprof.md

- [x] `debug_Pprof_0` [常驻服务] 非错误 — 前次扫描 HANG 为中间态；当前实测直接跑完；验证：PASS

## debug/Utils.md

- [x] `debug_Utils_2` [缺import] 已修 — import 块补 "log"（goroutine 里 log.Println 在用）；验证：PASS(无输出)

## dp/Proactor.md

- [x] `dp_Proactor_0` [常驻服务] 非错误 — Proactor 模式 echo 服务器，常驻；验证：实测在 :8080 正常监听(验证进程泄漏占端口已清理)

## dp/Reactor.md

- [x] `dp_Reactor_0` [常驻服务] 非错误 — Reactor echo 服务器，常驻；打印 Server is listening on port 8080... 后阻塞；验证：换端口 :18080 实测监听成功

## encoding/Gob.md

- [x] `encoding_Gob_2` [逻辑] 已修 — gob 接口编解码：编码侧改为把接口变量以指针传入 Encode(&m)，直接传具体值收不到接口信封，解码端报 local interface type ... can only be decoded from remote interface type；补运行输出；验证：PASS(hello / image: https://example.com/a.png)

## encoding/Ini.md

- [x] `encoding_Ini_0` [前置缺失] 已修 — 读取示例直接 ini.Load("config.ini") 却无前置说明，裸跑必失败；补「先跑下方写入示例生成或手写」说明、样例 config.ini 内容与运行输出声明；验证：PASS（配样例文件实跑：Name: John Doe / Age: 30 / City: New York 与声明一致；写入+读取成对实测通过）

## encoding/TOML.md

- [x] `encoding_TOML_0` [前置缺失] 已修 — 读取示例直接 toml.LoadFile("config.toml") 却无前置说明；补前置说明、样例 config.toml 内容与运行输出声明；验证：PASS（配样例文件实跑：Host: localhost / Port: 8080 与声明一致；写入+读取成对实测通过）

## env/Env.md

- [x] `env_Env_0` [过时API] 已修 — io/ioutil 已废弃（Go 1.16 起）：ioutil.ReadFile 改 os.ReadFile，import 同步换；读 data/file.txt 是页面明示的项目结构前提；验证：PASS(按页面结构创建 data/file.txt 后输出 hello env)
- [x] `env_Env_1` [过时API] 已修 — 同上：ioutil.ReadFile 改 os.ReadFile 并去掉 io/ioutil 导入；验证：PASS(同上前提)

## error/Error.md

- [x] `semantic_error_Error` [说法不准确] 已修 — C++ 无 finally 块：语言对比表与总结两处改为 try/catch + RAII 惯用法，并补充 Java/Python/JS 才有 finally；验证：事实核对(C++ 标准)

## error/Errors.md

- [x] `error_Errors_4` [片段] 非错误 — 提前返回示例调用 doSomething，该函数在本页第 2、3 节示例块中均有定义，页面按节递进；报的语法错是块内列表缩进使归一化误包 main 所致；验证：不适用(BUILD-FAIL: 语法错来自缩进误包；真实缺口是上方已定义的 doSomething)
- [x] `error_Errors_5` [片段] 非错误 — main 调用的 process 定义在上一块（最佳实践·提前返回），属同页递进片段；验证：不适用(BUILD-FAIL: 语法错来自缩进误包；真实缺口是上方已定义的 process)

## error/PanicAndRecover.md

- [x] `error_PanicAndRecover_0` [常驻服务] 非错误 — 有意演示 panic：程序带非零退出码终止，页面已如实记载输出（含 exit status 2），This will not be executed 不出现正是教学点；验证：实测输出与文档一致
- [x] `error_PanicAndRecover_3` [伪代码] 非错误 — 正文明示「以下是 Go 运行时库中的相关代码片段（伪代码）」，getPanicValue 无函数体属示意，不修；验证：不适用(伪代码示意)

## func/AnonymousFunc.md

- [x] `func_AnonymousFunc_0` [伪代码] 非错误 — 「#### 语法」下的匿名函数语法模板，parameter_list/return_type 为占位符，不修；验证：不适用(语法模板占位符)

## func/Defer.md

- [x] `func_Defer_0` [伪代码] 非错误 — 正文「defer 的语法如下」的语法模板，functionName/deferredFunction 是占位符（等价于规则里的语法占位符类），真实示例在下一节；验证：不适用(语法占位模板)

## func/DefineAndCall.md

- [x] `func_DefineAndCall_0` [伪代码] 非错误 — 「#### 基本语法」下的函数定义模板，parameterList/returnType 为占位符，不修；验证：不适用(语法模板占位符)
- [x] `func_DefineAndCall_2` [伪代码] 非错误 — 「#### 基本语法」下的函数类型定义模板 type FunctionNameType func(parameterList) (returnType)，占位符，不修；验证：不适用(语法模板占位符)

## func/InnerFunc.md

- [x] `func_InnerFunc_8` [输出更正] 已修 — panic 内建函数演示块（defer 先执行再崩溃，教学意图保留），补真实运行输出与说明：Defer executed 先于 panic 信息；验证：输出与文档一致(Defer executed / panic: Something went wrong)
- [x] `func_InnerFunc_9` [输出更正] 已修 — recover 演示块输出注释不完整：第二次调用除打印 Recovered 信息外还打印命名返回值 0，注释据实更正；验证：PASS(5 / Recovered from panic: Division by zero / 0)

## gc/GC.md

- [x] `gc_GC_0` [常驻服务] 非错误 — GC 观察程序设计内运行 20s；验证：PASS(25s 实测：打印 Allocated/TotalAlloc/NumGC)

## generics/Advanced.md

- [x] `generics_Advanced_8` [陈述] 已修 — 8.4.2 第 2 点改为「返回零值实例」：var zero T 拿零值，正文说明反射无法凭空确定类型参数；与示例一致；验证：PASS（verify_one fence 219：Int instance: 0）

## generics/Constraints.md

- [x] `generics_Constraints_3` [片段] 已修 — 块引用的 Stringer 约束定义在上一块，本块单独抽出不编译；在块首补 Stringer 接口定义（3 行），Box 示例意图不变；验证：PASS(编译运行退出码 0)

## generics/Pattern.md

- [x] `generics_Pattern_4` [片段] 非错误 — Container 接口在紧邻上一块（4.3 定义泛型接口）定义，本块只展示 IntContainer 实现与断言，两块连读即完整示例；验证：不适用(页内上一块已定义 Container)

## generics/Performance.md

- [x] `generics_Performance_1` [缺import] 已修 — 补 import "testing"，BenchmarkGeneric 签名用 *testing.B；验证：PASS(编译运行退出码 0，无输出)
- [x] `generics_Performance_2` [片段] 非错误 — 7.4 的 Set[T] 复用 7.3 示例块定义的 Pool[T]/NewPool，正文讲的就是用内存池优化集合，两块配套；验证：不适用(明示片段，Pool 在上方 7.3 定义)

## generics/Syntax.md

- [x] `generics_Syntax_5` [语法] 已修 — 示例调用 intSlice := ... / PrintSlice(intSlice) 原先裸在包级，包进 func main；PrintSlice 定义原样保留；验证：PASS(输出 1 2 3)

## gin/Config.md

- [x] `gin_Config_1` [片段] 非错误 — 10.2.2 演示启动加载，LoadConfig/Config 定义于 10.2.1 块，同页分节连续示例；验证：不适用(LoadConfig 定义于 10.2.1 块)
- [x] `gin_Config_2` [片段] 非错误 — 10.3.1 承接 10.2.1 的 Config/LoadConfig 同文件分节展示；import 块只列本节新增的 fsnotify/viper，gin 复用文件级导入；验证：不适用(Config/LoadConfig 定义于 10.2.1 块)
- [x] `gin_Config_3` [片段] 非错误 — LoadConfigFromEtcd 返回的 Config 定义于 10.2.1 块，本节仅展示 etcd 读取部分；验证：不适用(Config 定义于 10.2.1 块)

## gin/Error.md

- [x] `gin_Error_0` [片段] 已修 — 块首补 someFunction 占位实现（返回 errors.New，注释说明其代表业务调用），handler 原样保留；验证：PASS(空输出，退出 0)
- [x] `gin_Error_3` [片段] 非错误 — 断言用的 AppError 在 8.2.1 小节块中定义，8.2.2 沿用，页面按小节递进；验证：不适用(BUILD-FAIL: undefined: AppError)
- [x] `gin_Error_4` [片段] 已修 — 块首补 ValidationError 类型（含 Error 方法）与 someFunction 占位（返回校验错误），handler 原样保留；验证：PASS(空输出，退出 0；8s 首跑 TIMEOUT 是 gin 冷编译，30s 复跑 PASS)

## gin/Extend.md

- [x] `gin_Extend_0` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；保留补进的 gin 导入；验证：PASS（exit 0）
- [x] `gin_Extend_1` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；gin-contrib/logger 已补进验证依赖；验证：PASS（编译通过+服务启动实测（r.Run() 常驻，按超时收尾））；需要依赖 github.com/gin-contrib/logger v1.2.9
- [x] `gin_Extend_2` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；swaggo 两包已补进验证依赖；验证：PASS（编译通过+服务启动实测（r.Run() 常驻，按超时收尾））；需要依赖 github.com/swaggo/gin-swagger v1.6.1、github.com/swaggo/files v1.0.1
- [x] `gin_Extend_3` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；validator/v10 已在依赖内；验证：PASS（编译通过+服务启动实测（r.Run() 常驻，按超时收尾））
- [x] `gin_Extend_5` [片段] 非错误 — 与上一块「创建自定义中间件」配对：middleware 包在上方块中 package middleware 声明，main 块省略工程级导入，两块须同工程编译；验证：不适用(BUILD-FAIL: undefined: middleware)
- [x] `gin_Extend_7` [片段] 非错误 — 与上一块「创建自定义路由插件」配对：routes 包在上方块声明；验证：不适用(BUILD-FAIL: undefined: routes)
- [x] `gin_Extend_9` [片段] 非错误 — 与上一块「创建自定义数据处理插件」配对：processor 包在上方块声明；验证：不适用(BUILD-FAIL: undefined: processor)

## gin/Middleware.md

- [x] `gin_Middleware_1` [片段] 非错误 — 「全局使用」演示块，Logger 定义于 5.1.1 块；验证：不适用(Logger 定义于 5.1.1 块)
- [x] `gin_Middleware_10` [代码缺失] 已修 — 5.4.3 原块只定义 Middleware1/2 没有可运行入口；改为 httptest 驱动的完整程序（NewRecorder+NewRequest+ServeHTTP），Logger 中间件套真实 handler；验证：PASS（输出 4 行与声明逐字一致）
- [x] `gin_Middleware_2` [片段] 非错误 — 「路由组中使用」演示块：r 为上一块创建的路由，AuthRequired 在 5.3 定义，loginHandler/submitHandler 为业务处理占位；验证：不适用(用法示意，符号在页内其他块/工程其他处)
- [x] `gin_Middleware_5` [缺import] 已修 — 块内使用 gin.New 却只导入 cors，补 "github.com/gin-gonic/gin" 导入；验证：PASS(gin.New 建立 engine 后正常退出)
- [x] `gin_Middleware_7` [片段] 非错误 — 「在路由组中使用自定义中间件」演示块：AuthRequired 在 5.3 定义，r/secureEndpoint 为上下文占位；验证：不适用(用法示意)
- [x] `gin_Middleware_8` [片段] 非错误 — 5.4.1 顺序演示块，Middleware1/Middleware2 的完整定义在 5.4.3 块给出；验证：不适用(完整可运行版本见 5.4.3 块)
- [x] `gin_Middleware_9` [片段] 非错误 — 5.4.2 顺序示意，GlobalMiddleware/GroupMiddleware/endpointHandler 为命名占位，正文只讲注册顺序；可运行对应版本在 5.4.3 块；验证：不适用(顺序示意占位符)

## gin/Optimize.md

- [x] `gin_Optimize_0` [伪代码] 非错误 — 本页是 gin 路由内部源码讲解：块用 gin 未导出类型 router/node/HandlersChain，属于源码示意，非可运行程序；验证：不适用(源码示意)
- [x] `gin_Optimize_2` [伪代码] 非错误 — 同页源码示意：node.getValue 引用 gin 内部类型 Params/HandlersChain；验证：不适用(源码示意)
- [x] `gin_Optimize_3` [伪代码] 非错误 — 路径缓存示例引用 gin 内部 router/Context/HandlersChain，示意性质；验证：不适用(源码示意)
- [x] `gin_Optimize_4` [伪代码] 非错误 — 前缀树 addRoute 为占位注释体（// 插入节点逻辑），源码示意；验证：不适用(源码示意)
- [x] `gin_Optimize_5` [伪代码] 非错误 — 二分查找示例引用 gin 内部 node/Params/HandlersChain，源码示意；验证：不适用(源码示意)
- [x] `gin_Optimize_6` [伪代码] 非错误 — 哈希表路由示例引用 gin 内部 node/HandlersChain，源码示意；验证：不适用(源码示意)

## gin/Request.md

- [x] `gin_Request_0` [片段] 非错误 — gin.Context 源码节选：Params/errorMsgs 是 gin 包内类型，块内注释「其他字段...」已明示为节选而非可运行程序；验证：不适用(实测 undefined: Params/errorMsgs，属源码节选预期)

## gin/Response.md

- [x] `gin_Response_8` [片段] 非错误 — 不改：7.4.1 已完整定义 MyRenderer（实现 render.Render 接口），本块是 c.Render 配合自定义渲染器的用法片段，正文有说明；验证：不适用(明示的片段)

## gin/Route.md

- [x] `gin_Route_0` [片段] 非错误 — 7 行 HTTP 方法注册形态演示：r 是 4.1 完整示例里的 gin.Default() 引擎，handler 为处理函数通配，紧随正文说明各方法签名，下一块即完整可运行程序，不修；验证：不适用(注册形态片段)
- [x] `gin_Route_2` [片段] 非错误 — 4.2.1 精确匹配的单条注册演示，r 沿用 4.1 完整示例中的引擎，不修；验证：不适用(单条注册片段)
- [x] `gin_Route_3` [片段] 非错误 — 4.2.2 路径参数（:name）注册演示，r 沿用上文完整示例，不修；验证：不适用(单条注册片段)
- [x] `gin_Route_4` [片段] 非错误 — 4.2.2 通配符（*filepath）注册演示，r 沿用上文完整示例，不修；验证：不适用(单条注册片段)
- [x] `gin_Route_5` [片段] 非错误 — 4.3 路由分组演示：v1/v2 分组写法是教学点，loginHandler/submitHandler 等处理函数在工程其他处定义，不修；验证：不适用(分组写法片段)
- [x] `gin_Route_6` [片段] 非错误 — 分组共享中间件演示：AuthRequired 中间件与 loginHandler 等在工程其他处定义，页面只讲 r.Group(", AuthRequired()) 的用法，不修；验证：不适用(中间件分组片段)
- [x] `gin_Route_7` [片段] 非错误 — 4.4.1 静态路由两条注册演示，homeHandler/loginHandler 在工程其他处定义，不修；验证：不适用(静态路由片段)
- [x] `gin_Route_8` [片段] 非错误 — 4.4.2 路径参数（:id）注册演示，r 沿用上文完整示例，不修；验证：不适用(单条注册片段)
- [x] `gin_Route_9` [片段] 非错误 — 4.4.2 通配符（*filepath）注册演示，r 沿用上文完整示例，不修；验证：不适用(单条注册片段)

## gin/Source.md

- [x] `gin_Source_0` [片段] 非错误 — 源码走读节选（标注 routergroup.go/gin.go）：方法挂在 gin 的 RouterGroup/Engine 上，离开 gin 包无法编译，补桩等于重写源码示例；验证：不适用(实测 undefined: RouterGroup 等，属源码节选预期)
- [x] `gin_Source_1` [片段] 非错误 — handleHTTPRequest 源码节选（标注 router.go），Engine/Context 由框架定义；验证：不适用(源码节选)
- [x] `gin_Source_10` [片段] 非错误 — Stream 节选（标注 context.go），io 语义靠注释说明；验证：不适用(源码节选)
- [x] `gin_Source_11` [片段] 已修 — Render 调用的 WriteJSON 是 gin render/json.go 同文件辅助函数（已对 gin v1.12.0 源码确认），块内补了一个节选实现（json.Marshal 后写入，注明省略 Content-Type），encoding/json 随之被真正使用；验证：PASS(编译运行通过)
- [x] `gin_Source_12` [片段] 非错误 — Status 节选（标注 context.go）；验证：不适用(源码节选)
- [x] `gin_Source_13` [片段] 非错误 — File 节选（标注 context.go）；验证：不适用(源码节选)
- [x] `gin_Source_15` [片段] 非错误 — errors.go 节选：ErrorType 在同文件其余部分定义，补桩会伪造 gin 源码；验证：不适用(实测 undefined: ErrorType，属源码节选预期)
- [x] `gin_Source_16` [类型] 已修 — 同 gin_Source_5：「应用代码」改为 gin.HandlerFunc 与 *gin.Context；验证：PASS(编译运行通过)
- [x] `gin_Source_2` [片段] 非错误 — Group 方法节选（标注 routergroup.go），函数体以注释说明，页面明示按源码走读；验证：不适用(源码节选)
- [x] `gin_Source_3` [片段] 非错误 — Use 方法节选（标注 routergroup.go），依赖 gin 未导出上下文；验证：不适用(源码节选)
- [x] `gin_Source_4` [片段] 非错误 — recovery.go 节选：RecoveryWithWriter/DefaultErrorWriter 是 gin 未导出成员，外部无法引用；验证：不适用(源码节选)
- [x] `gin_Source_5` [类型] 已修 — 块标注「应用代码」，却用无限定名的 HandlerFunc/Context，实际写不出来；改为 gin.HandlerFunc 与 *gin.Context，import 由验证器自动补；验证：PASS(编译运行通过)
- [x] `gin_Source_6` [片段] 非错误 — Next 方法节选（标注 context.go），Context 类型未随块给出；验证：不适用(源码节选)
- [x] `gin_Source_7` [缺import] 已修 — 块内用到 http.Request/http.ResponseWriter 却没有任何 import，补 import "net/http" 后该节选自含可编译（Context 结构体与 JSON 方法本就在块内）；验证：PASS(编译运行通过)
- [x] `gin_Source_8` [片段] 非错误 — BindJSON 节选（标注 context.go），Context 未随块给出；验证：不适用(源码节选)
- [x] `gin_Source_9` [片段] 非错误 — Next 节选（标注 context.go）；验证：不适用(源码节选)

## gin/Use.md

- [x] `gin_Use_0` [片段] 已修 — 补 r := gin.Default() 与 handler 定义，四行注册原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_1` [片段] 已修 — 块首补 r := gin.Default()，原注册代码不动；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_10` [片段] 已修 — 块首补 r := gin.Default()，返回 JSON 示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_11` [片段] 已修 — 块首补 r := gin.Default()，返回 XML 示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_12` [片段] 已修 — 块首补 r := gin.Default()，AbortWithStatusJSON 示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_14` [未使用] 已修 — 补一行 r.GET("/ping", ...) 用起 r；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_15` [未使用] 已修 — 补一行 r.GET("/ping", ...) 用起 r；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_16` [片段] 已修 — 块首补 r := gin.New()，单独使用 Recovery 中间件的写法原样保留；验证：PASS(gin 中间件挂载，退出码 0)
- [x] `gin_Use_2` [片段] 已修 — 块首补 r := gin.Default()，动态路由示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_3` [片段] 已修 — 块首补 r := gin.Default()，查询参数示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_4` [未使用] 已修 — 补一行 r.GET("/ping", ...) 用起 r，演示默认中间件引擎的用法；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_6` [片段] 已修 — 按 gin 官方中间件工厂写法补 AuthRequired() gin.HandlerFunc 定义与 r := gin.New()，endpoint 处理函数就地定义，原 Group/POST 代码不动；验证：PASS(gin 路由组注册，退出码 0)
- [x] `gin_Use_7` [片段] 已修 — 块首补 r := gin.Default()，表单解析示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_8` [语法] 已修 — type Login 与 r.POST 混在顶层导致语法错；改为完整程序（package/import/类型定义/func main 内注册路由），教学代码逐字保留；验证：PASS(gin JSON 绑定示例，退出码 0)
- [x] `gin_Use_9` [片段] 已修 — 块首补 r := gin.Default()，返回字符串示例原样保留；验证：PASS(gin engine 创建，退出码 0)
- [x] `gin_Use_prose` [陈述] 已修 — 3.2 正文与方法名统一为 c.ShouldBindJSON（返回 error 由调用方处理，与示例的错误处理一致）；验证：验证（gin 源码 bind.go 对照；示例块编译见 gin_Use_8）

## gin/advanced.md

- [x] `gin_advanced_0` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测（GORM 连接块）；验证：PASS（exit 0）
- [x] `gin_advanced_1` [片段] 非错误 — 集成步骤第 2 步调用第 1 步块定义的 SetupDatabase()，同节分步展示，页面有说明；验证：不适用(SetupDatabase 定义于同节上一块)
- [x] `gin_advanced_2` [依赖缺失] 已修 — 补 import "github.com/golang-jwt/jwt/v5"（依赖已入验证环境）+ 缩进修复；验证：PASS（exit 0；签发+解析真跑 jwtrun：token 生成、parsed.Valid=true）；需要依赖 github.com/golang-jwt/jwt/v5 v5.3.1
- [x] `gin_advanced_3` [依赖缺失] 已修 — 同上补 jwt 导入 + 缩进修复；验证：PASS（exit 0；真跑：篡改 token 解析报错、bad.Valid=false）；需要依赖 github.com/golang-jwt/jwt/v5 v5.3.1
- [x] `gin_advanced_4` [递进片段] 页面级 — AuthMiddleware+main 调用上一块定义的 ParseToken，同节分步展示；组合程序编译实测；验证：PASS（JWTALL-BUILD-OK，三块合一编译通过）
- [x] `gin_advanced_5` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测（WebSocket 块）；验证：PASS（编译通过+服务启动实测（r.Run() 常驻，按超时收尾））

## idioms/BlankIdentifier.md

- [x] `idioms_BlankIdentifier_1` [其他] 已修 — 补示例数据 numbers := []int{1, 2, 3}，range 忽略下标的用法保持原样；验证：PASS(编译运行通过，无输出)
- [x] `idioms_BlankIdentifier_3` [语法] 已修 — var 声明与 if 语句混排使验证器把语句落到函数体外，首行改为 v := interface{}("hello")，断言用法原样保留；验证：PASS(输出: v 是字符串)

## idioms/Labels.md

- [x] `idioms_Labels_0` [伪代码] 非错误 — 「标签的语法示例」占位符片段（LabelName: + 注释行），页面明示只展示标签语法形态；验证：不适用(语法占位符)

## idioms/ShortVarDecl.md

- [x] `idioms_ShortVarDecl_0` [伪代码] 非错误 — 「基本语法」小节展示 := 的抽象形式（variableName/expression 为占位符），紧跟的具体示例块可编译运行；抽象语法行非可运行代码，补全反而破坏教学意图；验证：不适用(语法占位符)

## introduction/Feature.md

- [x] `introduction_Feature_2` [未使用] 已修 — 类型推断示例 x/name 声明后未使用，补 fmt.Println(x, name)；验证：PASS(10 Go)
- [x] `introduction_Feature_4` [常驻服务] 非错误 — http.HandleFunc + ListenAndServe 常驻 Web 服务示例；验证：编译 PASS，常驻设计

## io/Advanced.md

- [x] `io_Advanced_3` [需真实服务] 非错误 — confluent-kafka-go 消费者 for 循环示例，编译通过；无 broker 时常驻重连；验证：不适用(编译 PASS；运行需真实 Kafka broker)

## io/EfficientIO.md

- [x] `io_EfficientIO_3` [服务型] 非错误 — socket 服务示例常驻；:8080 被本机 Docker 端口映射占用属环境冲突；验证：PASS(端口空闲时实测启动成功，12s 常驻不退)

## io/ModIO.md

- [x] `io_ModIO_14` [片段] 非错误 — io.TeeReader 的 API 签名清单，同上；验证：不适用(API 签名清单，配套示例块已可运行)
- [x] `io_ModIO_16` [片段] 非错误 — io.Copy 的 API 签名清单，同上；验证：不适用(API 签名清单，配套示例块已可运行)
- [x] `io_ModIO_18` [片段] 非错误 — io.ReadAll 的 API 签名清单，同上；验证：不适用(API 签名清单，配套示例块已可运行)
- [x] `io_ModIO_20` [片段] 非错误 — io.ReadFull 的 API 签名清单，同上；验证：不适用(API 签名清单，配套示例块已可运行)
- [x] `io_ModIO_24` [片段] 非错误 — strings.NewReader 签名清单，块内注释已明示「标准库 strings.Reader 的简化摘录」；验证：不适用(明示的摘录)
- [x] `io_ModIO_7` [片段] 非错误 — io.Pipe 的 API 签名清单（package io + go doc 风格函数签名，无函数体），页面结构是每个签名块紧跟一个可运行「示例」块，签名本身即教学意图；验证：不适用(API 签名清单，配套示例块已可运行)

## io/ModOS.md

- [x] `io_ModOS_13` [runtime示意] 非错误 — 标准库签名摘要（package path / func Join(elem ...string) string），godoc 式声明展示，讲的是库的接口形态不是可运行程序；验证：不适用(实测 missing function body，属签名展示预期)
- [x] `io_ModOS_15` [runtime示意] 非错误 — 同上（package filepath / func Abs 签名）；验证：不适用(签名展示)
- [x] `io_ModOS_17` [runtime示意] 非错误 — 同上（package path / func Base 签名）；验证：不适用(签名展示)
- [x] `io_ModOS_19` [runtime示意] 非错误 — 同上（package path / func Dir 签名），其下紧跟可运行的示例块；验证：不适用(签名展示)

## io/ModPath.md

- [x] `io_ModPath_0` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)
- [x] `io_ModPath_10` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)
- [x] `io_ModPath_2` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)
- [x] `io_ModPath_4` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)
- [x] `io_ModPath_6` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)
- [x] `io_ModPath_8` [片段] 非错误 — `package path` + 无函数体的标准库 API 签名清单（go doc 风格），每个签名块紧跟可运行「示例」块与「输出」，签名本身即教学内容；验证：不适用(相邻示例块已实测 PASS 且输出与「输出」块逐行一致)

## io/Utils.md

- [x] `io_Utils_2` [常驻服务] 非错误 — pprof 演示：6060 端口 pprof 服务 + select{} 常驻，教学意图；验证：编译 PASS，常驻设计

## log/Aggregation.md

- [x] `log_Aggregation_0` [需真实服务] 非错误 — fluent-logger-golang 钩子示例，编译通过；裸跑连不上 Fluentd(:24224) 而退出；验证：不适用(编译 PASS；运行需真实 Fluentd 服务，connection refused 属预期)

## log/LibLog.md

- [x] `log_LibLog_1` [片段] 非错误 — 1.2 延续 1.1 程序的 logger 变量做级别与钩子演示，CustomHook 是钩子类型占位（页内未给实现），代写 Hook 接口实现超出本节范围；验证：不适用(logger/CustomHook 属跨块引用与占位类型)
- [x] `log_LibLog_10` [缺import] 已修 — zerolog 一行链式调用包成完整 main 并显式 import github.com/rs/zerolog/log（normalize 的 ALIAS 会误配成标准库 log 导致 undefined: log.Info）；验证：PASS(exit 0，JSON 日志输出到 stderr)
- [x] `log_LibLog_11` [缺import] 已修 — 两行 JSON 输出示例包成 main，补 os 与 zerolog/log import；原报错 log.Logger 非表达式/log.Output 参数不足是误配标准库 log 的假象；验证：PASS(JSON 日志输出到 stdout)
- [x] `log_LibLog_2` [片段] 非错误 — 1.3 是 1.4 实践案例的节选（同一 SetFormatter/OpenFile/SetOutput 逻辑），完整可运行版本在本页 1.4 块；验证：不适用(1.4 完整块 fence 54 实测 PASS)
- [x] `log_LibLog_5` [未使用] 已修 — 单行 zap.NewProduction(zap.WithCaller(false)) 包成完整 main，defer logger.Sync() 并 logger.Info 用起 logger；验证：PASS(exit 0，zap 默认输出到 stderr)
- [x] `log_LibLog_6` [片段] 非错误 — 2.3 结构化日志一行调用延续 2.1 块的 logger，完整可运行版本在本页 2.5 实践案例块；验证：不适用(2.5 完整块 fence 146 上方 2.1 fence 89 实测 PASS)
- [x] `log_LibLog_7` [缺import] 已修 — config 构建四行本身自包含，缺 package/import 包裹；补 package main 与 import go.uber.org/zap 包成完整程序；验证：PASS(JSON 日志输出到 stdout)

## log/ModLog.md

- [x] `log_ModLog_0` [未使用] 已修 — 删除未使用的 "os" import；验证：PASS(编译运行退出码 0)
- [x] `log_ModLog_1` [类型] 已修 — slog.NewJSONHandler 缺第二个参数，补 nil（标准写法）；验证：PASS(JSON INFO 日志一行)
- [x] `log_ModLog_11` [片段] 已修 — 裸 logger 语句片段，补 package main/imports/func main 及 logger 初始化；验证：PASS(JSON INFO 日志)
- [x] `log_ModLog_13` [类型] 已修 — NewJSONHandler 缺第二参，补 nil；验证：PASS(编译运行退出码 0)
- [x] `log_ModLog_15` [类型] 已修 — NewJSONHandler 缺第二参，补 nil；验证：PASS(并发 JSON 日志)
- [x] `log_ModLog_16` [未使用] 已修 — 删除未使用的 "os" import；块为 package logutil 库包，go build 通过，go run 对库包不适用；验证：BUILD OK(库包无 main，go run 报 not a main package 属预期)
- [x] `log_ModLog_17` [片段] 非错误 — 页面 8.2 明示 logutil 包来自 8.1（NewLogger 返回 *log.Logger，有 Println），文档自洽；验证环境的同名桩模块只有空 Logger 结构体（无任何方法），无法反映真实包，非文档错误；验证：不适用(依赖桩模块差异)
- [x] `log_ModLog_2` [片段] 已修 — API 演示片段，补 package main/import "log"/func main；log.Fatal/log.Panic 会 os.Exit(1)/panic 使程序非零退出，改为注释保留讲解；验证：PASS(两条 log 输出)
- [x] `log_ModLog_3` [片段] 已修 — 裸 logger 语句片段（含未定义的 err），补完整程序：errors.New 造 err、初始化 logger；验证：PASS(INFO/WARN/ERROR 三条 JSON 日志)
- [x] `log_ModLog_5` [片段] 已修 — 裸 logger 片段补完整程序，NewJSONHandler 补 nil；验证：PASS(JSON INFO 日志)
- [x] `log_ModLog_6` [未使用] 已修 — 删除未使用的 "fmt"、"os" import；验证：PASS(编译运行退出码 0)
- [x] `log_ModLog_7` [片段] 已修 — 裸 logger 语句片段补完整程序（package main + 初始化 logger）；验证：PASS(INFO/WARN/ERROR 三条 JSON 日志)
- [x] `log_ModLog_9` [片段] 已修 — 输出重定向 slog 片段补完整程序（log/log/slog/os import + func main），NewJSONHandler 补 nil；验证：PASS(JSON 日志写入 app.log)

## math/Calc.md

- [x] `math_Calc_0` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；牛顿迭代迭代过程；验证：PASS（x0=0.60 x1=2.80）
- [x] `math_Calc_1` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；定积分；验证：PASS（4.000010000027032）
- [x] `math_Calc_2` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；级数求和；验证：PASS（0.33335000000000004）
- [x] `math_Calc_3` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；逐步开方逼近；验证：PASS（1.414213562373095）

## math/LinearAlgebra.md

- [x] `math_LinearAlgebra_1` [语法] 已修 — 块以 import 开头且未声明 package，归一化后 import 落进函数体；块首补 package main，并补上一块的 Vector2D 类型定义使块自洽；验证：PASS(向量长度: 5)
- [x] `math_LinearAlgebra_2` [注释错误] 已修 — 矩阵加法/乘法注释输出改为实测值 {6 8 10 12}、{19 22 43 50}；验证：PASS（verify_one fence 73）
- [x] `math_LinearAlgebra_3` [注释错误] 已修 — 矩阵转置注释输出改为实测值 {1 3 2 4}；验证：PASS（verify_one fence 111）
- [x] `math_LinearAlgebra_4` [语法] 已修 — 块首补 package main（gonum 已在验证环境依赖中，无需新增依赖）；验证：PASS(解向量: x0=0.60, x1=2.80)
- [x] `math_LinearAlgebra_5` [语法] 已修 — 块首补 package main；验证：PASS(特征值: [2.381966011250105 4.618033988749895])

## math/MathFunc.md

- [x] `math_MathFunc_0` [语法] 已修 — 块缺 package main 导致 import 被包进函数体；块首补 package main；验证：PASS(输出 绝对值: 3.14)
- [x] `math_MathFunc_1` [语法] 已修 — 同上，补 package main；验证：PASS(输出 幂运算: 8)
- [x] `math_MathFunc_2` [语法] 已修 — 同上，补 package main；验证：PASS(输出 平方根: 4)
- [x] `math_MathFunc_3` [语法] 已修 — 同上，补 package main；实测正切输出 1 与注释一致；验证：PASS(输出 正弦 0.7071067811865475/余弦 .../正切 1)
- [x] `math_MathFunc_4` [语法] 已修 — 同上，补 package main；验证：PASS(输出 指数函数: 7.38905609893065)
- [x] `math_MathFunc_5` [语法] 已修 — 同上，补 package main；验证：PASS(输出 自然对数/常用对数)
- [x] `math_MathFunc_6` [语法] 已修 — 同上，补 package main；验证：PASS(输出 双曲正弦/余弦/正切)
- [x] `math_MathFunc_7` [语法] 已修 — 同上，补 package main；验证：PASS(输出 随机整数/随机浮点数)
- [x] `math_MathFunc_heading` [陈述] 已修 — 小节标题改「特殊函数（`math` 包）」；正文修正：标准库 math 提供 Gamma/Lgamma/Erf/Erfc，没有 Beta，需要时用 gonum（本机工具链 go doc math 对照核实）；验证：PASS（声明的四个函数均存在于本机 math 包，Beta 不存在）

## math/Optimize.md

- [x] `math_Optimize_1` [语法] 已修 — 块首补 package main；验证：PASS(根: 1.414213562373095)

## math/Science.md

- [x] `math_Science_3` [语法] 已修 — gonum/mat 示例缺 package main；块首补 package main（依赖已在 mod 中）；验证：PASS(输出 矩阵乘法结果 19/22/43/50)
- [x] `math_Science_4` [语法] 已修 — sha256 示例缺 package main；块首补 package main；验证：PASS(输出 SHA-256: b94d27b9...)

## math/Statistics.md

- [x] `math_Statistics_0` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；基础统计；验证：PASS（均值 3）
- [x] `math_Statistics_1` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；正态分布概率密度；验证：PASS（0.24197072451914337（与注释声称值一致））
- [x] `math_Statistics_2` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；中位数/分位数；验证：PASS（5.3）
- [x] `math_Statistics_5` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测；线性回归；验证：PASS（y = 2.00x + 0.00（与注释一致））

## middleware/ApacheKafka.md

- [x] `middleware_ApacheKafka_0` [需真实服务] 非错误 — sarama 生产者示例，编译通过；裸跑连不上 Kafka(:9092) 而失败；验证：不适用(编译 PASS；运行需真实 Kafka broker)
- [x] `middleware_ApacheKafka_1` [需真实服务] 非错误 — 同页第二段生产者示例，同上；验证：不适用(编译 PASS；运行需真实 Kafka broker)

## mod/Get.md

- [x] `mod_Get_0` [伪代码] 非错误 — 块内容是 go.mod 文件示例（module/go/require），是构建配置不是 Go 源码，无法也不应改写成可编译程序；fence 语言标记按红线不动；验证：不适用(实测报 unexpected name your_module_name，属配置文件示例预期)

## mod/Import.md

- [x] `mod_Import_4` [伪代码] 非错误 — 不改：块内是 go.mod 配置文件内容（module/require），页面明示「go.mod 文件」，不是 Go 源码；围栏语言标记按红线不动；验证：不适用(配置文件展示，非 Go 程序)

## mod/Mod.md

- [x] `mod_Mod_0` [其他] 非错误 — 围栏内容是 go.mod 文件内容而非 Go 程序，小节标题「查看 go.mod 文件」已明示；围栏语言标记按红线不动；验证：不适用(配置文件展示)

## mod/Pkg.md

- [x] `mod_Pkg_1` [其他] 已修 — 文档未改：main.go 块调用的 Subtract 在同页 mathutils.go 块有定义，而桩模块 mod/stub/path/to/your/project/mathutils 只实现了 Add，已同步补上 Subtract 使桩与文档一致；验证：PASS(Sum: 15 / Difference: 5)
- [x] `mod_Pkg_2` [其他] 非错误 — 围栏展示的是 go.mod 文件内容（module/go 指令），是清单文件清单不是 Go 源码，不能也不应按 Go 程序编译；验证：不适用(go.mod 文件内容展示)
- [x] `mod_Pkg_3` [其他] 已修 — 文档未改：桩模块 mod/stub/dependency 的 SomeFunction 无返回值，与文档 result := dependency.SomeFunction() 的用法矛盾，桩改为返回 string（文档把该包描述为 go get 的虚构三方包）；验证：PASS(输出 some result)

## mod/Work.md

- [x] `mod_Work_0` [其他] 非错误 — 块内容是 go.work 配置文件（go 1.20 / use 指令），不是 Go 源程序；围栏语言标记按红线不动；验证：不适用(go.work 配置文件内容示意)
- [x] `mod_Work_1` [其他] 非错误 — 块内容是 go.work 配置文件（go 1.20 / use 指令），不是 Go 源程序；围栏语言标记按红线不动；验证：不适用(go.work 配置文件内容示意)
- [x] `mod_Work_2` [其他] 非错误 — 块内容是 go.work 配置文件（go 1.20 / use 指令），不是 Go 源程序；围栏语言标记按红线不动；验证：不适用(go.work 配置文件内容示意)
- [x] `mod_Work_3` [片段] 非错误 — module1/main.go 与下一块 module2/library.go（定义 Greet() string）配套，页面明示这是同一工作区的两个模块；报错是因为验证环境里 example.com/module2 是桩模块、桩的 Greet(name string) 无返回值，签名差异属验证环境，页面自身自洽；验证：不适用(与下块配套；桩模块签名差异)

## naming/Naming.md

- [x] `naming_Naming_0` [伪代码] 非错误 — 命名规范页用 `{ ... }` 省略函数体/字段的示意写法，讲命名风格而非可运行程序（b08 ShortVarDecl/const_Const 同口径）；验证：不适用(伪代码省略体)
- [x] `naming_Naming_1` [伪代码] 非错误 — 命名规范页用 `{ ... }` 省略函数体/字段的示意写法，讲命名风格而非可运行程序（b08 ShortVarDecl/const_Const 同口径）；验证：不适用(伪代码省略体)
- [x] `naming_Naming_5` [伪代码] 非错误 — 命名规范页用 `{ ... }` 省略函数体/字段的示意写法，讲命名风格而非可运行程序（b08 ShortVarDecl/const_Const 同口径）；验证：不适用(伪代码省略体)

## net/Advanced.md

- [x] `net_Advanced_0` [常驻服务] 非错误 — select+FdSet echo 服务器，常驻；本机 :8080 被占导致的 exit1 为环境性；验证：换端口 :18080 实测监听成功
- [x] `net_Advanced_1` [服务型] 非错误 — TCP/HTTP 服务示例，r.Run/ListenAndServe 常驻；终扫期间 :8080 被本机 Docker 容器端口映射占用致 bind 失败，属环境冲突；验证：PASS(端口空闲时实测启动成功，12s 常驻不退)
- [x] `net_Advanced_2` [常驻服务] 非错误 — epoll echo 服务器，常驻；同上；验证：换端口 :18080 实测监听成功

## net/Netpoll.md

- [x] `net_Netpoll_0` [runtime示意] 非错误 — 页面明示「摘录的是 Go 1.27 源码（精简注释版）」，sys.NotInHeap/mutex/timer 为运行时内部标识符，讲运行时源码而非可运行程序；验证：不适用(runtime 源码节选)
- [x] `net_Netpoll_1` [runtime示意] 非错误 — netpollopen 为 runtime/netpoll_epoll.go 源码节选，linux/taggedPointerPack/epfd 均为运行时内部标识；验证：不适用(runtime 源码节选)
- [x] `net_Netpoll_2` [runtime示意] 非错误 — netpoll 轮询函数为运行时源码节选，gList/_EINTR/throw 等运行时内部标识；验证：不适用(runtime 源码节选)
- [x] `net_Netpoll_3` [runtime示意] 非错误 — netpollready 为运行时源码节选，g/gList/netpollunblock/pollDesc 为运行时内部标识；验证：不适用(runtime 源码节选)

## net/Socket.md

- [x] `net_Socket_4` [常驻服务] 非错误 — UDP echo 服务端常驻等待报文；验证：编译 PASS，常驻设计

## oop/Interface.md

- [x] `oop_Interface_3` [片段] 已修 — 「示例：接口实现」块引用了紧邻上一块定义的 Speaker 却未携带定义，按规则「与相邻块合并」在块首补上 type Speaker interface { Speak() string } 四行，其余不动；验证：PASS(Hi, I'm Alice)

## oop/InterfaceImpl.md

- [x] `oop_InterfaceImpl_0` [runtime示意] 非错误 — 接口底层结构简化示意，正文已注明真实实现是 runtime 的 eface/iface/itab，typeDescriptor 在下文第 2 节定义；验证：不适用(runtime 内部结构示意)

## oop/Methods.md

- [x] `oop_Methods_0` [伪代码] 非错误 — 「方法的定义语法如下」的语法模板，receiver/ReceiverType/MethodName/params/ReturnType 为占位符，下方 bullet 逐项解释；验证：不适用(语法模板占位符)

## oop/PointerReceiver.md

- [x] `oop_PointerReceiver_0` [伪代码] 非错误 — 「方法定义语法」模板，ReceiverType/MethodName/params/ReturnType 为占位符，块下逐项注释解释，属语法示意；验证：不适用(语法模板)

## oop/Poly.md

- [x] `oop_Poly_1` [runtime示意] 非错误 — 块内注释已写明「简化示意……真实实现见 runtime 包中的 eface、iface 和 itab」，methodTable 紧随其后的下一块定义；验证：不适用(BUILD-FAIL: undefined: methodTable)

## oop/TypeAssertion.md

- [x] `oop_TypeAssertion_0` [伪代码] 非错误 — 单行语法演示 value, ok := x.(T)，正文紧随其后逐项解释 x/T/value/ok，属语法讲解占位；验证：不适用(declared and not used: value/ok、undefined: x)
- [x] `oop_TypeAssertion_3` [伪代码] 非错误 — 单行演示裸断言 s := i.(string)（失败会 panic）的写法，i 为讲解用接口变量；验证：不适用(declared and not used: s、undefined: i)
- [x] `oop_TypeAssertion_4` [伪代码] 非错误 — 演示 ok 形式的失败处理分支骨架，注释即处理位置；验证：不适用(declared and not used: s、undefined: i)

## operator/Receiver.md

- [x] `operator_Receiver_0` [伪代码] 非错误 — 「基本语法」模板：ReceiverType/params/ReturnType/method body 均为占位符，正文 bullet 逐项解释；验证：不适用(语法占位符)

## operator/TypeAssertion.md

- [x] `operator_TypeAssertion_0` [伪代码] 非错误 — 基本语法式 value, ok := interface.(T)，interface/T 为语法占位符（下方逐项解释各符号含义），与规则中语法讲解占位符同类；验证：不适用(语法记法展示)

## redis/Bitmap.md

- [x] `redis_Bitmap_0` [依赖缺失] 已修 — 步骤 1 import 块补 "fmt"（步骤 3-5 用到 fmt，整页拼装才能编译）；整页四步拼装后对本地 Redis 实测；验证：PASS（Bit value: 1 / Bit count: 1 / First set bit position: 10）
- [x] `redis_Bitmap_1` [片段] 非错误 — 步骤 2「设置位」给出 example() 的操作体，redis/ctx/连接由步骤 1 块提供，运行需真实 Redis；扫描报错本身是抽块工具不识别列表内缩进围栏的顶层声明（步骤 1 块实测 PASS）；验证：不适用(跨块引用+需 Redis 服务)
- [x] `redis_Bitmap_2` [片段] 非错误 — 步骤 3「获取位」同上；验证：不适用(跨块引用+需 Redis 服务)
- [x] `redis_Bitmap_3` [片段] 非错误 — 步骤 4「统计位数」同上（步骤 3-5 用到 fmt，见页面级备注）；验证：不适用(跨块引用+需 Redis 服务)
- [x] `redis_Bitmap_4` [片段] 非错误 — 步骤 5「查找位」同上；验证：不适用(跨块引用+需 Redis 服务)

## redis/Geospatial.md

- [x] `redis_Geospatial_1` [片段] 非错误 — 第 2 步「添加地理位置」：rdb/ctx 定义于第 1 步完整程序块（含 var ctx = context.Background()），本块是同一 example 函数的分步展示；列表缩进还使验证器把缩进 func 误判为语法错，非文档本身缺陷，不修；验证：不适用(同页第 1 步块定义 rdb/ctx 的分步片段)
- [x] `redis_Geospatial_2` [片段] 非错误 — 第 3 步「查询地理位置」GeoPos 分步片段，同 redis_Geospatial_1，不修；验证：不适用(分步片段)
- [x] `redis_Geospatial_3` [片段] 非错误 — 第 4 步「计算距离」GeoDist 分步片段，同 redis_Geospatial_1，不修；验证：不适用(分步片段)
- [x] `redis_Geospatial_4` [片段] 非错误 — 第 5 步「查找半径内的地点」GeoRadius 分步片段，同 redis_Geospatial_1，不修；验证：不适用(分步片段)

## redis/HyperLogLog.md

- [x] `redis_HyperLogLog_1` [片段] 非错误 — 不改：步骤2「添加元素」：PFAdd 的 example 函数体，依赖的 redis.Client/ctx/import 都在步骤1「连接 Redis」的完整程序里（该块实测 PASS）；报错是列表缩进 fence 被验证器包进 func main 的伪语法错；验证：不适用(片段;同页步骤1完整程序实测 PASS)
- [x] `redis_HyperLogLog_2` [片段] 非错误 — 不改：步骤3「获取基数」：PFCount 的 example 函数体，依赖的 redis.Client/ctx/import 都在步骤1「连接 Redis」的完整程序里（该块实测 PASS）；报错是列表缩进 fence 被验证器包进 func main 的伪语法错；验证：不适用(片段;同页步骤1完整程序实测 PASS)
- [x] `redis_HyperLogLog_3` [片段] 非错误 — 不改：步骤4「合并 HyperLogLog」：PFMerge 的 example 函数体，依赖的 redis.Client/ctx/import 都在步骤1「连接 Redis」的完整程序里（该块实测 PASS）；报错是列表缩进 fence 被验证器包进 func main 的伪语法错；验证：不适用(片段;同页步骤1完整程序实测 PASS)

## redis/List.md

- [x] `redis_List_1` [片段] 非错误 — example(rdb) 各操作块与「1. 连接 Redis」块（定义 ctx、rdb）配套，页尾注明「这几段合起来就是前面场景的 Go 写法」；syntax error 源于列表内缩进块被误包进 func main，属工具产物；验证：不适用(明示片段；缩进列表块的验证器伪错)
- [x] `redis_List_2` [片段] 非错误 — example(rdb) 各操作块与「1. 连接 Redis」块（定义 ctx、rdb）配套，页尾注明「这几段合起来就是前面场景的 Go 写法」；syntax error 源于列表内缩进块被误包进 func main，属工具产物；验证：不适用(明示片段；缩进列表块的验证器伪错)
- [x] `redis_List_3` [片段] 非错误 — example(rdb) 各操作块与「1. 连接 Redis」块（定义 ctx、rdb）配套，页尾注明「这几段合起来就是前面场景的 Go 写法」；syntax error 源于列表内缩进块被误包进 func main，属工具产物；验证：不适用(明示片段；缩进列表块的验证器伪错)
- [x] `redis_List_4` [片段] 非错误 — example(rdb) 各操作块与「1. 连接 Redis」块（定义 ctx、rdb）配套，页尾注明「这几段合起来就是前面场景的 Go 写法」；syntax error 源于列表内缩进块被误包进 func main，属工具产物；验证：不适用(明示片段；缩进列表块的验证器伪错)

## redis/Set.md

- [x] `redis_Set_1` [片段] 非错误 — 与第 1 块「连接 Redis」配对：example 函数签名与 ctx 在首块定义，本块给出 example 的操作体；且需真实 Redis 服务，补齐样板等于重写示例，判递进片段；验证：不适用(BUILD-FAIL: 缩进误包 main 后 example 成嵌套函数)
- [x] `redis_Set_2` [片段] 非错误 — 与第 1 块「连接 Redis」配对：example 函数签名与 ctx 在首块定义，本块给出 example 的操作体；且需真实 Redis 服务，补齐样板等于重写示例，判递进片段；验证：不适用(BUILD-FAIL: 同上)
- [x] `redis_Set_3` [片段] 非错误 — 与第 1 块「连接 Redis」配对：example 函数签名与 ctx 在首块定义，本块给出 example 的操作体；且需真实 Redis 服务，补齐样板等于重写示例，判递进片段；验证：不适用(BUILD-FAIL: 同上)
- [x] `redis_Set_4` [片段] 非错误 — 与第 1 块「连接 Redis」配对：example 函数签名与 ctx 在首块定义，本块给出 example 的操作体；且需真实 Redis 服务，补齐样板等于重写示例，判递进片段；验证：不适用(BUILD-FAIL: 同上)
- [x] `redis_Set_5` [片段] 非错误 — 与第 1 块「连接 Redis」配对：example 函数签名与 ctx 在首块定义，本块给出 example 的操作体；且需真实 Redis 服务，补齐样板等于重写示例，判递进片段；验证：不适用(BUILD-FAIL: 同上)

## redis/SortedSet.md

- [x] `redis_SortedSet_1` [片段] 非错误 — 「添加元素」是步骤 1「连接 Redis」环境中 example 函数体的替换内容（redis 导入、ctx、rdb 在步骤 1 定义）；报错本身是列表缩进被验证器误判为语法错；验证：不适用(分步片段，环境在步骤 1)
- [x] `redis_SortedSet_2` [片段] 非错误 — 「获取所有元素」同上，分步展示 example 函数体；验证：不适用(分步片段)
- [x] `redis_SortedSet_3` [片段] 非错误 — 「检查元素是否存在」同上，分步展示 example 函数体；验证：不适用(分步片段)
- [x] `redis_SortedSet_4` [片段] 非错误 — 「删除元素」同上，分步展示 example 函数体；验证：不适用(分步片段)
- [x] `redis_SortedSet_5` [片段] 非错误 — 「范围查询」同上，分步展示 example 函数体；验证：不适用(分步片段)

## redis/Streams.md

- [x] `redis_Streams_0` [依赖缺失] 已修 — 步骤 1 import 块补 "fmt"；整页四步拼装（XAdd→XRange→消费者组）对本地 Redis 实测；验证：PASS（Message ID/Fields 输出与写入内容一致，组消费投递同一条消息）
- [x] `redis_Streams_1` [片段] 非错误 — 步骤 2 example() 的 XAdd 操作体，redis/ctx 由步骤 1 块提供，需真实 Redis；验证：不适用(跨块引用+需 Redis 服务)
- [x] `redis_Streams_2` [片段] 非错误 — 步骤 3 XRange 操作体（用 fmt.Println，见页面级备注）；验证：不适用(跨块引用+需 Redis 服务)
- [x] `redis_Streams_3` [片段] 非错误 — 步骤 4 XReadGroup 操作体；验证：不适用(跨块引用+需 Redis 服务)

## regex/Debug.md

- [x] `regex_Debug_0` [未使用] 已修 — 编译失败示范块中 re 声明未用：块尾补 `_ = re // 编译失败时 re 为 nil，此处仅占位`，错误处理逻辑不变；验证：PASS(Regex compilation error: error parsing regexp: missing closing ): `(abc`)
- [x] `regex_Debug_1` [缺import] 已修 — 测试函数片段缺 import：块首补 import ("regexp" "testing")，TestRegex 函数体与断言不变；验证：PASS(无输出，退出码 0)

## regex/Lib.md

- [x] `regex_Lib_0` [片段] 非错误 — 不改：「导入」小节的单行 import 示意，正文紧接介绍 *regexp.Regexp；验证：不适用(明示的导入示意)
- [x] `regex_Lib_1` [片段] 非错误 — 不改：MustCompile 用法速查单行，`pattern` 是占位符（同「条件表达式」类），re 由本块引入供全页后续块使用；验证：不适用(速查占位示意)
- [x] `regex_Lib_10` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_11` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_12` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_13` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_14` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_15` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_16` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_17` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_18` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_19` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_2` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_20` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_21` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_3` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_4` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_5` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_6` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_7` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_8` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)
- [x] `regex_Lib_9` [片段] 非错误 — 不改：regexp 包 API 速查单行（MatchString/FindAllString/ReplaceAll* 等），re 在上方 MustCompile 块定义，每块前有对应方法说明；验证：不适用(速查示意片段)

## start/Hello.md

- [x] `start_Hello_0` [片段] 非错误 — 前次扫描 build-fail 为目录缺失中间态；桩模块补齐后实测通过；验证：PASS
- [x] `start_Hello_2` [片段] 非错误 — 同上；验证：PASS

## sync/CriticalSection.md

- [x] `sync_CriticalSection_1` [片段] 非错误 — 「代码解释」第 1 条，单行节选自上方完整可运行示例（fence 11）中的定义；验证：不适用(解释性节选，完整程序在上方)
- [x] `sync_CriticalSection_2` [片段] 非错误 — 「代码解释」第 2 条，increment 函数临界区三行的节选；验证：不适用(解释性节选)
- [x] `sync_CriticalSection_3` [片段] 非错误 — 「代码解释」第 3 条，main 函数节选，increment/counter 在上方完整示例中定义；验证：不适用(解释性节选)

## sync/Mutex.md

- [x] `sync_Mutex_1` [片段] 非错误 — 「代码解释」小节第 1 段，逐段引用上方完整示例（该完整示例实测 PASS 输出 Final Counter: 10000）；片段嵌在有序列表内必须保持缩进，单独抽出才报 unused；验证：不适用(节选自同页可运行示例)
- [x] `sync_Mutex_2` [片段] 非错误 — 「代码解释」第 2 段 increment 片段，counter/mu 定义在上方完整示例中；验证：不适用(节选自同页可运行示例)
- [x] `sync_Mutex_3` [片段] 非错误 — 「代码解释」第 3 段 main 片段，同上；验证：不适用(节选自同页可运行示例)

## sync/MutualLock.md

- [x] `sync_MutualLock_2` [片段] 已修 — 成对加锁惯用法示例缺 mu 声明，补一行 var mu sync.Mutex，Lock/defer Unlock 两行原样保留；验证：PASS(空输出，退出 0)
- [x] `sync_MutualLock_3` [缩进] 已修 — 列表内围栏渲染修复：围栏内容恢复到与围栏同缩进（此前批次改「顶格」会让代码块渲染为空、正文逃逸）；语义不动，在去缩进副本上 normalize 后实测（Counter/Inc 块）；验证：PASS（exit 0）

## sync/REMutex.md

- [x] `sync_REMutex_1` [片段] 非错误 — 「代码解释」小节把上方完整示例逐段摘出讲解，本块与完整程序中的 var 声明逐字一致；完整程序（本页首块）实测 PASS；验证：不适用(明示片段，完整程序已 PASS)
- [x] `sync_REMutex_2` [片段] 非错误 — readCounter 函数摘录，同上；验证：不适用(明示片段，完整程序已 PASS)
- [x] `sync_REMutex_3` [片段] 非错误 — writeCounter 函数摘录，同上；验证：不适用(明示片段，完整程序已 PASS)
- [x] `sync_REMutex_4` [片段] 非错误 — main 函数摘录，同上；验证：不适用(明示片段，完整程序已 PASS)

## sync/Spinlock.md

- [x] `sync_Spinlock_2` [片段] 非错误 — 「代码解释」小节逐段拆解页面开头那个完整可运行程序（首个 fence），Spinlock/atomic/runtime 均在其上定义，属明示片段；验证：不适用(明示片段)
- [x] `sync_Spinlock_3` [片段] 非错误 — 同上：Unlock 方法片段，出处为上方完整程序；验证：不适用(明示片段)
- [x] `sync_Spinlock_4` [片段] 非错误 — 同上：increment 函数片段，counter/spinLock 在上方完整程序中定义；验证：不适用(明示片段)
- [x] `sync_Spinlock_5` [片段] 非错误 — 同上：main 函数片段，出处为上方完整程序；验证：不适用(明示片段)

## syntax/For.md

- [x] `syntax_For_0` [伪代码] 非错误 — 「结构如下」后的 for 循环语法模板，初始化语句/条件表达式/后置语句为规则明列的中文占位符，不修；验证：不适用(语法模板占位符)
- [x] `syntax_For_9` [伪代码] 非错误 — for{} 无限循环语法模板（for 四种形式的第四种），本身即教学点；验证：不适用(语法模板)

## syntax/If.md

- [x] `syntax_If_0` [伪代码] 非错误 — 语法结构展示用中文占位符「条件表达式」，规则明确判非错误；验证：不适用(中文占位符)
- [x] `syntax_If_14` [片段] 已修 — someFunction 未定义；前置一个返回 error 的闭包定义，保留 if err := ...; err != nil 教学意图；验证：PASS(Error: something went wrong)
- [x] `syntax_If_15` [片段] 已修 — x/y/z 未定义；块首补 x, y, z := 7, 3, 3；验证：PASS(Complex condition met)
- [x] `syntax_If_2` [伪代码] 非错误 — if/else 语法结构中文占位符「条件表达式」；验证：不适用(中文占位符)
- [x] `syntax_If_4` [伪代码] 非错误 — if-else if-else 语法结构中文占位符「条件表达式1/2」；验证：不适用(中文占位符)
- [x] `syntax_If_6` [伪代码] 非错误 — 带初始化语句的 if 语法结构中文占位符「初始化语句; 条件表达式」；验证：不适用(中文占位符)
- [x] `syntax_If_8` [片段] 已修 — someFunction 未定义；前置一个返回 error 的闭包定义；验证：PASS(Error: something went wrong)

## syntax/Variable.md

- [x] `syntax_Variable_0` [伪代码] 非错误 — 「变量的语法格式」小节展示 var 声明的抽象形式（name/type/expression 为占位符），紧跟具体示例块；type 是关键字只是占位写法使然，非可运行代码；验证：不适用(语法占位符)

## test/Advanced.md

- [x] `test_Advanced_0` [测试文件] 非错误 — TestConcurrentProcessing 测试文件块，本身无 func main，按 go run 口径缺入口；测试体完整正确；验证：PASS(go test 实测：--- PASS: TestConcurrentProcessing)
- [x] `test_Advanced_1` [片段] 非错误 — gomock 示例的 NewMockService 由 mockgen 生成（块内注释「使用 gomock 生成模拟对象」已说明），生成代码在工程其他处；验证：不适用(package example 测试片段；gomock v1.6.0 在依赖中但生成辅助代码不在块内)
- [x] `test_Advanced_2` [测试文件] 非错误 — BenchmarkSort 基准测试文件块，同上；验证：PASS(go test -bench 实测：BenchmarkSort-14 10 122.6 ns/op)
- [x] `test_Advanced_3` [测试文件] 非错误 — TestABComparison 对比测试文件块，同上；验证：PASS(go test 实测：--- PASS: TestABComparison)

## test/BaseTest.md

- [x] `test_BaseTest_0` [片段] 非错误 — 不改：math.go 与 math_test.go 两个文件合并展示，注释标明文件边界（测试代码本就只能放 _test.go，无法作为单文件程序运行）；验证：不适用(双文件合并展示的测试示意)
- [x] `test_BaseTest_1` [片段] 非错误 — 不改：t.Logf 用法示例，Add 与导入约定在 2.1 同页定义；验证：不适用(片段)
- [x] `test_BaseTest_2` [片段] 非错误 — 不改：t.Fatalf/t.Errorf 对比示例，Divide 是惯用的被测函数示意（同 Add 之于 2.1），本节主题是测试错误处理写法；验证：不适用(片段)

## test/Benchmark.md

- [x] `test_Benchmark_0` [片段] 非错误 — 一个围栏展示两个文件，// math.go 与 // math_test.go 注释已标明边界，各自带 package 子句；拼进单文件后第二个 package 子句必然编译错，属展示形式而非代码错误；验证：不适用(双文件清单展示)

## test/Example.md

- [x] `test_Example_0` [片段] 非错误 — 一个围栏内以 // math.go 与 // math_test.go 注明两个源文件，是双文件清单而非单文件程序；测试包也本就不经 go run 运行；验证：不适用(双文件清单)
- [x] `test_Example_1` [片段] 非错误 — 4.5 的两个 Example 函数延续 4.1 math.go 块定义的 Add，同一 math 包的后续示例；验证：不适用(Add 定义于 4.1 块)

## test/Lib.md

- [x] `test_Lib_1` [片段] 非错误 — 页面 6.2 明示「示例中的 NewMockService 函数即由 mockgen 生成」，且块为 _test.go 文件（package example），属工程其他处生成的明示片段；验证：不适用(明示片段)

## test/Practice.md

- [x] `test_Practice_0` [片段] 非错误 — 不改：表驱动测试 TestAdd 示例（example_test.go，package example），被测函数 Add 在同页 8.6「// 被测试的函数」中定义，页面按测试文件惯例展示；验证：不适用(片段)
- [x] `test_Practice_1` [片段] 非错误 — 不改：BenchmarkAdd 基准测试示例，被测函数 Add 在同页 8.6「// 被测试的函数」中定义，页面按测试文件惯例展示；验证：不适用(片段)
- [x] `test_Practice_2` [片段] 非错误 — 不改：t.Parallel() 并行测试示意（另受列表缩进的伪语法错影响），被测函数 Add 在同页 8.6「// 被测试的函数」中定义，页面按测试文件惯例展示；验证：不适用(片段)
- [x] `test_Practice_3` [片段] 非错误 — 不改：TestErrorHandling 验证错误返回值示意（另受列表缩进的伪语法错影响），被测函数 Add 在同页 8.6「// 被测试的函数」中定义，页面按测试文件惯例展示；验证：不适用(片段)

## time/FormatAndParse.md

- [x] `time_FormatAndParse_0` [未使用] 已修 — layout 只是声明未使用，加 fmt.Println(time.Now().Format(layout)) 把布局用起来；验证：PASS(2026-10-05 04:44:06)
- [x] `time_FormatAndParse_2` [未使用] 已修 — customLayout 声明未使用，加 fmt.Println(time.Now().Format(customLayout)) 演示中文布局；验证：PASS(2026年10月05日 04时44分10秒)

## time/PkgTime.md

- [x] `time_PkgTime_0` [片段] 非错误 — 整块内容就是 import "time" 语句本身的教学展示（「只需在你的代码中引入它」），非独立程序；验证：不适用(语句级教学片段)
- [x] `time_PkgTime_1` [类型] 已修 — time.Date 第 7 个参数是 nsec int，原文误传 time.UTC；改为 0，末参时区保留 time.UTC；验证：PASS(指定日期时间: 2024-07-27 15:30:00 +0000 UTC)

## type/Array.md

- [x] `type_Array_0` [语法] 已修 — 三条声明示例裸在包级（:= 不能出现在包级），包进 func main 并加 fmt.Println(arr1, arr2, arr3) 用起变量，声明与注释原样保留；验证：PASS(输出 [0 0 0 0 0] [1 2 3] [1 2 3 4])

## type/Assertion.md

- [x] `type_Assertion_0` [伪代码] 非错误 — 「类型断言的基本语法如下」的语法模板，interfaceVariable/ConcreteType 是占位符且下方逐条解释，真实示例在后续小节；验证：不适用(语法占位模板)

## type/BaseConv.md

- [x] `type_BaseConv_7` [缺import] 已修 — import 块补 "strconv"，strconv.FormatBool 随之可用；验证：PASS(输出: true)

## type/Bool.md

- [x] `type_Bool_0` [语法] 已修 — 三种声明方式混有顶层短声明导致语法错；补 package/import/main 包裹并加 fmt.Println 展示三值；验证：PASS(输出 false true false)
- [x] `type_Bool_1` [片段] 已修 — a/b 未定义；块首补 a := false、b := true，if/for 演示原样保留；验证：PASS(输出 a is false / This will print once...)

## type/Byte.md

- [x] `type_Byte_0` [语法] 已修 — 顶层语句非法，包进 func main(){}（语句内容与输出注释不变）；验证：PASS(255 / 100，与注释声明一致)
- [x] `type_Byte_3` [缺import] 已修 — import 块补 "fmt"（块内用了 fmt.Println）；验证：PASS(Hello, World!)
- [x] `type_Byte_4` [缺import] 已修 — import 块补 "fmt"（块内用了 fmt.Println）；验证：PASS(直连 example.com:80 读取并打印响应后退出 0)

## type/Conv.md

- [x] `type_Conv_0` [未使用] 已修 — 展示用变量 b/c/d 用 fmt.Println(b, c, d) 用起来（与 BaseConv.md 同款写法对齐）；验证：PASS(输出: 100 100 100)
- [x] `type_Conv_1` [未使用] 已修 — 加 fmt.Println(b, c) 用起转换结果；验证：PASS(输出: 42 42)
- [x] `type_Conv_2` [语法] 已修 — 删除语句位置的 import "strconv" 行（验证器会自动推断 strconv），n/err/str 用 fmt.Println 用起来；验证：PASS(输出: 123 <nil> / 3.14)
- [x] `type_Conv_3` [未使用] 已修 — b/err 与 strBool 分别用 fmt.Println 用起来；验证：PASS(输出: true <nil> / true)

## type/Heap.md

- [x] `semantic_type_Heap` [空壳页] 页面级 — 文件名 Heap 标题却是「栈」且零正文：整页删除；栈内容已有 algo/stack/Stack.md、algo/list/Stack.md，堆内容已有 algo/tree/Heap.md、BinaryHeap.md、algo/array/PriorityQueue.md；SUMMARY 第 51 行链接同步移除，sidebar.json 重新生成；验证：SUMMARY/磁盘/侧栏三处对账一致

## type/HtmlTemplate.md

- [x] `type_HtmlTemplate_1` [未使用] 已修 — 单行 Parse 片段的 tmpl/err 未使用：按同页 block 0 的既有模式补成小 main（给 data、panic 检查、Execute 到 Stdout），Parse 行原样保留；验证：PASS(输出 <p>Name: Tom, Age: 18</p>)
- [x] `type_HtmlTemplate_2` [未使用] 已修 — 同上（if/else 模板，data 为 struct{ Active bool }）；验证：PASS(输出 <p>User is active</p>)
- [x] `type_HtmlTemplate_3` [未使用] 已修 — 同上（range 模板，data 为 Items []string）；验证：PASS(输出 <ul><li>Go</li><li>Rust</li><li>Python</li></ul>)
- [x] `type_HtmlTemplate_4` [未使用] 已修 — 同上（管道模板，data 为 struct{ Name string }）；验证：PASS(输出 <p>Hello, World!</p>)

## type/Int.md

- [x] `type_Int_0` [未使用] 已修 — var count 声明后未使用，补 fmt.Println(count)；验证：PASS(100)
- [x] `type_Int_1` [未使用] 已修 — var buffer 数组未使用，补 fmt.Println(len(buffer))；验证：PASS(1024)
- [x] `type_Int_2` [未使用] 已修 — var packetSize 未使用，补 fmt.Println(packetSize)；验证：PASS(1024)
- [x] `type_Int_3` [未使用] 已修 — var fileSize 未使用，补 fmt.Println(fileSize)；验证：PASS(2147483648)
- [x] `type_Int_5` [语法] 已修 — 裸赋值语句在函数体外，包成完整 main（int8 溢出演示）并 fmt.Println 输出；验证：PASS(-128，与注释一致)
- [x] `type_Int_6` [语法] 已修 — 裸赋值语句在函数体外，包成完整 main（uint8 溢出演示）并 fmt.Println 输出；验证：PASS(0，与注释一致)
- [x] `type_Int_7` [其他] 已修 — math.IntAdd 在 Go 1.27 中不存在（go doc math.IntAdd 核实 no symbol），溢出检查块换成 math/bits.Add32 进位演示；正文提及 math 包 IntAdd/IntSub 的整句一并更正为 math/bits 的 Add/Add32/Add64；验证：PASS(sum: 0 carry: 1)

## type/Interface.md

- [x] `type_Interface_1` [runtime示意] 非错误 — iface/itab 是 Go 运行时接口底层结构示意（runtime 源码走读），interfacetype/_type 为 runtime 内部类型；验证：不适用(runtime 结构示意)
- [x] `type_Interface_3` [片段] 已修 — Animal 嵌入的 Speaker 在本块内缺失（上方块的 Speaker 不随块携带），块内补 Speaker 接口定义，嵌套教学点保留；验证：PASS(Woof!/Run，与注释输出一致)

## type/Json.md

- [x] `type_Json_6` [片段] 已修 — 唯一的语句级片段（页面其余块都是完整程序）：补成同款 package main 程序——定义 jsonString、补 import、fmt.Println 用掉断言结果，原四条语句原样保留；验证：PASS(Alice 30)

## type/Pointer.md

- [x] `type_Pointer_1` [语法] 已修 — 顶层短声明导致语法错；补 package/import/main 包裹，原三行不动；验证：PASS(输出变量地址，注释已标「例如」)
- [x] `type_Pointer_2` [语法] 已修 — 同上；实测输出 10/20 与注释一致；验证：PASS(输出 10、20)

## type/Ring.md

- [x] `type_Ring_1` [片段] 非错误 — 「基本使用」第 2 项：r 是第 1 项完整程序里 ring.New(5) 建好的环，本项只演示 Len() 用法，不修；验证：不适用(沿用第 1 项环 r 的片段)
- [x] `type_Ring_2` [片段] 非错误 — 「基本使用」第 3 项 Do 遍历演示，r 沿用第 1 项，不修；验证：不适用(沿用第 1 项环 r 的片段)
- [x] `type_Ring_3` [片段] 非错误 — 「基本使用」第 4 项移动指针演示：r 沿用第 1 项，n 为移动步数占位，next/prev 只示意取值方式，不修；验证：不适用(Move/Next/Prev 用法示意片段)
- [x] `type_Ring_4` [片段] 非错误 — 「基本使用」第 5 项 Link 链接演示：r2 块内自建，r 沿用第 1 项，不修；验证：不适用(沿用第 1 项环 r 的片段)
- [x] `type_Ring_5` [片段] 非错误 — 「基本使用」第 6 项 Unlink 删除演示，r 沿用第 1 项，不修；验证：不适用(沿用第 1 项环 r 的片段)

## type/Rune.md

- [x] `type_Rune_0` [语法] 已修 — 包级位置出现 r2 := 短声明，非法；func main() 包住三种声明形式并 Println 展示值；验证：PASS(0 65 19990)
- [x] `type_Rune_1` [语法] 已修 — 声明+Println 平铺包级；func main() 包住，输出与注释一致（65/A/19990/世）；验证：PASS(65 A 19990 世)
- [x] `type_Rune_4` [片段] 已修 — runes 沿用上一块，块首补 runes := []rune("Hello, 世界") 使块自洽；验证：PASS(Hello, 世界)

## type/Slice.md

- [x] `type_Slice_0` [语法] 已修 — 四种声明写法挤一块互相重复声明（s := 复用同名变量报 no new variables）且语句在函数体外；包成完整 main，后三种写法改用 s2/s3/s4，末尾 fmt.Println 用起变量；验证：PASS([] [1 2 3 4 5] [0 0 0 0 0] [0 0 0])
- [x] `type_Slice_6` [语法] 已修 — var s 与 if 裸语句在函数体外，包成完整 main（nil 切片判断示例）；验证：PASS(s is nil / s is not nil)

## type/String.md

- [x] `type_String_0` [语法] 已修 — 三种声明方式补 package/import/main 包裹，加 Printf 展示默认空串；验证：PASS(输出 s1: "", s2: Hello, s3: World)
- [x] `type_String_1` [片段] 已修 — s2/s3 未定义；块首补 s2 := "Hello"、s3 := "World"，拼接代码原样保留；验证：PASS(输出 Hello, World!，与注释一致)
- [x] `type_String_3` [片段] 已修 — greeting 未定义；块首补 greeting := "Hello, World!"；验证：PASS(输出 Length of greeting: 13)
- [x] `type_String_4` [片段] 已修 — greeting 未定义；块首补 greeting := "Hello, World!"；验证：PASS(输出 First character: H)
- [x] `type_String_5` [片段] 已修 — greeting 未定义；块首补 greeting := "Hello, World!"；验证：PASS(输出 Substring: Hello)
- [x] `type_String_6` [片段] 已修 — s2 未定义；块首补 s2 := "Hello"；验证：PASS(输出 s2 is Hello)
- [x] `type_String_8` [片段] 已修 — s 未定义；块首补 s := "Hello"；验证：PASS(输出 Index/Character 遍历行)
- [x] `type_String_9` [未使用] 已修 — 完整示例里 s1 声明未用；按教学意图加 fmt.Printf 展示默认空串；验证：PASS(输出 s1: "")

## type/Struct.md

- [x] `type_Struct_0` [未使用] 已修 — p2/p3 为展示三种初始化方式而声明但未使用；补 fmt.Println(p2)、fmt.Println(p3)（与第 11 节 Println(p2) 风格一致）；验证：PASS(Charlie 30 / {Bob 25} / { 0})
- [x] `type_Struct_16` [逻辑] 已修 — §12 原示例 d.Name 对同层双嵌入确实编译不过；重写为正确的字段提升示例（B 嵌入 A，b.Name = "Alice" 输出 Alice），正文改为「双重嵌入同名字段报 ambiguous selector 编译错误」并指向 §13；验证：PASS（verify_one fence 459）

## type/Switch.md

- [x] `type_Switch_0` [伪代码] 非错误 — 「类型 switch 的语法」模板：i/T1/T2 为占位符，正文 bullet 明确解释「T1，T2：具体类型」；同页有三处可运行示例均 PASS；验证：不适用(语法占位符)

## type/Template.md

- [x] `type_Template_1` [未使用] 已修 — 模板语法小节的单行 Parse 调用包成完整 main（import text/template），_ = tmpl/_ = err 消除未使用，Parse 行逐字保留；验证：PASS(exit 0)
- [x] `type_Template_2` [未使用] 已修 — 模板语法小节的单行 Parse 调用包成完整 main（import text/template），_ = tmpl/_ = err 消除未使用，Parse 行逐字保留；验证：PASS(exit 0)
- [x] `type_Template_3` [未使用] 已修 — 模板语法小节的单行 Parse 调用包成完整 main（import text/template），_ = tmpl/_ = err 消除未使用，Parse 行逐字保留；验证：PASS(exit 0)
- [x] `type_Template_4` [未使用] 已修 — 模板语法小节的单行 Parse 调用包成完整 main（import text/template），_ = tmpl/_ = err 消除未使用，Parse 行逐字保留；验证：PASS(exit 0)
- [x] `type_Template_5` [未使用] 已修 — 模板语法小节的单行 Parse 调用包成完整 main（import text/template），_ = tmpl/_ = err 消除未使用，Parse 行逐字保留；验证：PASS(exit 0)
- [x] `type_Template_6` [缺import] 已修 — 自定义函数完整程序用 strings.ToUpper 却漏 import strings，import 区补 "strings"；验证：PASS(WORLD，与「输出结果」一致)

## var/Assignment.md

- [x] `var_Assignment_0` [伪代码] 非错误 — 「简单赋值」两行最小模式展示；页面末尾「示例代码」完整程序覆盖全部十种写法且实测 PASS；验证：不适用(语法模式展示)
- [x] `var_Assignment_2` [伪代码] 非错误 — 「简短变量声明」模式展示（x := 10 等，变量未用是模式展示本性）；验证：不适用(语法模式展示)
- [x] `var_Assignment_3` [伪代码] 非错误 — 「多重赋值/交换」模式展示；验证：不适用(语法模式展示)
- [x] `var_Assignment_4` [伪代码] 非错误 — 「空白标识符」模式展示，someFunction/anotherFunction 为示意函数名；验证：不适用(语法模式展示)
- [x] `var_Assignment_5` [伪代码] 非错误 — 「指针赋值」模式展示；验证：不适用(语法模式展示)
- [x] `var_Assignment_6` [伪代码] 非错误 — 「结构体赋值」模式展示；验证：不适用(语法模式展示)
- [x] `var_Assignment_7` [伪代码] 非错误 — 「切片赋值」模式展示；验证：不适用(语法模式展示)
- [x] `var_Assignment_9` [伪代码] 非错误 — 「函数返回值赋值」模式展示（a, b := someFunction() 在顶层只为展示形态，someFunction 已在块内定义）；验证：不适用(语法模式展示)

## var/ScopeAndLifetime.md

- [x] `var_ScopeAndLifetime_0` [片段] 非错误 — 多文件示例（块内标注 file1.go/file2.go，各自 package main），教学点正是「同包跨文件可见」；合并成单文件会毁掉教学意图，块内已用文件名注释明示；验证：不适用(多文件节选)
- [x] `var_ScopeAndLifetime_1` [片段] 非错误 — 函数作用域的单点示例（嵌在列表内，缺 package/import），页面末尾「示例代码」把三种作用域合成了可运行完整程序且实测 PASS；验证：不适用(节选，完整可运行版本在同页)
- [x] `var_ScopeAndLifetime_2` [片段] 非错误 — 块作用域单点示例，同上；验证：不适用(节选)
- [x] `var_ScopeAndLifetime_3` [片段] 非错误 — 包级变量生命周期的单行声明示例；验证：不适用(节选)
- [x] `var_ScopeAndLifetime_4` [片段] 非错误 — 局部变量生命周期单点示例，同上；验证：不适用(节选)
- [x] `var_ScopeAndLifetime_5` [片段] 非错误 — new 动态分配单点示例，同上；验证：不适用(节选)

## var/Segment.md

- [x] `var_Segment_2` [未使用] 已修 — initializedLocalVar 声明未使用；补 _ = initializedLocalVar（附注释说明），演示栈上分配的意图不变；验证：PASS(编译运行退出码 0)
- [x] `var_Segment_3` [未使用] 已修 — uninitializedLocalVar 声明未使用；补 _ = uninitializedLocalVar；验证：PASS(编译运行退出码 0)

## var/VarAndInit.md

- [x] `var_VarAndInit_0` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(0  false)
- [x] `var_VarAndInit_1` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(30 Alice true)
- [x] `var_VarAndInit_2` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(30 Alice true)
- [x] `var_VarAndInit_3` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；批量声明块含 var(...) 组触发 normalize 的 fmt 导入推断怪癖（误判 fmt 为本地定义），该块改为完整 main 程序；验证：PASS(30 Alice true)
- [x] `var_VarAndInit_4` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(0  false <nil>)
- [x] `var_VarAndInit_5` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(30 Alice true <nil>)
- [x] `var_VarAndInit_6` [未使用] 已修 — 该写法示例的变量声明后未使用，补 fmt.Println 用起变量；验证：PASS(30 Alice true)


---

合计登记 517 块：已修 196，非错误 319，页面级 2。