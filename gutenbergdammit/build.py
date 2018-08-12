import sys
import pathlib
from os.path import join as opj
from zipfile import BadZipFile
import json

from gutenbergdammit import text_info_iter, get_plain_text
from gutenbergdammit.textcleaner import TextCleaner

def err(*args):
    print(*args, file=sys.stderr)

if __name__ == '__main__':
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--src-path",
            help="path to GutenTag dump",
            default="./PGUS")
    parser.add_option("-d", "--dest-path",
            help="path to output (will be created if it doesn't exist)",
            default="./gutenberg-dammit")
    parser.add_option("-m", "--metadata-file",
            help="path to metadata file for output (will be overwritten)",
            default="./gutenberg-metadata.json")
    parser.add_option("-l", "--limit", type="int",
            help="limit to n entries (good for testing)",
            default=None)
    parser.add_option("-o", "--offset", type="int",
            help="start at index n (good for testing)",
            default=0)
    options, _ = parser.parse_args()

    errors = []
    metadata = []
    cleaner = TextCleaner()

    err("Processing input from GutenTag dump at", options.src_path, "...")

    for i, item in enumerate(text_info_iter(corpus_dir=options.src_path)):
        if i < options.offset:
            continue
        try:
            raw_text = get_plain_text(item["href"], item["charset"],
                    corpus_dir=options.src_path)
            cleaned = cleaner.clean_text(raw_text)
            num_str = str(int(item["Num"])).zfill(5)
            num_fragment = num_str[:-2]
            output_dirname = opj(options.dest_path, num_fragment)
            output_filename = num_str + ".txt"
            output_filename_with_dir = opj(output_dirname, output_filename)
            pathlib.Path(output_dirname).mkdir(parents=True, exist_ok=True)
            with open(opj(output_filename_with_dir), "w") as fh:
                fh.write(cleaned)
            item["gd-num-padded"] = num_str
            item["gd-path"] = opj(num_fragment, output_filename)
            metadata.append(item)
            if i % 1000 == 0:
                err("processing", item["Num"], "-", item["Title"][0])
            if options.limit is not None and i > options.offset + options.limit:
                err("Stopping early (--limit)")
                break
        except (UnicodeDecodeError, BadZipFile, NotImplementedError,
                FileNotFoundError) as e:
            errors.append((item, e))

    err("Done.")
    err("Writing metadata...")
    metadata.sort(key=lambda x: x["gd-num-padded"])
    with open(options.metadata_file, "w") as fh:
        json.dump(metadata, fh, indent=4, sort_keys=True)
    err("Done.")

    if len(errors) > 0:
        print("Errors:")
        for item in errors:
            print("*", item[0]["Num"], item[0]["href"], ":", item[1])

