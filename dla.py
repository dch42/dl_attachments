#!/usr/bin/env python3
"""Download and print email attachments"""
import os
import sys
import argparse
import imaplib
import email
from pathlib import Path
from tqdm import tqdm
import yaml
import cfg_crypt as cc

# define and parse args
parser = argparse.ArgumentParser(
    description="Download and print email attachments")
parser.add_argument(
    "-d", "--download", help='download email attachments', action="store_true")
parser.add_argument(
    "-p", "--print", help='print downloaded attachments', action="store_true")
parser.add_argument(
    "-s", "--seenflag", help='set `seen` flag on processed emails', action="store_true")
parser.add_argument(
    "-u", "--unseen", help='search for messages marked `unseen`', action='store_true')
parser.add_argument(
    "-a", "--address", type=str, nargs='+', help='search for messages from address(es)')
parser.add_argument("-i", "--inbox", type=str, nargs='+',
                    help='search inbox(es)')
parser.add_argument("-t", "--terms", type=str, nargs='+',
                    help='search subjects for term(s)')
args = parser.parse_args()

# open mailboxes as read only unless setting seen flags
RO = not args.seenflag

SCRIPT = "dla"
hidden_path = cc.make_hidden_dir(SCRIPT)


def crypt_cfg():
    """Create fernet encrypted cfg if not exists, decrypt"""
    if not os.path.exists(f'{hidden_path}/.{SCRIPT}.key'):
        print("No key detected...")
        cc.gen_key(hidden_path, SCRIPT)
    if not os.path.exists(f'{hidden_path}/.{SCRIPT}_cfg'):
        login_info = cc.gen_cfg()
        key = cc.read_key(hidden_path, SCRIPT)
        cc.encrypt_cfg(login_info, key, hidden_path, SCRIPT)
    key = cc.read_key(hidden_path, SCRIPT)
    crypt_login = cc.decrypt_cfg(key, hidden_path, SCRIPT)
    return crypt_login


def yaml_cfg():
    """Load YAML config file"""
    with open(f'{hidden_path}/{SCRIPT}_config.yml', 'r') as stream:
        try:
            cfg = (yaml.safe_load(stream))
            return cfg
        except Exception as e:
            print(e)


def make_dir_if_no(dir1, dir2):
    """Make dir if not exists"""
    if not os.path.exists(f'{dir1}/{dir2}'):
        os.makedirs(f'{dir1}/{dir2}')


def sort_files(destination, dir1, item):
    """Move file(s) from one dir to another"""
    make_dir_if_no(dir1, destination)
    file_sort = f"mv {dir1}/{item} {dir1}/{destination}/"
    os.system(file_sort)


def init_imap():
    """Initialize connection object"""
    imap_obj = imaplib.IMAP4_SSL(host=IMAP_HOST, port=PORT)
    print("Logging in to mailbox...")
    resp_code, response = imap_obj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print(f"Response Code : {resp_code}")
    print(f"Response      : {response[0].decode()}\n")
    return imap_obj


def set_mailbox(imap_obj):
    """Set mailbox and begin loop"""
    if args.inbox:
        if len(args.inbox) >= 1:
            for arg in args.inbox:
                imap_obj.select(
                    mailbox=f'{ROOT_INBOX}/{arg}', readonly=RO)
                search_mail(imap_obj)
    else:
        imap_obj.select(mailbox=f'{ROOT_INBOX}', readonly=RO)
        search_mail(imap_obj)


def create_query(term=False, address=False):
    """Build query string for mailbox"""
    query = '%s%s%s' % ("UNSEEN " if args.unseen else '',
                        f'FROM "{address}" ' if args.address else '', f'SUBJECT "{term}" ' if args.terms else '')
    query = query.rstrip()
    return query


def get_mail_list(imap_obj, query):
    """Return list of mails matching query"""
    mail = imap_obj.search(None, f'({query})')[1]
    return mail


def search_mail(imap_obj):
    """Search mailbox"""
    if args.terms and args.address:
        for address in args.address:
            for term in args.terms:
                query = create_query(term=term, address=address)
                mail = get_mail_list(imap_obj, query)
                list_mail(imap_obj, mail)
    elif args.terms and not args.address:
        for term in args.terms:
            query = create_query(term=term)
            mail = get_mail_list(imap_obj, query)
            list_mail(imap_obj, mail)
    elif args.address and not args.terms:
        for address in args.address:
            query = create_query(term=False, address=address)
            mail = get_mail_list(imap_obj, query)
            list_mail(imap_obj, mail)
    else:
        if args.unseen:
            mail = imap_obj.search(None, "UNSEEN")[1]
            list_mail(imap_obj, mail)
        else:
            mail = imap_obj.search(None, "ALL")[1]
            list_mail(imap_obj, mail)


def list_mail(imap_obj, mails):
    """Loop through messages"""
    mail_ids = mails[0].decode().split()
    print(f"{len(mail_ids)} emails found...\n")
    for uid in tqdm((mail_ids), file=sys.stdout):
        mail_data = imap_obj.fetch(uid, '(RFC822)')[1]
        message = email.message_from_bytes(mail_data[0][1])
        tqdm.write(
            '='*20+f'[#{uid}]'+'='*20+f'\
            \n\033[96mFROM:  {message["From"]}\
            \n\033[93mSUBJ:  "{message["Subject"]}" \
            \n\033[96mDATE:  ({message["Date"]})\033[00m\n')
        dl_attachments(DL_DIR, message, uid, imap_obj)


def dl_attachments(DL_DIR, message, uid, imap_ssl):
    """Downloads pdf/doc attachments from applicable email messages"""
    for part in message.walk():
        if part.get_content_type() == "multipart":
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        data = part.get_payload(decode=True)
        if not data:
            continue
        if filename is not None:
            if filename.endswith(tuple(EXTENSIONS)):
                with open(os.path.join(DL_DIR, filename), 'wb') as f:
                    f.write(data)
                    tqdm.write(
                        f"\033[5m==>\033[0m \033[92m[DOWNLOAD SUCCESSFUL] `{filename}`!\033[0m\n")
                    if args.print:
                        print_file(filename)
    if args.seenflag:
        imap_ssl.uid("STORE", uid, '+FLAGS', '\\Seen')


def print_file(filename):
    """Print files"""
    file_to_print = os.path.join(DL_DIR, filename)
    os.system(
        f'lpr -P {MAIN_PRINTER} -o media={MEDIA} "{file_to_print}"')
    tqdm.write(f'Printing {file_to_print}...')
    make_dir_if_no(DL_DIR, 'printed')
    sort_files('printed', DL_DIR, filename)


def print_all():
    """Print all files in dl dir"""
    print_dir = Path(f'{DL_DIR}')
    files = print_dir.iterdir()
    for item in tqdm(files, file=sys.stdout):
        if item.is_file():
            filename = item.name
            file_to_print = os.path.join(DL_DIR, filename)
        else:
            break
        if file_to_print.endswith('.pdf'):
            print_file(file_to_print)


###########################################################################

if __name__ == '__main__':
    # encrypt/decrypt login info
    crypt_login = crypt_cfg()
    EMAIL_ADDRESS, EMAIL_PASSWORD = crypt_login['EMAIL'], crypt_login['PW']
    # load and parse cfg file
    cfg = yaml_cfg()

    IMAP_HOST = (cfg['EMAIL_INFO']['IMAP_HOST'])
    PORT = (cfg['EMAIL_INFO']['PORT'])
    ROOT_INBOX = (cfg['EMAIL_INFO']['ROOT_INBOX'])
    DL_DIR = (cfg['DOWNLOAD_DIRECTORY'])
    MAIN_PRINTER = (cfg['MAIN_PRINTER'])
    MEDIA = (cfg['MEDIA'])
    EXTENSIONS = (cfg['EXTENSIONS_TO_DOWNLOAD'])

    if args.download:
        imap_obj = init_imap()
        set_mailbox(imap_obj)
        imap_obj.close()
    if args.print and not args.download:
        print_all()
