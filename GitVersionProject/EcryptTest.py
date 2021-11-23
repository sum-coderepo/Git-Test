import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.fernet import Fernet
message = "my deep dark secret".encode()
key = Fernet.generate_key()
f = Fernet(key)

print(key)
in_file_name = 'C:\\Users\\sumeet\\IdeaProjects\\VersionControlAOS\\GitVersion\\Dir1\\essay001.txt'
out_file_name = 'C:\\Users\\sumeet\\IdeaProjects\\VersionControlAOS\\GitVersion\\Dir1\\encypted.txt'
out_decrypt_name = 'C:\\Users\\sumeet\\IdeaProjects\\VersionControlAOS\\GitVersion\\Dir1\\decypted.txt'

with open(in_file_name, "rb") as fin, open(out_file_name, "wb") as fout:
    while True:
        block = fin.read(4096)
        if not block:
            break
        f = Fernet(key)
        output = f.encrypt(block)
        fout.write(output)

#
# decrypt
#
in_file_name = out_file_name
out_file_name = out_decrypt_name
with open(in_file_name, "rb") as fin, open(out_file_name, "wb") as fout:
    while True:
        block = fin.read(4096)
        if not block:
            break
        f = Fernet(key)
        output = f.decrypt(block)
        fout.write(output)