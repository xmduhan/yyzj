#!/usr/bin/env python
# encoding: utf-8

import config
import poplib
import chardet
import shutil
import environment
import lfasr
from dateutil.parser import parse
from email import message_from_bytes
from email import header
from db import models
from os import path
import tempfile
from glob import glob
from subprocess import call
from time import sleep
del environment


def decode_header(s):
    part_list = []
    for part, code in header.decode_header(s):
        code = 'ascii' if code is None else code
        code = chardet.detect(part)['encoding'] if 'unknown' in code else code
        part_list.append(part.decode(code) if type(part) is bytes else part)
    return ''.join(part_list)


def read_mail():
    """ """
    server = poplib.POP3_SSL(config.pop3_address)
    server.user(config.pop3_user)
    server.pass_(config.pop3_password)

    for _, istr in enumerate(server.list()[1][::-1][:100], 1):
        i = int(istr.split()[0])
        try:
            # Fetch mail from server
            for __ in range(10):
                try:
                    resp, lines, octets = server.retr(i)
                    break
                except Exception:
                    sleep(1)
            else:
                print('Fetch mail: %d failed' % i)
                continue

            # Decode infomation
            message = message_from_bytes(b'\n'.join(lines))
            subject = decode_header(message.get('Subject'))
            mailfrom = decode_header(message.get('From'))
            date = parse(message.get('Date'), fuzzy=True)
            message_id = message.get('Message-ID')

            # Save mail to database
            mail_model, created = models.MailModel.objects.get_or_create(message_id=message_id)

            if created:
                print('New mail:', subject, mailfrom, date, message_id)
                mail_model.__dict__.update(subject=subject, date=date, mailfrom=mailfrom)
                if subject == '语音质检':
                    batch_model = models.BatchModel(mail=mail_model, state='processing')
                    batch_model.save()

                    # Save attachment files
                    tempdir = tempfile.mkdtemp(dir='wav')
                    for part in message.walk():
                        if part.get_content_disposition() == 'attachment':
                            filename = decode_header(part.get_filename())
                            data = part.get_payload(decode=True)
                            f = open(path.join(tempdir, filename), 'wb')
                            f.write(data)
                            f.close()

                    # Extract zip files if exists
                    for filename in glob(path.join(tempdir, '**/*.zip'), recursive=True):
                        # print(filename, ''.join(filename.split('.')[:-1]))
                        call(['unzip', filename, '-d', ''.join(filename.split('.')[:-1])])
                        call(['rm', filename])
                        print('Extract %s ...' % filename)

                    # Upload all wav file
                    for filename in glob(path.join(tempdir, '**/*.wav'), recursive=True):
                        lfasr_model = lfasr.add_task(filename)
                        batch_item_model = models.BatchItemModel(filename=filename, batch=batch_model, lfasr=lfasr_model)
                        batch_item_model.save()
                        print('New wav file upload:', filename)

                    # Remove all temp files
                    shutil.rmtree(tempdir)

            mail_model.save()
        except Exception as e:
            print(_, e)


def main():
    """ """
    while True:
        read_mail()
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lfasr.gateway = None
