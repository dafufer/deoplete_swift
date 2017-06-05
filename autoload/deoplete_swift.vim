" Based on the code from https://github.com/mitsuse/autocomplete-swift

let s:placeholder_pattern = '<#\%(T##\)\?\%([^#]\+##\)\?\([^#]\+\)#>'

function! deoplete_swift#jump_to_placeholder()
  if &filetype !=# 'swift'
    return ''
  end

  if !search(s:placeholder_pattern)
    return ''
  endif

  return "\<ESC>:call deoplete_swift#begin_replacing_placeholder()\<CR>"
endfunction

function! deoplete_swift#begin_replacing_placeholder()
    if mode() !=# 'n'
        return
    endif

    let l:pattern = s:placeholder_pattern

    let [l:line, l:column] = searchpos(l:pattern)
    if l:line == 0 && l:column == 0
        return
    end

    execute printf(':%d s/%s//', l:line, l:pattern)

    call cursor(l:line, l:column)

    startinsert
endfunction
