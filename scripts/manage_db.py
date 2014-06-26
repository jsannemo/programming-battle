#!/usr/bin/env python3
from sys import argv

from battle.models.manage import create_db, destroy_db, reset_db

def main():
    if argv[1] == 'create':
        create_db()
    if argv[1] == 'destroy':
        destroy_db()
    if argv[1] == 'reset':
        reset_db()


if __name__ == '__main__':
    main()
