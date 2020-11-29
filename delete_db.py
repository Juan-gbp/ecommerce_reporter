import glob
import os


# glob will find any file that has the ending .rdb
for file in glob.glob("*.rdb"):
    # then for each file found, the file is removed entirely
    os.remove(file)
