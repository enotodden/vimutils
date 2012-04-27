function! VimUtilsCommandOutput(cmd)
	redir => message
	silent execute a:cmd
	redir END
	return message
endfunction


"Write a buffer to a tmp file and return the tmp filename
function! VimUtilsWriteBufferToTmpFile(bufno)
python << EOF
import vim
import random
tmpfile = "/tmp/vimutils_" + str(random.randint(1,19928))
current_buffer = str(vim.current.buffer.number)
vim.command(":buffer " + vim.eval("a:bufno"))
vim.command("silent execute \":write " + tmpfile + "\"")
vim.command("silent execute \":buffer " + current_buffer + "\"")
EOF
	redir => bb
    :py print tmpfile
    redir END
    return bb
endfunction

