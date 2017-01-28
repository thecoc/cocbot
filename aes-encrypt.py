from cogs.utils import crypto
import os

key = os.getenv('CRYPTOKEY', '').encode('utf-8')
crypto.file_encrypt(key, 'config.json')