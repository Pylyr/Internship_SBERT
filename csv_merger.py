import os

path = "/users/daychman/Internship_SBERT/files/"
os.chdir(path)

# get all .csv files in path
files = [f for f in os.listdir() if f.endswith(".csv")]

# copy files in one large file
with open("merged", "w") as out:
    out.write("Word A,Word B,Relation,Sentence\n")
    for file in files:
        with open(file, "r") as f:
            f.readline() # Ignore the first line 
            out.write(f.read())
            out.write("\n")



