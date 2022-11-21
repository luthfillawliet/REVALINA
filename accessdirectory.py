import os

path = "C:\\xampp\\htdocs\\python\\REWA\\TX\\"
if os.path.isdir(path):
    print("\nIt is a directory")
elif os.path.isfile(path):
    print("\nIt is a normal file")

else:
    print("It is a special file (socket, FIFO, device file)" )
print()

def current_path():
    print("Current working directory before")
    print(os.getcwd())
    print()

# Driver's code
# Printing CWD before
current_path()
# Changing the CWD
os.chdir(path)

# Printing CWD after
current_path()
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")
# print the list
print(dir_list)