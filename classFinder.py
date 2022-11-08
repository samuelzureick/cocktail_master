import difflib

f = open("classes.txt")
classes = f.readlines()
f.close()
classes = [c.replace("\n", "") for c in classes]
print(difflib.get_close_matches("Fernet Bra", classes))