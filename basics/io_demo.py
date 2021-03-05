with open("arrays.py") as f:
    print(f.readlines())

# copy file
with open("copy_of_readme.md", "w") as wf:
    with open("Readme.md", "r") as rf:
        file_content = rf.read()
        wf.write(file_content)
