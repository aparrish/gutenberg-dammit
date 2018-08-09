# code based on/adapted from https://github.com/julianbrooke/GutenTag
# Creative Commons Attribution-ShareAlike 4.0 International

import re
import os
import zipfile

from gutenbergdammit.textcleaner import TextCleaner
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

def get_plain_text(href, charset, corpus_dir="./PGUS"):
    encodings = ["latin-1", "utf-8"]
    if charset not in encodings:
        charset = [charset] + encodings
    # FIXME: platform-independent path joining
    with zipfile.ZipFile(corpus_dir + href.upper()) as my_zip:
        for enc in encodings:
            with my_zip.open(my_zip.namelist()[0]) as f:
                raw_text = f.read().decode(enc)
                return raw_text

