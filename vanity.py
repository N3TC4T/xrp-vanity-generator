# coding=utf-8
###############################################################################
# Ripple Vanity Address Generator
# !/usr/bin/python
###############################################################################
from __future__ import print_function

import argparse
import multiprocessing
import re
import sys
from ripple import genb58seed, seed2accid


class bcolors:
    HEADER = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def worker(FOUND_FLAG):
    regex = "^(r)(%s)(.+)$|^(r.+)(%s)$" % (NAME, NAME)

    seed = genb58seed()
    fpgadd, accadd, accid = seed2accid(seed)

    if _verbose:
        print(bcolors.HEADER + "[-] " + accid)

    if re.match(regex, accid):
        FOUND_FLAG.set()
        print(bcolors.OKGREEN + bcolors.BOLD + "\n[*]FOUND IT:")
        print("---------------------------------------------------")
        print("[!]ADDRESS: ", accid)
        print("[!]SEED: ", seed)
        print("---------------------------------------------------\n" + bcolors.ENDC)
        sys.exit()


def starter():
    """
    process workers initialize
    """
    numbers = 0

    print(bcolors.HEADER + "\n[!] Initializing Workers")

    m = multiprocessing.Manager()
    FOUND_FLAG = m.Event()

    print("[!] Start Workers ... \n" + bcolors.ENDC)

    try:
        while not FOUND_FLAG.is_set():
            procs = []
            for w in range(THREAD):
                numbers += 1
                process = multiprocessing.Process(target=worker, args=(FOUND_FLAG,))
                procs.append(process)
                process.start()
                if numbers % 100 == 0:
                    sys.stdout.write('.')
                if numbers % 1000 == 0:
                    sys.stdout.write("\r" + str(numbers) + ' ')

                sys.stdout.flush()
            for p in procs:
                p.join()
    except (KeyboardInterrupt, SystemExit):
        print("Caught KeyboardInterrupt, terminating workers")
        sys.exit()
    finally:
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ripple Vanity Address Generator",
        epilog="./vanity -n brian -p 4 -v"
    )

    # required argument
    parser.add_argument('-n', '--name', action="store", required=True, help='Target Name')
    # optional arguments
    parser.add_argument('-p', '--process', help='NUM of Process', type=int, default=4)
    parser.add_argument('-v', '--verbose', action='store_const', help='Verbose', const=True, default=False)

    args = parser.parse_args()

    NAME = args.name
    THREAD = args.process
    _verbose = args.verbose

    starter()
