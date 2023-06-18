#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mailsvs.py: Provides POP3-client, IMAP-client, SMTP-client.
"""


import getpass
import imaplib
import smtplib
import poplib
import base64
import re


POP3_MAIL_SERVER = 'pop.mail.ru'
IMAP_MAIL_SERVER = 'imap.mail.ru'
SMTP_MAIL_SERVER = 'smpt.mail.ru'



def pop3():
    """
    pop3: Function which implements POP3-client. It allows reading messages from your mailbox.
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

        for i in range(message_count):
            message_num = i + 1
            message_size = messages_info[1][i].split()[1]

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
                for line in server.retr(message_num)[1]:
                    print(line)

            if input('Delete? Y/Any: ') in ['y', 'Y']:
                server.dele(message_num)
                print('Message has been successfully deleted.')
    finally:
        server.quit()


def imap():
    """
    imap: Function which implements IMAP-client. It allows reading messages from your mailbox.
    """
    server_name = input(f'IMAP server("{IMAP_MAIL_SERVER}" by default): ') or IMAP_MAIL_SERVER
    username = input(f'Username("{MAIL_USERNAME}" by default): ') or MAIL_USERNAME
    password = getpass.getpass(f'Password("{MAIL_PASSWORD[:4]}***" by default): ') or MAIL_PASSWORD

    try:
        server = imaplib.IMAP_SSL(server_name)
        server.user(username)
        server.pass_(password)

        print('-' * 80)
        print(f'Connection has been created. Server response: {server.getwelcome()}')

        message_count, mailbox_size = server.stat()
        print(f'Messages: {message_count}, Mailbox size: {mailbox_size}')

        messages_info = server.list()

        for i in range(message_count):
            message_num = i + 1
            message_size = messages_info[1][i].split()[1]

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
                for line in server.retr(message_num)[1]:
                    print(line)

            if input('Delete? Y/Any: ') in ['y', 'Y']:
                server.dele(message_num)
                print('Message has been successfully deleted.')
    finally:
        server.quit()


def smtp():
    """
    smtp: Function which implements SMTP-client. It allows sending messages from your mbox to other.
    """
    server_name = input(f'SMTP server("{SMTP_MAIL_SERVER}" by default): ') or SMTP_MAIL_SERVER
    username = input(f'Username("{MAIL_USERNAME}" by default): ') or MAIL_USERNAME
    password = getpass.getpass(f'Password("{MAIL_PASSWORD[:4]}***" by default): ') or MAIL_PASSWORD

    try:
        server = smtplib.SMTP_SSL(server_name)
        server.user(username)
        server.pass_(password)

        print('-' * 80)
        print(f'Connection has been created. Server response: {server.getwelcome()}')

        message_count, mailbox_size = server.stat()
        print(f'Messages: {message_count}, Mailbox size: {mailbox_size}')

        messages_info = server.list()

        for i in range(message_count):
            message_num = i + 1
            message_size = messages_info[1][i].split()[1]

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
                for line in server.retr(message_num)[1]:
                    print(line)

            if input('Delete? Y/Any: ') in ['y', 'Y']:
                server.dele(message_num)
                print('Message has been successfully deleted.')
    finally:
        server.quit()


if __name__ == '__main__':
    while True:
        print('1 - POP3 protocol')
        print('2 - IMAP protocol')
        print('3 - SMTP protocol')
        print('4 - Exit')

        match input('>>> '):
            case '1':
                pop3()
                break
            case '2':
                imap()
                break
            case '3':
                smtp()
                break
            case '4':
                break
            case _:
                print('Incorrent input. Try again.')
