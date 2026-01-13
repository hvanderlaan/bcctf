#!/usr/bin/env python3

from argparse import ArgumentParser
from multiprocessing import Pool
from os.path import exists
from sys import exit
from typing import Callable, Any

from colorama import Fore, Back, Style
from requests import get, exceptions
from tqdm import tqdm


def display_header():
    print(f'+--------------------------------------------+')
    print(f'| Dirbuster lite: Scrap a webserver          |')
    print(f'+--------------------------------------------+')
    print(f'| Version : v1.0.0                           |')
    print(f'| Date    : 13 / 12 / 2025                   |')
    print(f'| Author  : Harald van der Laan              |')
    print(f'| E-mail  : harald.vanderlaan@brightcubes.nl |')
    print(f'+--------------------------------------------+')
    print()


def get_commandline_arguments() -> None:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-d', '--directorylist', help='Directory list file', required=False)
    parser.add_argument('-t', '--target', help='Target to scan', required=True)

    return parser.parse_args()


def check_hostname(target: str) -> None:
    try:
        response: int = get(target)
    except exceptions.MissingSchema:
        exit(f'{Fore.RED}[-]:{Style.RESET_ALL} Missing schema (http:// or https://).')
    except exceptions.ConnectionError:
        exit(f'{Fore.RED}[-]:{Style.RESET_ALL} Could not connect to {target}.')
    except exceptions.InvalidURL:
        exit(f'{Fore.RED}[-]:{Style.RESET_ALL} Invalid taget, target must be an url.')


def create_fqdn_url(base_url: str, directories: list[str]) -> list[str | Any]:
    fqdn_url: list[str] = []
    for directory in directories:
        fqdn_url.append(f'{base_url}/{directory}')
    
    return fqdn_url


def check_fqdn_url(fqdn_url: str) -> str | None:
    if get(fqdn_url).status_code == 200:
        result:str = f'{Fore.GREEN}[+]:{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{fqdn_url}{Style.RESET_ALL} -> [200]'
        return result


def main(args: ArgumentParser) -> None:
    target: str = args.target
    check_hostname(target)
    if args.directorylist:
        if not exists(args.directorylist):
            exit(f'{Fore.RED}[-]:{Style.RESET_ALL} Could not find {args.directorylist}')
        else:
            wordlist: str = args.directorylist
    else:
        wordlist: str = 'dirlist.txt'
    
    directories: list[str | Any] = []
    with open(wordlist, 'r') as f:
        for directory in f.read().splitlines():
            directories.append(directory)
    
    fqdn_url: list[str | Any] = create_fqdn_url(target, directories)

    with Pool() as pool:
        results: list[str | None] = list(tqdm(pool.imap(check_fqdn_url, fqdn_url), total=len(fqdn_url)))
    
    for result in results:
        if result != None:
            print(result)


if __name__ == "__main__":
    ARGS = get_commandline_arguments()
    display_header()
    main(ARGS)