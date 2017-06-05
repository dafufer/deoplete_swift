function! deoplete_swift#get_sdk()
  " sdk:
  "     if empty, the flag won't be set in sourcekitten command (default)
  "     set the value to the path of a sdk version, i.e.:
  "     /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS9.0.sdk
  "     xcrun --show-sdk-path
  let s:sdk = get(b:, 'deoplete_swift_sdk', get(g:, 'deoplete_swift_sdk', ''))
  return s:sdk
endfunction

function! deoplete_swift#get_target()
  " target:
  "     if empty, the flag won't be set in sourcekitten command (default)
  "     set the value to a target, i. e: arm64-apple-ios9.0 or x86_64-apple-darwin16.6.0
  "     clang -v 2>&1 | grep Target
  let s:target = get(b:, 'deoplete_swift_target', get(g:, 'deoplete_swift_target', ''))
  return s:target
endfunction

function! deoplete_swift#get_spm_module()
  " spm-module:
  "     if empty, the flag won't be set in sourcekitten command (default)
  "     set the value to the name of a swift package manager module
  let s:spm = get(b:, 'deoplete_swift_spm_module', get(g:, 'deoplete_swift_spm_module', ''))
  return s:spm
endfunction


nnoremap <silent><expr> <Plug>(deoplete_swift_jump_to_placeholder) deoplete_swift#jump_to_placeholder()
inoremap <silent><expr> <Plug>(deoplete_swift_jump_to_placeholder) deoplete_swift#jump_to_placeholder()

