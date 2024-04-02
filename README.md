# bleach

## Acme::Bleach

This is a small Perl library available on CPAN that makes a script "disappear"
by converting it entirely into whitespace characters -- yet, miraculously, the
script can still be run.

The way this works is that the bytes of the input script are converted into
bits and those bits become tabs and spaces, which are written to the new file --
just a bunch of whitepsace. When you want to "run" the script, a one line header
includes Acme::Bleach which can turn the rest of the file back into normal code
and the result is then `eval()`'d.

Acme::Bleach is a very Perlish module: arguably pointless, but also cryptic
and a bit magical seeming. It is the oppposite of the Python ethos.

That's why I had to create `bleach.py`. Because Python deserves some magic,
too.

## Use

### As a library

You can import `bleach` into your Python script and use it directly. The 
`bleach` and `unbleach` routines work on file handles rather than strings,
but you can use StringIO and BytesIO to access strings if you prefer.

The input to `bleach()` and the output of `unbleach()` are always opened
in binary mode, so that binary files (or text files) can be handled. However,
the output of `bleach()` and the input of `unbleach()` are always opened
int text mode becausae the bleach output is just tabs and spaces -- these 
are text files.

### From the command line

You can also call `bleach.py` from the command line, like this:

```bash
$ ./bleach.py --encode input.txt --output bleached.txt
$ ./bleach.py --decode bleached.txt --output check.txt
# diff  input.txt check.txt
```

You can also do this to make a runnable bleached script:

```bash
$ ./bleach.py --script myscript.py --output bleached.py
```

Use this to impress your friends!

