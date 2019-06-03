#!/usr/bin/env python
"""
Pulled from: https://github.com/jzlotek/threaded-download-py

Usage is for large simultaneous file download
It seems as if small downloads have minimal affect
in terms of speed up across multiple threads due
to the overhead of setting the threads up.
-v Verbose option also slows down script execution for smaller files
"""

import threading
import sys
import requests
import time
import os


def split_url_list(urls, num):
    ret = [[] for x in range(num)]

    for x in range(len(urls)):
        ret[x % num].append(urls[x])

    return filter(lambda l: len(l) > 0, ret)


def runner(progress, files, directory, printing=False, no_clobber=True):
    if printing:
        progress[3] = len(files)

    for f_name in files:
        r = requests.get(f_name, stream=True)
        local_filename = f_name.split('/')[-1]
        if printing:
            progress[2] += 1
            progress[1] = local_filename
            size_max = r.headers['Content-Length']
            size_dl = 0

        if no_clobber and os.path.isfile(directory + local_filename):
            counter = 0
            s = local_filename.split('.')
            ext = s.pop(-1)
            s.append(str(counter))

            while os.path.isfile(directory + "_".join(s) + '.' + ext):
                counter += 1
                s[-1] = str(counter)

            local_filename = "_".join(s) + '.' + ext
            if printing:
                progress[1] = local_filename

        with open(directory + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    if printing:
                        size_dl += len(chunk)
                        progress[0] = float(size_dl) / float(size_max) * 100
                    f.write(chunk)

    return


def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()


def progress_print(p):

    for x in p:
        print()

    while threading.active_count() > 2:
        string = ""
        for x in p:
            up()
        for x in range(len(p)):
            string += "[%-20s] %-6.2f%% < %s > (%d of %d)\n" % (
                                                '=' * (int(p[x][0]/5)-1) + '>',
                                                float(p[x][0]),
                                                p[x][1] if p[x][1] else "",
                                                p[x][2],
                                                p[x][3])

        sys.stdout.write(string)
        sys.stdout.flush()


if __name__ == "__main__":
    threads = []
    num = 1
    printing = False
    directory = './'
    no_clobber = True

    if '-t' in sys.argv:
        try:
            num = int(sys.argv[sys.argv.index('-t') + 1])
        except Exception as e:
            print("Error trying to parse thread count | option: -t")
            exit(1)

    if '-d' in sys.argv:
        try:
            directory = str(sys.argv[sys.argv.index('-d') + 1])
            if directory[0] != '~':
                directory = './' + directory
            directory += '/'
            if not os.path.exists(directory):
                os.makedirs(directory)

        except Exception as e:
            print("Error trying to parse directory | option: -d")
            exit(1)

    if '--clobber' in sys.argv:
        no_clobber = False

    files = []

    for line in sys.stdin:
        files.append(line.strip())

    if len(files) == 0:
        print("No urls provided...")
        exit(1)

    files = list(split_url_list(files, num))

    # make sure we don't spawn additional threads
    if len(files) < num:
        num = len(files)

    progress = [[0, None, 0, 0] for x in range(num)]

    printing_thread = None
    if '-v' in sys.argv:
        printing = True
        printing_thread = threading.Thread(target=progress_print,
                                        args=(progress,))

    for x in range(num):
        threads.append(threading.Thread(target=runner,
                                        args=(progress[x],
                                              files[x],
                                              directory,
                                              printing,
                                              no_clobber)))
    timer = time.time()

    if printing_thread is not None:
        printing_thread.start()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    if printing_thread is not None:
        printing_thread.join()

    timer = time.time() - timer
    if printing:
        print("Elapsed time: %-10.6fs" % timer)
