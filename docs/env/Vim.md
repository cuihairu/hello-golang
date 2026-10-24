# Vim
To write Go in Vim, set up the environment first:

### Install Vim

If you haven't installed Vim yet:

**On Ubuntu/Debian:**
```sh
sudo apt update
sudo apt install vim
```

**On MacOS:**
```sh
brew install vim
```

### Install Go

If you haven't installed Go yet, download the latest version from the [Go official site](https://go.dev/dl/) and install it.

### Configure Vim

1. **Install a plugin manager**

   I use [vim-plug](https://github.com/junegunn/vim-plug) for plugin management. Install it with:

   ```sh
   curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
   ```

2. **Edit the `.vimrc` file**

   Open your `.vimrc` file (usually located at `~/.vimrc`) and add the following to set up the Go development environment:

   ```vim
   call plug#begin('~/.vim/plugged')

   " Go development plugins
   Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

   call plug#end()

   " Basic settings
   syntax on
   filetype plugin indent on
   set number " show line numbers

   " vim-go plugin settings
   let g:go_fmt_command = "goimports"
   let g:go_def_mode = 'gopls'
   let g:go_info_mode = 'gopls'
   ```

3. **Install the plugins**

   Open Vim and run the following command to install the plugins:

   ```vim
   :PlugInstall
   ```

4. **Update the vim-go binaries**

   Run the following command to install and update the tools vim-go needs:

   ```vim
   :GoUpdateBinaries
   ```

### Install and configure gopls

[gopls](https://github.com/golang/tools/tree/master/gopls) is an implementation of the Go Language Server Protocol (LSP); it gives your editor code completion, jump-to-definition, refactoring, and more. You can install gopls with the following command:

```sh
go install golang.org/x/tools/gopls@latest
```

In the `.vimrc` file, make sure vim-go is configured to use gopls:

```vim
let g:go_def_mode = 'gopls'
let g:go_info_mode = 'gopls'
```

### Other useful plugins

1. **Autocompletion plugins (such as YouCompleteMe or deoplete)**

   **Install YouCompleteMe:**
   ```vim
   Plug 'ycm-core/YouCompleteMe', { 'do': './install.py --go-completer' }
   ```

   **Install deoplete:**
   ```vim
   Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
   Plug 'zchee/deoplete-go', { 'do': 'make' }
   ```

2. **Linting plugins (such as ale)**

   ```vim
   Plug 'dense-analysis/ale'
   ```

   **Enable ale and gopls support in `.vimrc`:**
   ```vim
   let g:ale_linters = {
       \   'go': ['gopls'],
       \}
   let g:ale_fixers = {
       \   'go': ['gofmt', 'goimports'],
       \}
   ```

Once you've gone through these steps, Vim can handle Go: completion, navigation, and refactoring come from gopls, formatting from goimports, and real-time checking from ale.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules guide](https://go.dev/doc/modules/)


## Sibling pages

- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [GOPROXY](/env/GOPROXY.md)
- [Tools](/env/Tools.md)
- [ide](/env/ide.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Tools](/env/Tools.md)
- [ide](/env/ide.md)
