# Gutenberg, dammit

By [Allison Parrish](http://www.decontextualize.com/)

*Gutenberg, dammit* is a corpus of every plaintext file in Project Gutenberg (up
until June 2016), organized in a consistent fashion, with (mostly?) consistent
metadata. The intended purpose of the corpus is to make it really easy to do
creative things with this wonderful and amazing body of freely-available text.

[Download the corpus here.](TK)

The name of the corpus was inspired by Leonard Richardson's [Unicode,
dammit](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#unicode-dammit).

Code in this repository relies on the data prepared by the [GutenTag
project](http://www.cs.toronto.edu/~jbrooke/gutentag/) (Brooke 2015) and the
code is partially based on the [GutenTag source
code](https://github.com/julianbrooke/GutenTag).

> NOTE: Not all of the works in Project Gutenberg are in the public domain.
> Check the `Copyright Status` field in the metadata for each work you plan on
> using to be sure. I believe that all of the files in the corpus are
> redistributable, but it might not be okay for you to "reuse" any works in the
> corpus that are not in the public domain.

## Working with the corpus

The `gutenbergdammit.ziputils` module has some functions for working with the
corpus file *in situ* using Python's `zipfile` library, so you don't even have
to decompress the file and make a big mess on your hard drive. You can
copy/paste these functions, use them as a reference in your own implementation,
or use them directly by installing this package from the repo:

    pip install https://github.com/aparrish/gutenberg-dammit/archive/master.zip

For example, to retrieve the text of one particular file from the corpus:

    >>> from gutenbergdammit.ziputils import retrieve_one
    >>> text = retrieve_one("gutenberg-dammit-files-001.zip", "123/12345.txt")
    >>> text[:50]
    '[Illustration: "I saw there something missing from'

To retrieve the metadata file:

    >>> from gutenbergdammit.ziputils import loadmetadata
    >>> metadata = loadmetadata("gutenberg-dammit-files-001.zip")
    >>> metadata[456]['Title']
    ['Essays in the Art of Writing']

To search for and retrieve files whose metadata contains particular strings:

    >>> from gutenbergdammit.ziputils import searchandretrieve
    >>> for info, text in searchandretrieve("gutenberg-dammit-files-001.zip", {'Title': 'Made Easy'}):
    ...     print(info['Title'][0], len(text))
    ... 
    Entertaining Made Easy 108314
    Reading Made Easy for Foreigners - Third Reader 209964
    The Art of Cookery Made Easy and Refined 262990
    Shaving Made Easy	What the Man Who Shaves Ought to Know 44982
    Writing and Drawing Made Easy, Amusing and Instructive	Containing The Whole Alphabet in all the Characters now	us'd, Both in Printing and Penmanship 10036
    Etiquette Made Easy 119770

### Details

The corpus is arranged as multiple subdirectories, each with the first three
digits of the number identifying the Gutenberg book. Plain text files for each
book whose ID begins with those digits are located in that directory. For
example, the book with Gutenberg ID `12345` has the relative path
`123/12345.txt`. This path fragment is present in the metadata for each file as
the `gd-path` attribute; see below for more details. (Splitting up the files
like this is intended to be a compromise that makes accessing each file easy
while making life a little bit easier if you're poking around with your file
browsing application or `ls`.)

The files themselves have had Project Gutenberg boilerplate headers and footers
stripped away for your convenience. (The code used to strip the boilerplate is
copied from GutenTag.) You may want to do your own sanity check on individual
files of importance to guarantee that they have the contents you think they
should have.

#### Metadata

The `gutenberg-metadata.json` file in the zip is a big JSON file with metadata on
each book. The is a list of JSON objects with the following format:

    {
        "Author": [ "Robert Carlton Brown" ],
        "Author Birth": [ 1886 ],
        "Author Death": [ 1959 ],
        "Author Given": [ "Robert Carlton" ],
        "Author Surname": [ "Brown" ],
        "Copyright Status": [ "Not copyrighted in the United States." ],
        "Language": [ "English" ],
        "LoC Class": [ "SF: Agriculture: Animal culture" ],
        "Num": "14293",
        "Subject": [ "Cookery (Cheese)", "Cheese" ],
        "Title": [ "The Complete Book of Cheese" ],
        "charset": "iso-8859-1",
        "gd-num-padded": "14293",
        "gd-path": "142/14293.txt",
        "href": "/1/4/2/9/14293/14293_8.zip"
    }

The capitalized fields correspond to the fields in the official Project
Gutenberg metadata, with information about the author broken out into the
birth/death/given/surname fields when possible. Fields are presented as lists
to accommodate books that (e.g.) have more than one author or title.

The lower-case fields are metadata specific to this corpus, explained below:

* `charset`: The character set of the original file. All of the files in the
  ZIP are in UTF8 encoding, so this is only helpful if (e.g.) you're using the
  metadata to refer back to the original file on the Gutenberg website.
* `gd-num-padded`: The book number ("Gutenberg ID") left-padded to five digits
  with zeros.
* `gd-path`: The path to the file inside the Gutenberg Dammit zip file,
  to be appended to the `gutenberg-dammit-files/` directory present in the zip
  file itself.
* `href`: The path to the file in the original GutenTag corpus.

#### What was included, what was left out

First off, *Gutenberg, dammit* is based on files from [Project
Gutenberg](http://www.gutenberg.org/), and doesn't include files from any of
the related international projects (e.g. Project Gutenberg Canada, Project
Gutenberg Australia).

Only Gutenberg items with plaintext files are included in this corpus. It
doesn't include audiobooks, and it doesn't include any books only available
in text formats other than plaintext (e.g., PDF or HTML).

In some cases, books that are primarily available in some non-plaintext format
will include a "stub" text file that just tells the reader to look at the other
file. No attempt has been made to systematically exclude these from the present
corpus.

## How to *Gutenberg, dammit* from scratch

If you just want to *use* the corpus, don't bother with any of the content that
follows. If you want to be able to recreate the process of how I made the
corpus, read on.

The scripts in this repository work on the files prepared by
[GutenTag](http://www.cs.toronto.edu/~jbrooke/gutentag/download.html). In order
to use the scripts, you'll need to download their corpus ("Our (full) Project
Gutenberg Corpus", ~7Gb ZIP file) and unzip it into a directory on your system.

The included package `gutenbergdammit/build.py` is designed to be used as a
command-line script. Run it on the command line like so:

    python -m gutenbergdammit.build --src-path=<path to your gutentag download> \
        --dest-path=output --metadata-file=output/gutenberg-metadata.json \

Help on the options:

    Usage: build.py [options]

    Options:
    -h, --help            show this help message and exit
    -s SRC_PATH, --src-path=SRC_PATH
                            path to GutenTag dump
    -d DEST_PATH, --dest-path=DEST_PATH
                            path to output (will be created if it doesn't exist)
    -m METADATA_FILE, --metadata-file=METADATA_FILE
                            path to metadata file for output (will be overwritten)
    -l LIMIT, --limit=LIMIT
                            limit to n entries (good for testing)
    -o OFFSET, --offset=OFFSET
                            start at index n (good for testing)

The `--limit` and `--offset` options are not required, and, if omitted, the
tool will default to processing the entire archive.

### Notes on implosion

Python's `zipfile` module doesn't support the compression algorithm used on
some of the files in the Gutenberg archive ("implosion"). Whoops. Included in
the repository is a script that unzips and re-zips these files using a modern
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

## Next steps

* Rework this process so it can construct a similarly-organized archive
  starting with a straight-up mirror of Project Gutenberg (rather than the
  GutenTag corpus, which is a combination of the 2010 DVD ISO and I think more
  recent entries collected via web scraping?)
* Implement a process for adding newer files to the corpus (by looking at the
  [RSS feed](http://www.gutenberg.org/wiki/Gutenberg:Feeds)?)
* Make the corpus zip file into a torrent or something so I'm not paying for
  every download

## Works cited

Brooke, Julian, et al. “[GutenTag: An NLP-Driven Tool for Digital Humanities
Research in the Project Gutenberg
Corpus](http://www.cs.toronto.edu/pub/gh/Brooke-etal-2015-CLfL.pdf).” CLfL@
NAACL-HLT, 2015, pp. 42–47.

## License

In accordance with GutenTag's license:

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative
Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

