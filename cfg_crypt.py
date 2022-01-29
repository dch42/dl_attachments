#!/usr/bin/env python3
"""Module to create a small encrypted config file for EMAIL/PW combos"""

import getpass
import os.path
import ast
from cryptography.fernet import Fernet
from pathlib import Path
import pathlib

home_dir = Path.home()
script_name = os.path.splitext(os.path.basename(__file__))[0]


def make_hidden_dir(script_name):
    """Make hidden directory with script name in user $HOME"""
    hidden_path = pathlib.Path(f'{home_dir}/.{script_name}')
    hidden_path.mkdir(parents=True, exist_ok=True)
    return hidden_path


def gen_key(hidden_path, script_name):
    """Generate fernet encryption key"""
    print("Generating encryption key...")
    fernet_key = Fernet.generate_key()
    with open(f'{hidden_path}/.{script_name}.key', 'wb') as cfg_key:
        cfg_key.write(fernet_key)
    print(
        f"\033[5m==>\033[0m Key generated at '{hidden_path}/.{script_name}.key'\n")


def read_key(hidden_path, script_name):
    """Read encryption key"""
    with open(f'{hidden_path}/.{script_name}.key', 'rb') as filekey:
        raw_key = filekey.read()
        fernet_key = Fernet(raw_key)
    return fernet_key


def gen_cfg():
    """Generate configuration file"""
    print("Generating config file...")
    LOGIN = input("Please enter your login email: ")
    PW = getpass.getpass("Please enter your login password: ")
    login_info = '{' + f"'EMAIL': '{LOGIN}', 'PW': '{PW}'" + '}'
    return login_info


def encrypt_cfg(login_info, fernet_key, hidden_path, script_name):
    """Encrypt and save cfg file"""
    print("\nEncrypting config file...")
    encrypted = fernet_key.encrypt(bytes(login_info, 'utf-8'))
    with open(f'{hidden_path}/.{script_name}_cfg', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print('Encryption complete.')
    print(
        f"\033[5m==>\033[0m Encrypted file saved at '{hidden_path}/.{script_name}_cfg'\n")


def decrypt_cfg(fernet_key, hidden_path, script_name):
    """Decrypt bytes and convert to cfg dict"""
    with open(f'{hidden_path}/.{script_name}_cfg', 'rb') as file:
        encrypted = file.read()
    decrypted = fernet_key.decrypt(encrypted)
    decrypted_str = decrypted.decode('utf-8')
    config_dic = ast.literal_eval(decrypted_str)
    return config_dic


if __name__ == '__main__':
    hidden_path = make_hidden_dir(script_name)
    if not os.path.exists(f'{hidden_path}/.{script_name}.key'):
        print("No key detected...")
        gen_key()
    if not os.path.exists(f'{hidden_path}/.{script_name}_cfg'):
        login_info = gen_cfg()
        key = read_key()
        encrypt_cfg(login_info, key)
    key = read_key()
    cfg = decrypt_cfg(key)
