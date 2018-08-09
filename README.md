# Gutenberg, dammit

By [Allison Parrish](http://www.decontextualize.com/)

I wanted a big flat directory with plain-text versions of all the books from
Project Gutenberg. This is the result.

Code in this repository relies on the data prepared by the [GutenTag
project](http://www.cs.toronto.edu/~jbrooke/gutentag/) and the code is
partially based on the [GutenTag source
code](https://github.com/julianbrooke/GutenTag).

## Working with the corpus

[Download the corpus here](TK).

The corpus is arranged as multiple subdirectories, each with the first three
digits of the number identifying the Gutenberg book. Plain text files for each
book whose ID begins with those digits are located in that directory. For
example, the book with Gutenberg ID `12345` has the relative path
`123/12345.txt`. (Splitting up the files like this is intended to be a
compromise that makes accessing each file easy while making life a little bit
easier if you're poking around with your file browsing application or `ls`.)

The included `gutenberg-metadata.json` file is a big JSON file with metadata on
each book.


## Replicating the work

The scripts in this repository work on the files prepared by
[GutenTag](http://www.cs.toronto.edu/~jbrooke/gutentag/download.html). In order
to use the scripts, you'll need to download their corpus ("Our (full) Project
Gutenberg Corpus", ~7Gb ZIP file) and unzip it into a directory on your system.

## Notes on implosion

Python's `zipfile` module doesn't support the compression algorithm used on
some of the files in the archive ("implosion"). Whoops. Included in the
repository is a script that unzips and re-zips these files using a modern
compression algorithm. To run it:

    python -m gutenbergdammit.findbadzips --src-path=<gutentag_dump> --fix

This will modify the ~100 files in your GutenTag dump with broken ZIP
compression, and save copies of the originals (with `-orig` at the end of the
filename). Leave off `--fix` to do a dry run (i.e., just show which files are
bad, don't fix them).

To use this script, you'll need to have the `zip` and `unzip` binaries on your
system and in your path. It also probably assumes UNIX-ey paths (i.e.,
separated with slashes), but a lot of stuff in here does. Pull requests
welcome.

## License

In accordance with GutenTag's license:

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative
Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

