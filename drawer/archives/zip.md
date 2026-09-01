## Creating archives
- `zip archive.zip file1 file2` — create an archive from specific files <!-- compress -->
- `zip -r archive.zip dir/` — create an archive from a directory, recursively <!-- compress -->
- `zip -9 archive.zip file1` — maximum compression level
- `zip -e archive.zip file1` — create a password-protected archive <!-- encrypt -->

## Extracting archives
- `unzip archive.zip` — extract into the current directory <!-- decompress -->
- `unzip archive.zip -d /path/to/dest` — extract into a specific directory <!-- decompress -->
- `unzip -o archive.zip` — extract, overwriting existing files without prompting

## Inspecting
- `unzip -l archive.zip` — list contents without extracting
- `unzip -t archive.zip` — test archive integrity without extracting

## Updating & removing
- `zip -u archive.zip file1` — add or update a file in an existing archive
- `zip -d archive.zip file1` — remove a file from an existing archive
