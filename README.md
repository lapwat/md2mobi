# md2mobi

Convert Markdown files to Mobi files for Amazon Kindle.

## Run

Run this command with custom `title` and `author`.

```sh
$ docker run -v "$PWD"/your_ebook.md:/ebook.md -e TITLE="A title" -e AUTHOR="An author" lapwat/md2mobi > your_ebook.mobi
```

## Build from source

```sh
$ docker build -t lapwat/md2mobi .
```
