try:
    f = open("readme.md")
except Exception as e:
    print(e)
else:
    print(f.read())
    f.close()
finally:
    print("executing finally...")
