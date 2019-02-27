# md2mobi

Convert Markdown files to Mobi files for Amazon Kindle.

## Run

Run this command with custom `title` and `author`.

```sh
$ cat your_ebook.md | docker run -i -e TITLE="A title" -e AUTHOR="An author" lapwat/md2mobi > your_ebook.mobi
```

## Build from source

```sh
$ docker build -t lapwat/md2mobi .
```
