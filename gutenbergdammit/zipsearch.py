import zipfile
import json

def loadmetadata(zipfn):
    with zipfile.ZipFile(zipfn) as zfh:
        with zfh.open("gutenberg-dammit-files/gutenberg-metadata.json") as jfh:
            return json.load(jfh)

def search(metadata, fields=None, op=all):
    """Simple function for finding matching items in the metadata file.

    Pass a the metadata list and a dictionary mapping field names from the
    metadata items to either strings or callables. If the value for a field is
    a string, matching items will have that string as a substring in the
    concatenated values from the corresponding value in the metadata. If the
    value is a callable, matching items will be those for which the callable
    returns True when passed the value for the field in the item's metadata.

    Specify all as the "op" parameter to require all fields to match (AND) or
    any to require only that one field matches."""

    if fields is None:
        fields = {}
    matches = []
    for item in metadata:
        bools = []
        for k, v in fields.items():
            if k not in item:
                bools.append(False)
                continue
            if type(item[k]) is list:
                search_against = "\n".join(item[k])
            else:
                search_against = item[k]
            if type(v) is str:
                bools.append(v in search_against)
            elif callable(v):
                bools.append(v(search_against))
        if len(bools) > 0 and op(bools):
            matches.append(item)
    return matches

def retrieve(zipfn, paths):
    with zipfile.ZipFile(zipfn) as zfh:
        for path in paths:
            yield zfh.open(path).read().decode('utf8')

def searchandretrieve(zipfn, fields, op=all):
    metadata = loadmetadata(zipfn)
    matches = search(metadata, fields, op)
    for tup in zip(matches, retrieve(zipfn,
            ["gutenberg-dammit-files/" + x['gd-path'] for x in matches])):
        yield tup

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    fields = {
            "author": "Author",
            "rights": "Copyright Status",
            "language": "Language",
            "subject": "Subject",
            "title": "Title"}
    for k, v in fields.items():
        parser.add_option("--" + k,
                help="records with value in " + v,
                default=None)
    parser.add_option("--srczip",
            help="path to gutenberg-dammit-files zip",
            default="gutenberg-dammit-files.zip")
    parser.add_option("--excerpt-length",
            help="length of excerpt to display",
            type="int",
            default=60)
    parser.add_option("--op",
            help="conditions operation: all (logical AND) or any (logical OR)",
            type="choice",
            choices=("all", "any"),
            default="all")
    options, _ = parser.parse_args()

    search_op = {"all": all, "any": any}[options.op]
    search_dict = {fields[k]: getattr(options, k) for k in fields.keys() 
            if getattr(options, k) is not None}
    for tup in searchandretrieve(options.srczip, search_dict, search_op):
        print(json.dumps(tup[0]), "\t",
                tup[1][:options.excerpt_length].replace("\n", " "))

