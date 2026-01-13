from argparse import ArgumentParser
from multiprocessing import Pool
from time import time
from typing import Callable

from colorama import Fore, Back, Style
from requests import get, exceptions
from tqdm import tqdm

def check_host(url: str) -> None:
    """
    Funtion check_host to check if a target is live.

    With this function you can check is a target host is live, the ulr
    is valide or is missing the schema http(s)://. This function prints the
    error with a sys.exit() statement.
    
    :param url: url or fqdn to check

    :example:
    >>> url = 'http://example.com'
    >>> check_host(url)
    """
    try:
        resp: object = get(url)
    except exceptions.MissingSchema:
        exit(f'{Fore.RED}[-]{Style.RESET_ALL}: Please use: http(s)://{url}.')
    except exceptions.ConnectionError:
        exit(f'{Fore.RED}[-]{Style.RESET_ALL}: Could not connect to host: {url}.')
    except exceptions.InvalidURL:
        exit(f'{Fore.RED}[-]{Style.RESET_ALL}: Please enter a valid url. url {url} is not valid.')


def bust_directory(url: str) -> None:
    """
    Function nust_directory to scrap a target / fqdn

    bust_directory will scran a target / fqdn for subdirectory. If a directory is found the
    function will report this with a print statement
    
    :param url: url on target
    :type url: str

    :example:
    >>> url = 'http://example.com'
    >>> directories = ['logs', 'uploads', 'admin', 'panel']
    >>> for directory in directpries:
    >>>     bust_directory(f'{url}/{directory}')
    [+]: http://example.com/admin -> [200]
    """
    if get(url).status_code == 200:
        return f'{Fore.GREEN}[+]: {Fore.LIGHTBLUE_EX}{url}{Style.RESET_ALL} -> [200]'
    

def create_url(base: str, directories: list[str]) -> list[str]:
    """
    Helper function to create urls

    Create_url is a helper function to create fqdns of the url and directories. And returns
    the fqdns in a list.
    
    :param base: base url
    :type base: str
    :param directories: directories
    :type directories: list[str]
    :return: list of urls to scan
    :rtype: list[str]

    :example:
    >>> directories: list['str'] = ['admin', 'uploads', 'pannel', 'cgi-bin']
    >>> url: str = 'http://example.com'
    >>> fqdn: list['str'] = create_url(url, directories)
    """
    url : list[str] = []
    for directory in directories:
        url.append(f'{base}/{directory}')
    
    return url


def get_arguments() -> ArgumentParser:
    """
    Getting commandline arguments
    
    :return: arguments
    :rtype: ArgumentParser
    """
    parser: ArgumentParser= ArgumentParser()
    parser.add_argument('-t', '--target', help="Target to scan.", required=True)

    return parser.parse_args()


def main(args) -> None:
    """
    Main Python function
    
    :param args: Commandline arguments
    """
    target: str = args.target
    wordlist: str = 'dirlist.txt'
    directories: list[str] = []
    urls: list[str] = []

    check_host(target)

    with open(wordlist, 'r') as fdh:
        for directory in fdh.read().splitlines():
            directories.append(directory)
    
    urls = create_url(target, directories)

    print('*********************************************')
    print('* dirbuster.py                              *')
    print('*********************************************')
    print('* Version: v1.0.1                           *')
    print('* Author : Harald van der Laan              *')
    print('* E-mail : harald.vanderlaan@brightcubes.nl *')
    print('*********************************************')
    print()
    with Pool() as pool:
        results: list[str] = list(tqdm(pool.imap(bust_directory, urls), total=4614))
        
    for result in results:
        if result != None:
            print(result)


if __name__ == "__main__":
    ARGS = get_arguments()
    main(ARGS)