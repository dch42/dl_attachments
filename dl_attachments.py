#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm
import argparse
import imaplib
import email
from pathlib import Path
import yaml

with open('config.yml', 'r') as stream:
    try:
        cfg = (yaml.safe_load(stream))
    except Exception as e:
        print(e)

EMAIL_ADDRESS = (cfg['EMAIL_INFO']['EMAIL_ADDRESS'])
EMAIL_PASSWORD = (cfg['EMAIL_INFO']['EMAIL_PASSWORD'])
IMAP_HOST = (cfg['EMAIL_INFO']['IMAP_HOST'])
PORT = (cfg['EMAIL_INFO']['PORT'])

DL_DIR = (cfg['DOWNLOAD_DIRECTORY'])

extensions = (cfg['extensions_to_download'])


parser = argparse.ArgumentParser(
    description="Download and print email attachments")
parser.add_argument(
    "-d", "--download", help='download email attachments', action="store_true")
parser.add_argument(
    "-s", "--seenflag", help='set `seen` flag on processed emails', action="store_true")
parser.add_argument(
    "-u", "--unseen", help='search for messages marked `unseen`', action='store_true')
parser.add_argument(
    "-a", "--address", type=str, nargs='+', help='search for messages from address(es)')
parser.add_argument("-i", "--inbox", type=str, nargs='+',
                    help='search inbox(es)')
args = parser.parse_args()

RO = not args.seenflag


def init_imap():
    imap_ssl = imaplib.IMAP4_SSL(host=IMAP_HOST, port=PORT)
    print(f"Connection Object : {imap_ssl}\nLogging in to mailbox...")
    # login
    resp_code, response = imap_ssl.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print(f"Response Code : {resp_code}")
    print(f"Response      : {response[0].decode()}\n")
    return imap_ssl


def list_mails(imap_ssl, mails):
    mail_ids = mails[0].decode().split()
    print(f"{len(mail_ids)} emails found...\n")
    for id in tqdm((mail_ids), file=sys.stdout):
        resp_code, mail_data = imap_ssl.fetch(id, '(RFC822)')
        message = email.message_from_bytes(mail_data[0][1])
        tqdm.write(
            f'[MSG #{id}] \033[96m{message["From"]} \033[93m"{message["Subject"]}" \033[96m({message["Date"]})\033[00m\n')
        dl_attachments(DL_DIR, message, id, imap_ssl)


def dl_attachments(DL_DIR, message, id, imap_ssl):
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
        if filename.endswith(tuple(extensions)):
            with open(os.path.join(DL_DIR, filename), 'wb') as f:
                f.write(data)
                if args.seenflag:
                    imap_ssl.uid("STORE", id, '+FLAGS', '\\Seen')
                tqdm.write(
                    f"==> \033[92m[DOWNLOAD SUCCESSFUL] `{filename}`!\033[0m\n")


def set_mailbox(imap_ssl):
    if args.inbox:
        if len(args.inbox) >= 1:
            for arg in args.inbox:
                imap_ssl.select(
                    mailbox=f'Inbox/{arg}', readonly=RO)
                search_mail(imap_ssl)

    else:
        imap_ssl.select(mailbox=f'Inbox', readonly=RO)
        search_mail(imap_ssl)


def search_mail(imap_ssl):
    if args.address:
        if len(args.address) >= 1:
            for arg in args.address:
                if args.unseen:
                    resp_code, mails = imap_ssl.search(
                        None, f'(UNSEEN FROM "{arg}")')
                    list_mails(imap_ssl, mails)
                else:
                    resp_code, mails = imap_ssl.search(None, f'(FROM "{arg}")')
                    list_mails(imap_ssl, mails)
    else:
        if args.unseen:
            resp_code, mails = imap_ssl.search(None, "UNSEEN")
            list_mails(imap_ssl, mails)
        else:
            resp_code, mails = imap_ssl.search(None, "ALL")
            list_mails(imap_ssl, mails)

##########################################


if args.download:
    imap_ssl = init_imap()
    set_mailbox(imap_ssl)
imap_ssl.close()
