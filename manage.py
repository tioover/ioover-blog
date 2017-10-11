#!/usr/bin/env python3
'''
Simple Jekyll site manage script.
'''
import os
import sys
import time
import datetime
import signal
import argparse
import subprocess
from os import system as run
from subprocess import Popen
import http.server
import socketserver

TIMEZONE = '+0800'

POST_TEMPLATE =\
'''---
layout: post
title: {}
date: {}
category:
summary:
typora-root-url: ../
typora-copy-images-to: ../media
---'''

def open_with_app(filepath):
    '''https://stackoverflow.com/questions/434597/open-document-with-default-application-in-python'''
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))

def create_post(title: str):
    filename = title.replace(' ', '_').lower()
    now = datetime.datetime.now()
    source = POST_TEMPLATE.format(filename, now.strftime('%Y-%m-%d %H:%M:%S '+TIMEZONE))
    filename = now.strftime('%Y-%m-%d-') + filename + '.md'
    path = os.path.join('_posts', filename)
    if not os.path.exists(path):
        with open(path, mode='w', encoding='utf-8') as new:
            new.write(source)
    else:
        print('File {} already exists!'.format(filename))
    open_with_app(path)


def build():
    run('JEKYLL_ENV=production bundle exec jekyll build')
    run('npm run webpack')
    run('sass ./_sass/main.sass ./assets/style.css')
    run('cp -r ./node_modules/han-css/font/ ./assets/fonts/')

def serve():
    try:
        Popen('npm run webpack -- -w', shell=True)
        Popen('sass --watch ./_sass/main.sass:./assets/style.css', shell=True)
        run('cp -r ./node_modules/han-css/font/ ./assets/fonts/')
        Popen("bundle exec jekyll serve", shell=True).wait()
    finally:
        os.killpg(os.getpid(), signal.SIGTERM)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    build_parser = subparsers.add_parser('build', help='Build site')
    deploy_parser = subparsers.add_parser('serve', help='Develop server')
    post_parser = subparsers.add_parser('post', help='Create new post.')
    post_parser.add_argument('title')

    args = parser.parse_args()
    if args.command == 'post':
        create_post(args.title)
    elif args.command == 'build':
        build()
    elif args.command == 'serve':
        serve()

if __name__ == '__main__':
    main()
