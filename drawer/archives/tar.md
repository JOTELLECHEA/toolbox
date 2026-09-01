## Creating archives
- `tar -cvf archive.tar file1 file2` — create an uncompressed archive <!-- tarball -->
- `tar -czvf archive.tar.gz dir/` — create a gzip-compressed archive <!-- tarball, zip -->
- `tar -cjvf archive.tar.bz2 dir/` — create a bzip2-compressed archive
- `tar -cJvf archive.tar.xz dir/` — create an xz-compressed archive

## Extracting archives
- `tar -xvf archive.tar` — extract an uncompressed archive <!-- unzip, decompress, tarball -->
- `tar -xzvf archive.tar.gz` — extract a gzip-compressed archive <!-- unzip, decompress, tarball -->
- `tar -xjvf archive.tar.bz2` — extract a bzip2-compressed archive <!-- unzip, decompress -->
- `tar -xJvf archive.tar.xz` — extract an xz-compressed archive <!-- unzip, decompress -->
- `tar -xzvf archive.tar.gz -C /path/to/dest` — extract into a specific directory

## Inspecting
- `tar -tvf archive.tar` — list contents without extracting
- `tar -tzvf archive.tar.gz` — list contents of a gzip archive without extracting

## Flag reference
- `-c` — create a new archive
- `-x` — extract an existing archive
- `-t` — list contents (table of contents), don't extract
- `-v` — verbose, print each file as it's processed
- `-f` — filename follows — must come immediately before the archive name
- `-z` — filter through gzip (.gz)
- `-j` — filter through bzip2 (.bz2)
- `-J` — filter through xz (.xz)
