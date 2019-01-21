# code based on/adapted from https://github.com/julianbrooke/GutenTag
# Creative Commons Attribution-ShareAlike 4.0 International

import re
import os
import zipfile
import chardet

from gutenbergdammit.metadata import MetadataReader, MetadataReaderRDF

def setup_tag_dict(filename, corpus_dir="./PGUS"):
    num = filename[:filename.find(".")].lower()
    if filename.endswith(".rdf"):
        href, charset,tag_dict = MetadataReaderRDF().get_PG_metadata(
                corpus_dir + "/ETEXT_SUP/"+ filename)
    else:
        href, charset,tag_dict = MetadataReader().get_PG_metadata(
                corpus_dir + "/ETEXT/"+ filename)           
    tag_dict["Num"] = num
    tag_dict["href"] = href
    tag_dict["charset"] = charset
    return tag_dict

def text_info_iter(corpus_dir="./PGUS"):
    filenames = os.listdir(corpus_dir + "/ETEXT")
    if os.path.exists(corpus_dir + "/ETEXT_SUP"):
        filenames.extend(os.listdir(corpus_dir + "/ETEXT_SUP"))
    filenames.sort(key=lambda x: int(re.findall(r"^(\d+)\..*$", x)[0]))
    for filename in filenames:
        tag_dict = setup_tag_dict(filename, corpus_dir)
        yield tag_dict

def try_to_decode(raw_text, charset):
    try:
        decoded = raw_text.decode(charset)
        return decoded
    except (LookupError, UnicodeDecodeError):
        detected = chardet.detect(raw_text)
        try:
            decoded = raw_text.decode(detected['encoding'])
            return decoded
        except (TypeError, LookupError, UnicodeDecodeError):
            # last ditch: maybe it's just iso-8859-1?
            decoded = raw_text.decode("iso-8859-1")
            return decoded

def get_plain_text(href, charset, corpus_dir="./PGUS"):
    # FIXME: platform-independent path joining
    # if it looks like a text file...
    if href.lower().endswith(".txt"):
        with open(corpus_dir + href, "rb") as fh:
            raw_text = fh.read()
            return try_to_decode(raw_text, charset)
    else: # otherwise assume zip
        with zipfile.ZipFile(corpus_dir + href.upper()) as my_zip:
            with my_zip.open(my_zip.namelist()[0]) as f:
                raw_text = f.read()
                return try_to_decode(raw_text, charset)

