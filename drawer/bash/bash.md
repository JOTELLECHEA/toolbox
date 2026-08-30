## Navigation
- `cd -` — jump back to the previous directory
- `cd ..` — move up one directory
- `pwd` — print the current working directory
- `pushd <dir>` — jump to a directory and remember where you came from
- `popd` — jump back to the directory `pushd` remembered

## Listing & inspecting
- `ls -lah` — long listing, human-readable sizes, include hidden files
- `ls -lt` — sort by most recently modified
- `du -sh <dir>` — total size of a directory, human-readable <!-- disk usage, folder size -->
- `df -h` — disk space usage across mounted filesystems, human-readable
- `file <path>` — identify a file's type
- `stat <path>` — detailed file metadata: size, permissions, timestamps

## Moving, copying, removing
- `mv src dst` — move or rename
- `cp -r src dst` — copy a directory recursively
- `rm -rf <dir>` — remove a directory and its contents (careful — irreversible)
- `mkdir -p a/b/c` — create nested directories in one go
- `ln -s target linkname` — create a symbolic link

## Permissions
- `chmod +x script.sh` — make a file executable
- `chmod 644 file` — read/write for owner, read-only for group and others
- `chown user:group file` — change a file's owner and group

## Searching
- `find . -name "*.py"` — find files matching a pattern
- `find . -mtime -1` — files modified in the last day <!-- recent files, modified today -->
- `grep -rn "term" .` — recursive search with line numbers
- `grep -i "term" file` — case-insensitive search

## History & recall
- `history | grep <term>` — search past commands
- `!123` — re-run history entry number 123
- `!!` — re-run the last command <!-- repeat last command -->
- `ctrl+r` — reverse-search through history interactively <!-- keyboard shortcut -->

## Text processing
- `sort file | uniq -c` — count occurrences of each unique line
- `wc -l file` — count lines in a file
- `cut -d',' -f2 file.csv` — extract a column from delimited text
- `awk '{print $1}' file` — print the first whitespace-separated field
- `sed 's/foo/bar/g' file` — replace text in a stream

## Processes
- `ps aux` — list all running processes
- `ps aux | grep <name>` — find a running process by name
- `kill -9 <pid>` — force-kill a process
- `top` — live view of running processes and resource usage
- `jobs` — list background jobs in the current shell
- `bg` — resume a stopped job in the background
- `fg` — bring a background job to the foreground

## Piping & redirection
- `command > file` — redirect output to a file, overwriting
- `command >> file` — redirect output to a file, appending
- `command 2>&1` — redirect stderr into stdout
- `command1 | command2` — pipe output from one command into the next
- `find . -name "*.log" | xargs rm` — build and run a command from piped input

