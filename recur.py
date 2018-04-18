import os
from pathlib import Path


def startswith(pth_name):
    ''' Checks for "." path names'''
    a = os.path.basename(pth_name)
    try:
        if a[0] == ".":
            return True
    except IndexError:
        return True
    else:
        return False


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.3f %s" % (num, x)
        num /= 1024.0


def get_fsize(pth_name):
    '''Returns size of file'''
    try:
        return os.path.getsize(pth_name)
    except FileNotFoundError:
        return 0


def null_check(pth_name):
    if "MB" in convert_bytes(get_fsize(pth_name)):
        return True
    if "GB" in convert_bytes(get_fsize(pth_name)):
        return True
    return False


def chk_dir(pth_name):
    '''True for no sub directories and false if sub directories present.
       Directory of this type has been referred to as absolute directory.''' 
    if startswith(pth_name):
        return False
    elif os.path.isfile(pth_name):
        return False
    elif os.path.isdir(pth_name):
        for i in os.scandir(pth_name):
            if os.path.isdir(i):
                return False
    return True


def list_size(pth_name):
    '''Returns list of size of each file in an absolute directory'''
    if chk_dir(pth_name):
        size = []
        sort_l = []
        for i in os.scandir(pth_name):
            if null_check(pth_name):
                size.append((i, get_fsize(i)))
                sort_l.append(get_fsize(i))
        temp = size
        size = []
        sort_l.sort(reverse=True)
        for j in sort_l:
            for i in range(len(temp)):
                if j == temp[i][1]:
                    size.append(temp[i])
        return size
    return 0


def top_size(pth_name):
    ''' Returns an unsorted list of tuples with filenames(PosixDirEntry) and sizes(in bytes).
        Every element is a tuple = (filename,size).'''
    size = []
    if os.path.isdir(pth_name):
        if chk_dir(pth_name):
            size = list_size(pth_name)
            return size
        for i in os.scandir(pth_name):
            if os.path.isfile(i) and null_check(i):
                size.append((i, get_fsize(i)))
            if os.path.isdir(i) and os.path.basename(i) != "Library":
                '''Library folder has been excluded to reduce build time.'''
                if chk_dir(i):
                    for j in top_size(i):
                        size.append(j)
                if not chk_dir(i):
                    for j in top_size(i):
                        size.append(j)
    return size


def top_ten(pth_name):
    '''RETURNS THE FINAL SORTED LIST '''
    first = top_size(pth_name)
    temp1 = []
    temp2 = []
    final = []
    for i in range(len(first)):
        temp1.append(first[i][1])
    temp1.sort(reverse=True)
    if len(temp1) > 10:
        temp1 = temp1[:10]
    for j in temp1:
        for i in range(len(first)):
            if j == first[i][1]:
                temp2.append(first[i])
    for j in range(len(temp2)):
        a = convert_bytes(temp2[j][1])
        final.append((temp2[j][0], a))
    return final

pth_name = input("Enter the name of the user :")
for i in top_ten("/users/" + pth_name):
    print(i)
