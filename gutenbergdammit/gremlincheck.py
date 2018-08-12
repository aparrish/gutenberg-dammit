# This is a simple script for sanity-checking encodings in the pre-zipped
# archive. It just looks at every file and prints out every line that has what
# looks like a non-ASCII character. If these lines look okay, then the way
# these scripts handle character encoding is also probably okay. That's the
# theory at least.
from glob import glob

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--src-path",
            help="path to unzipped Gutenberg, dammit archive",
            default="./gutenberg-dammit-files")
    options, _ = parser.parse_args()

    for fname in glob(options.src_path + "/*/*"):
        matches = []
        for line in open(fname):
            line = line.strip()
            if any([ord(ch) > 127 for ch in line]):
                matches.append(line)
        if len(matches) == 0:
            continue
        elif len(matches) <= 5:
            for match in matches:
                print(fname, match)
        else:
            print(fname, matches[0])
            print(fname, "...", len(matches), "matches in this file")

