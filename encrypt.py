#!/usr/bin/env python3
import argparse
import os
from cogs.utils import crypto 

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--decrypt', action='store_true')
parser.add_argument('file', help='path to unecrypted file')
parser.add_argument('aes', nargs='?', const=None,
        help='path to ecrypted file; defaults to $file.aes')

args = parser.parse_args()
if not args.aes:
    args.aes = args.file + '.aes'

method = crypto.file_encrypt
if args.decrypt:
    method = crypto.file_decrypt

cryptokey = os.getenv('CRYPTOKEY', '').encode('utf-8')

method(cryptokey, args.file, args.aes)




