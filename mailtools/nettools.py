#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mailsvs.py: Provides POP3-client, IMAP-client, SMTP-client.
"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import webbrowser
import tempfile
import getpass
import imaplib
import smtplib
import poplib
import ftplib
import base64
import email
import re
import os


poplib._MAXLINE = 20480

if load_dotenv('.env', encoding='UTF-8') is True:
    POP3_MAIL_SERVER = os.getenv('POP3_MAIL_SERVER')
    IMAP_MAIL_SERVER = os.getenv('IMAP_MAIL_SERVER')
    SMTP_MAIL_SERVER = os.getenv('SMTP_MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    FTP_SERVER = os.getenv('FTP_SERVER')
    FTP_USERNAME = os.getenv('FTP_USERNAME')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD')
else:
    raise Exception('Failed to read ENV variables')


def email_to_html(parsed: str) -> str:
    """
    email_to_html is a function that convert parsed email to html via "email" module.

    Args:
        parsed (str): parsed email message.

    Returns:
        str: prepared message in html format.
    """
    all_parts = []
    for part in parsed.walk():
        if type(part.get_payload()) == list:
            for subpart in part.get_payload():
                all_parts += email_to_html(subpart)
        else:
            if encoding := part.get_content_charset():
                all_parts.append(part.get_payload(decode=True).decode(encoding))
    return ''.join(all_parts)


def display(html: str) -> None:
    """
    display is a function that displays html message.

    Args:
        html (str): message in html format.
    """
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(html)
        webbrowser.open(url)


def pop3() -> None:
    """
    pop3: Function which implements POP3-client.
    It allows reading messages from your mailbox.
    It also allows printing and deleting them.
    """
    server_name = input(f'POP3 server("{POP3_MAIL_SERVER}" by default): ') or POP3_MAIL_SERVER
    username = input(f'Username("{MAIL_USERNAME}" by default): ') or MAIL_USERNAME
    password = getpass.getpass(f'Password("{MAIL_PASSWORD[:4]}***" by default): ') or MAIL_PASSWORD

    try:
        server = poplib.POP3_SSL(server_name)
        server.user(username)
        server.pass_(password)

        print('-' * 80)
        print(f'Connection has been created. Server response: {server.getwelcome()}')
        message_count, mailbox_size = server.stat()
        print(f'Messages: {message_count}, Mailbox size: {mailbox_size}')

        messages_info = server.list()

        for i in range(message_count, 0, -1):
            message_num = i - 1
            message_size = messages_info[1][message_count - i].split()[1]
            response, header_lines, chapter_size = server.top(message_num, 0)

            print('-' * 80)
            print(f'{message_num}) Chapter size: {chapter_size}, Message size: {int(message_size)}')
            header_lines = [line for line in header_lines if re.match(b'From:|To:|Subject:', line)]
            for line in header_lines:
                if b'?' in line:
                    line_parts = line.split(b'?')
                    charset, method, message = line_parts[1:4]

                    if method == b'B':
                        message = base64.b64decode(message).decode(charset.decode())
                        line = line_parts[0].split()[0].decode() + ' ' + message

                print(line.strip() if isinstance(line, str) else line.decode().strip())

            print('-' * 80)

            if input('Print? Y/Any: ') in ['y', 'Y']:
                raw_email = b'\n'.join(server.retr(message_num)[1])
                parsed = email.message_from_bytes(raw_email)
                display(email_to_html(parsed))

            if input('Delete? Y/Any: ') in ['y', 'Y']:
                server.dele(message_num)
                print('Message has been successfully deleted.')

            if input('Exit? Y/Any: ') in ['y', 'Y']:
                break
    finally:
        server.quit()


def imap() -> None:
    """
    imap: Function which implements IMAP-client.
    It allows reading messages from your mailbox.
    It also allows printing and deleting them.
    """
    server_name = input(f'IMAP server("{IMAP_MAIL_SERVER}" by default): ') or IMAP_MAIL_SERVER
    username = input(f'Username("{MAIL_USERNAME}" by default): ') or MAIL_USERNAME
    password = getpass.getpass(f'Password("{MAIL_PASSWORD[:4]}***" by default): ') or MAIL_PASSWORD

    try:
        server = imaplib.IMAP4_SSL(server_name)
        server.login(username, password)

        print('-' * 80)
        server_response, message_count = server.select()
        print(f'Connection has been created. Server response: {server_response}')
        print(f'Messages: {message_count}')

        message_set = server.search(None, 'ALL')[1]

        for msg in reversed(message_set[0].split()):
            typ, data = server.fetch(msg, '(RFC822)')

            print('-' * 80)
            header_lines = data[0][1].split(b'\r\n')
            header_lines = [line for line in header_lines if re.match(b'From:|To:|Subject:', line)]

            for line in header_lines:
                if b'?' in line:
                    line_parts = line.split(b'?')
                    charset, method, message = line_parts[1:4]

                    if method == b'B':
                        message = base64.b64decode(message).decode(charset.decode())
                        line = line_parts[0].split()[0].decode() + ' ' + message

                print(line.strip() if isinstance(line, str) else line.decode().strip())

            print('-' * 80)

            if input('Print? Y/Any: ') in ['y', 'Y']:
                raw_email = data[0][1]
                parsed = email.message_from_bytes(raw_email)
                display(email_to_html(parsed))

            if input('Delete? Y/Any: ') in ['y', 'Y']:
                server.store(msg, command='+FLAGS', flags=r'\Deleted')
                print('Message has been successfully deleted.')

            if input('Exit? Y/Any: ') in ['y', 'Y']:
                break

    finally:
        server.expunge()
        server.shutdown()


def smtp() -> None:
    """
    smtp: Function which implements SMTP-client.
    It allows sending messages from your mbox to others.
    """
    server_name = input(f'SMTP server("{SMTP_MAIL_SERVER}" by default): ') or SMTP_MAIL_SERVER
    username = input(f'Username("{MAIL_USERNAME}" by default): ') or MAIL_USERNAME
    password = getpass.getpass(f'Password("{MAIL_PASSWORD[:4]}***" by default): ') or MAIL_PASSWORD

    try:
        server = smtplib.SMTP_SSL(server_name)
        server.login(username, password)
        server.set_debuglevel(2)

        while True:
            toaddrs = input('To: ').strip().split()

            if not toaddrs:
                print('Wrong destination address(es)')
                continue

            msg = MIMEMultipart("alternative")
            msg.set_charset("utf-8")
            msg['Subject'] = input('Subject: ').strip()
            text = MIMEText(input('Message: '), 'plain')
            msg.attach(text)
            server.sendmail(username, toaddrs, msg.as_string())

            if input('Exit? Y/Any: ') in ['y', 'Y']:
                break

    finally:
        server.quit()


def ftp() -> None:
    """
    ftp: Function which implements FTP-client.
    It allows manipulating with files on the FTP server.
    """
    server_name = input(f'FTP server("{FTP_SERVER}" by default): ') or FTP_SERVER
    username = input(f'Username("{FTP_USERNAME}" by default): ') or FTP_USERNAME
    password = getpass.getpass(f'Password("{FTP_PASSWORD[:4]}***" by default): ') or FTP_PASSWORD

    try:
        server = ftplib.FTP(server_name)
        server.login(user=username, passwd=password)
        print(f'Connection has been created. Server response: {server.getwelcome()}')

        while True:
            print('1 - Change dir')
            print('2 - Download file')
            print('3 - Upload file')
            print('4 - List dir')
            print('5 - Back')

            match input('>>> '):
                case '1':
                    server.cwd(input('$ '))
                    continue
                case '2':
                    try:
                        filename = input('filename: ').strip()
                        location = input('save to: ').strip()
                        with open(location + os.sep + filename, 'wb') as fp:
                            server.retrbinary(f'RETR {filename}', fp.write)
                        continue
                    except Exception as error:
                        print('Error', error)
                        os.remove(location + os.sep + filename)
                case '3':
                    try:
                        filename = input('filename: ').strip()
                        location = input('save to: ').strip()
                        with open(location + os.sep + filename, 'rb') as fp:
                            server.storbinary(f'STOR {filename}', fp.read)
                        continue
                    except Exception as error:
                        print('Error', error)
                case '4':
                    server.dir()
                    continue
                case '5':
                    break
                case _:
                    print('Incorrent input. Try again.')
    finally:
        server.close()


if __name__ == '__main__':
    while True:
        print('1 - POP3 protocol')
        print('2 - IMAP protocol')
        print('3 - SMTP protocol')
        print('4 - FTP protocol')
        print('5 - Exit')

        match input('>>> '):
            case '1':
                pop3()
                continue
            case '2':
                imap()
                continue
            case '3':
                smtp()
                continue
            case '4':
                ftp()
                continue
            case '5':
                break
            case _:
                print('Incorrent input. Try again.')
