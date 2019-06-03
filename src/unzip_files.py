import zipfile
import sys
import os


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Need 2 arguments, {input}, {destination}')
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f'file: {sys.argv[1]} does not exist')
        exit(1)

    if not os.path.isdir(sys.argv[2]):
        os.makedirs(sys.argv[2], 0o777, exist_ok=True)

    zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])
