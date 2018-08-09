import sys
import os
import subprocess
from os.path import join as opj
from zipfile import ZipFile, BadZipFile
import tempfile

def fixzip(zfn):
    "nb needs absolute path!"
    with tempfile.TemporaryDirectory() as tmpdir_path:
        subprocess.run(["cp", zfn, zfn + "-orig"])
        subprocess.run(["unzip", zfn, "-d", tmpdir_path])
        subprocess.run("zip -v " + zfn + " *", cwd=tmpdir_path, shell=True)

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--src-path",
            help="path to GutenTag dump",
            default="./PGUS")
    parser.add_option("-f", "--fix",
            action="store_true", dest="fix",
            help="fix broken zips with zip/unzip in path, keep copy of orig")
    options, _ = parser.parse_args()

    for i, (root, dirs, files) in enumerate(os.walk(options.src_path)):
        if i % 1000 == 0:
            print(i, root)
        for filename in files:
            zfn = opj(root, filename)
            if not(zfn.lower().endswith(".zip")):
                continue
            try:
                with ZipFile(zfn) as zfh:
                    for fname in zfh.namelist():
                        with zfh.open(fname):
                            pass
            except (NotImplementedError, BadZipFile) as e:
                print(zfn, e)
                if options.fix:
                    print("fixing...")
                    fixzip(zfn)
                
