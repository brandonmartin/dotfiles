set nocompatible
filetype off

call pathogen#infect()

" Set filetype detection on, load plugins and indent.
filetype plugin indent on

" Use vim defaults.
set nocompatible

" Tabs, Spaces and Indentation.
set expandtab " Use spaces for tabs.
set tabstop=2 " Number of spaces to use for tabs.
set shiftwidth=2 " Number of spaces to autoindent.
set softtabstop=2 " Number of spaces for a tab.
set autoindent " Set autoindenting on.
set smartindent " Automatically insert another level of indent when needed. 

" Set tab width to 4 spaces for python files
" autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4

" Various.
set bs=2 " Backspace, this is the same as :set backspace=indent,eol,start.
set ruler " Show the cursor position.
set scrolloff=5 " Show 5 lines above/below the cursor when scrolling.
set number " Line numbers on.
set showcmd " Shows the command in the last line of the screen.
set autoread " Read files when they've been changed outside of Vim.

" Bells and whistles.
set novisualbell
set noerrorbells
set t_vb=

set history=1000 " Number of command lines stored in the history tables.
set undolevels=1000 " Number of levels of undo

set title " Set the title in the console.

" Use matchtime and showmatch together.
set matchtime=2 " Time to show matching parent in 10ths of a sec.
set showmatch " Show matching parents.

set splitright " Open new vertical split windows to the right of the current one, not the left.
set splitbelow " See above description. Opens new windows below, not above.

" Backup.
set nobackup " Don't backup files.
set nowritebackup
set noswapfile

" Searching.
set hlsearch " Highlight search terms
set incsearch " Show search matches as you type
set ignorecase " Ignore case when searching
set smartcase " Make searches case sensitive only if they contain uppercase stuff

set wildmode=longest,list " File and directory matching mode.

set nrformats=hex " Allow incrementing and decrementing numbers that start with 0 using <c-a> and <c-x>

set clipboard=unnamedplus,autoselect " Use + register (X Window clipboard) as unnamed register"

syntax on " Syntax highlighting on.

" Drupal command group, set the correct filetypes for Drupal files.
augroup drupal
  autocmd BufRead,BufNewFile *.module set filetype=php
  autocmd BufRead,BufNewFile *.theme set filetype=php
  autocmd BufRead,BufNewFile *.inc set filetype=php
  autocmd BufRead,BufNewFile *.install set filetype=php
  autocmd BufRead,BufNewFile *.engine set filetype=php
  autocmd BufRead,BufNewFile *.profile set filetype=php
  autocmd BufRead,BufNewFile *.test set filetype=php
augroup END

autocmd BufRead,BufNewFile *.json set filetype=json 

" Change the leader from \ to , for easier reaching
let mapleader = ","

" Prevent help popping up catch <F1> instead of <ESC>.
nmap <F1> <ESC>
map <F1> <ESC>
imap <F1> <ESC>

" Map keys to navigate tabs
map <C-h> :tabprevious<CR>
map <C-l> :tabnext<CR>

" Cursor doesn't skip wrapped lines with hitting j or k
nnoremap j gj
nnoremap k gk

" Map F1 to Esc instead of the stupid help crap.
inoremap <F1> <ESC>
nnoremap <F1> <ESC>
vnoremap <F1> <ESC>

" Indent as many times as you want in visual mode without losing focus
vnoremap < <gv
vnoremap > >gv

" Make a curly brace automatically insert an indented line
inoremap {<CR> {<CR>}<Esc>O<BS><Tab>

" Add auto-expanders for Django template tags
imap {% {%<Space><Space>%}<Esc>hhi
imap {{ {{<Space><Space>}}<Esc>hhi

" Make jj exit insert mode (since it's almost never typed normally).
imap jj <Esc>:w<CR>

" Disable arrow keys
map <up> <nop>
map <down> <nop>
map <left> <nop>
map <right> <nop>
imap <up> <nop>
imap <down> <nop>
imap <left> <nop>
imap <right> <nop>

" Map up/down to insert new line above/below respectively, without entering
" insert mode.
map <down> o<Esc>
map <up> O<Esc>

" Set color scheme (t_Co=256 is necessary for 256 color terminals to work).
set t_Co=256
colorscheme molokai

" Set options for Zen Coding
"let g:user_zen_expandabbr_key = '<c-e>'
"let g:use_zen_complete_tag = 1

" Set options for ctrlp.vim
"set wildignore+=*/.git/*,*/.hg/*,*/.svn/*
let g:ctrlp_dotfiles = 0
let g:ctrlp_working_path_mode = 0
let g:ctrlp_match_window_reversed = 0
let g:ctrlp_persistent_input = 0

" If you prefer the Omni-Completion tip window to close when a selection is
" made, these lines close it on movement in insert mode or when leaving
" insert mode.
autocmd CursorMovedI * if pumvisible() == 0|pclose|endif
autocmd InsertLeave * if pumvisible() == 0|pclose|endif

" Configure the Syntastic plugin for automatic syntax checking.
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
let g:syntastic_enable_signs=1
let g:syntastic_auto_loc_list=1

" Configure vim-gist
"let g:gist_clip_command = 'xclip -selection clipboard'
"let g:gist_detect_filetype = 1

" Enable the HTML closetag plugin
"au Filetype html,xml,php source ~/.vim/bundle/closetag.vim/plugin/closetag.vim

" Stuff for VimClojure
let g:vimclojure#HighlightBuiltins = 1
let g:vimclojure#ParenRainbow = 1

" disable pyflakes
let g:did_pyflakes_plugin = 1

