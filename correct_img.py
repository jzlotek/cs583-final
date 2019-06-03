#!/usr/bin/env python3
import sys
import os
import imageio
import src.net as net

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must provide arguments {raw}')
        exit(1)

    raw = sys.argv[1]
    dest = './'

    if not os.path.isfile(raw):
        print(f'{raw} is not a file')
        exit(1)

    ratio = int(sys.argv[2]) if len(sys.argv) == 3 else 50
    processed_img = net.net(raw, ratio)

    imageio.imwrite(f'{dest}/{raw.split(".")[0]}_{ratio}.png', processed_img)
    print(f'image created at {dest}/{raw.split(".")[0]}_{ratio}.png')
