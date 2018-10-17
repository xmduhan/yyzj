#!/usr/bin/env python
# encoding: utf-8

import config

import poplib
import smtplib
import chardet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import pandas as pd
from collections import OrderedDict
from datetime import datetime
import shutil
import environment
from django.db.models import Q
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
                    try:
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
                    finally:
                        # Remove all temp files
                        shutil.rmtree(tempdir)

            mail_model.save()
        except Exception as e:
            print(_, e)


def send_mail(receivers, title, content, attachments=[], encoding='utf-8'):
    """ """
    smtpServer = config.smtp_address
    smtpPort = config.smtp_port
    smtpUser = config.smtp_user
    smtpPassword = config.smtp_password
    smtpSender = config.smtp_user

    message = MIMEMultipart()
    contentPart = MIMEText(content, _subtype='html', _charset=encoding)
    message.attach(contentPart)

    # 创建附件部分
    for filename in attachments[::-1]:
        # 获取不含路径的文件名
        fn = path.split(filename)[-1]
        attMimeText = MIMEText(open(filename, 'rb').read(), 'base64', encoding)
        attMimeText["Content-Type"] = 'application/octet-stream'
        attMimeText["Content-Disposition"] = u'attachment; filename="%s"' % header.Header(fn).encode(encoding)
        message.attach(attMimeText)

    # Add Header
    message['to'] = ','.join(receivers)
    message['from'] = smtpSender
    message['subject'] = title

    # Send it
    smtp = smtplib.SMTP_SSL(smtpServer, smtpPort)
    smtp.login(smtpUser, smtpPassword)
    smtp.sendmail(smtpSender, receivers, message.as_string())
    smtp.quit()

    # 返回成功
    return True


def send_feedback():
    """ """
    for batch_model in models.BatchModel.objects.filter(state='processing'):
        qs = batch_model.batchitemmodel_set.filter(~Q(lfasr__step='finish'))
        if len(qs) == 0:
            print('Send feedback for mail: %s' % batch_model.mail.message_id)
            data_list = []
            for item_model in batch_model.batchitemmodel_set.all():
                lfasr = json.loads(item_model.lfasr.data)
                data = OrderedDict()
                data['filename'] = path.join(*item_model.filename.split('/')[2:])
                data['lfasr'] = ','.join([seg['onebest'] for seg in lfasr])
                data_list.append(data)
            df = pd.DataFrame(data_list)

            tempdir = tempfile.mkdtemp(dir='/tmp')
            try:
                # Set finish flag
                batch_model.state = 'finish'
                batch_model.save()

                filename = path.join(tempdir, '结果.xls')
                df.to_excel(filename)

                receivers = [batch_model.mail.mailfrom]
                title = '质检结果'
                content = '''
                触发邮件时间: %s
                ''' % datetime.strftime(batch_model.mail.date, '%Y-%m-%d %H:%M:%S')
                send_mail(receivers, title, content, [filename])

            finally:
                shutil.rmtree(tempdir)


def main():
    """ """
    while True:
        read_mail()
        send_feedback()
        sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lfasr.gateway = None
