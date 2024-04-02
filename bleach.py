#!/usr/bin/env python3

'''
In the spirit of Perl's Acme::Bleach, some routines that can get rid of those
pesky and unsighly printable characters.

4/2024 David Jacobowitz
'''

import functools, io

def bleach(ifh, ofh):
    while b:= ifh.read(1):
        ofh.write(''.join([ (' ','\t')[x] for x in [ bool(b[0] & (1<<i)) for i in range(8) ] ]))

def unbleach(ifh, ofh):
    while b := ifh.read(8):
        # print('b', [ ord(b[i]) for i in range(8) ])
        y = functools.reduce(lambda y, i: {' ':0,'\t':1}[b[i]] * (1<<i) + y, range(8), 0)
        ofh.write(bytes((y,)))

def run(s):
    ofh = io.BytesIO()
    unbleach(io.StringIO(s), ofh)
    ofh.seek(0)
    os = ofh.read().decode('utf-8')
    exec(os)

def bleachscript(ifh, ofh):
    fakeofh = io.StringIO()
    bleach(ifh, fakeofh)
    fakeofh.seek(0)
    s = fakeofh.read()
    ofh.write(f'''#!/usr/bin/env python3
import bleach

bleach.run('{s}')
''')

if __name__ == '__main__':
    import argparse
    import stat, os
    def getArgs():
        p = argparse.ArgumentParser(description='bleah a file or unbleach it')
        meg = p.add_mutually_exclusive_group(required=True)
        meg.add_argument(
           '-d', '--decode',
           help='file to decode',
           type=argparse.FileType(mode='r'),
        )
        meg.add_argument(
           '-e', '--encode',
           help='file to encode',
           type=argparse.FileType(mode='rb'),
        )
        meg.add_argument(
           '-s', '--script',
           help='script to encode',
           type=argparse.FileType(mode='rb'),
        )
        p.add_argument(
            '-o', '--output',
            help='output file to write',
            default='bleach.out',
            type=str,
        )
        return p.parse_args()

    args = getArgs()
    if args.encode is not None:
        bleach(args.encode, open(args.output, 'w'))
    elif args.script is not None:
        bleachscript(args.script, open(args.output, 'w'))
        st = os.stat(args.output)
        os.chmod(args.output, os.stat(args.output).st_mode | stat.S_IEXEC)
    elif args.decode is not None:
        unbleach(args.decode, open(args.output, 'wb'))
