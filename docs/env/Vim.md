# Vim
在Vim里写Go，先把环境搭起来：

### 安装Vim

没装Vim的先装：

**在Ubuntu/Debian系统上:**
```sh
sudo apt update
sudo apt install vim
```

**在MacOS上:**
```sh
brew install vim
```

### 安装Go

Go还没装的话，从[Go的官网](https://golang.org/dl/)下载最新版本安装。

### 配置Vim

1. **安装插件管理器**

   插件管理用[vim-plug](https://github.com/junegunn/vim-plug)，安装命令：

   ```sh
   curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
   ```

2. **编辑`.vimrc`文件**

   打开你的`.vimrc`文件（通常位于`~/.vimrc`），添加以下配置来设置Go开发环境：

   ```vim
   call plug#begin('~/.vim/plugged')

   " Go开发插件
   Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

   call plug#end()

   " 基本设置
   syntax on
   filetype plugin indent on
   set number " 显示行号

   " vim-go插件设置
   let g:go_fmt_command = "goimports"
   let g:go_def_mode = 'gopls'
   let g:go_info_mode = 'gopls'
   ```

3. **安装插件**

   打开Vim并运行以下命令来安装插件：

   ```vim
   :PlugInstall
   ```

4. **更新vim-go二进制文件**

   运行以下命令来安装和更新vim-go所需的工具：

   ```vim
   :GoUpdateBinaries
   ```

### 安装和配置gopls

[gopls](https://github.com/golang/tools/tree/master/gopls)是Go语言服务器协议（LSP）实现，它为编辑器提供了代码补全、跳转、重构等功能。你可以使用以下命令来安装gopls：

```sh
go install golang.org/x/tools/gopls@latest
```

在`.vimrc`文件中，确保vim-go已配置使用gopls：

```vim
let g:go_def_mode = 'gopls'
let g:go_info_mode = 'gopls'
```

### 其他有用的插件

1. **自动补全插件（如YouCompleteMe或deoplete）**

   **安装YouCompleteMe:**
   ```vim
   Plug 'ycm-core/YouCompleteMe', { 'do': './install.py --go-completer' }
   ```

   **安装deoplete:**
   ```vim
   Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
   Plug 'zchee/deoplete-go', { 'do': 'make' }
   ```

2. **语法检查插件（如ale）**

   ```vim
   Plug 'dense-analysis/ale'
   ```

   **在`.vimrc`中启用ale和gopls支持:**
   ```vim
   let g:ale_linters = {
       \   'go': ['gopls'],
       \}
   let g:ale_fixers = {
       \   'go': ['gofmt', 'goimports'],
       \}
   ```

走完这几步，Vim 就能写 Go 了：补全、跳转、重构靠 gopls，格式化交给 goimports，实时检查交给 ale。