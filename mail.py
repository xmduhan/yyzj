#!/usr/bin/env python
# encoding: utf-8

import config
import poplib
import chardet
import environment
from dateutil.parser import parse
from email import message_from_bytes
from email import header
from db import models
del environment


def decode_header(s):
    part_list = []
    for part, code in header.decode_header(s):
        code = 'ascii' if code is None else code
        code = chardet.detect(part)['encoding'] if 'unknown' in code else code
        part_list.append(part.decode(code) if type(part) is bytes else part)
    return ''.join(part_list)


def main():
    """ """
    server = poplib.POP3_SSL(config.pop3_address)
    server.user(config.pop3_user)
    server.pass_(config.pop3_password)

    for _, istr in enumerate(server.list()[1][::-1][:100], 1):
        i = int(istr.split()[0])
        try:
            resp, lines, octets = server.retr(i)
            message = message_from_bytes(b'\n'.join(lines))
            subject = decode_header(message.get('Subject'))
            mailfrom = decode_header(message.get('From'))
            date = parse(message.get('Date'), fuzzy=True)
            message_id = message.get('Message-ID')
            mail_model, created = models.MailModel.objects.get_or_create(message_id=message_id)
            if created:
                mail_model.__dict__.update(subject=subject, date=date, mailfrom=mailfrom)
            mail_model.save()
            print(_, subject, mailfrom, date, message_id)
        except Exception as e:
            print(_, e)


if __name__ == "__main__":
    main()
