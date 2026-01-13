from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from colorama import Fore, Style
from multiprocessing import Pool, cpu_count
from os import cpu_count as os_cpu_count
from os import system, name
from signal import signal, SIGINT, SIG_IGN
from socket import AddressFamily, AF_INET, gaierror, getaddrinfo, getservbyport, socket, SOCK_STREAM
from sys import exit, stderr
from tqdm import tqdm
from typing import Any

'''
portscanner.py: A multiprocessing TCP scanner

Author  : Harald van der Laan <harald.vanderlaan@brightcubes.nl>
Version : V0.1.1
Date    : 20/12/2025

Usage   : python3 portscanner.py [options] <target>
'''

def display_header() -> None:
    '''
    display_header: Function to display the header
    '''
    name: str = 'portscanner.py'
    version: str = 'v0.1.1'
    author: str = 'By: Harald van der Laan <harald.vanderlaan@brightcubes.nl>'

    print('+' + '-' * 70 + '+')
    print('| ' + f'{name: ^68} ' + '|')
    print('| ' + f'{version: ^68} ' + '|')
    print('| ' + f'{author: ^68} ' + '|')
    print('+' + '-' * 70 + '+')
    print()


def get_arguments() -> ArgumentParser:
    '''
    get_arguments: Function to get commandline arguments
    
    :return: arguments
    :rtype: ArgumentParser
    '''
    parser: ArgumentParser = ArgumentParser(
        description="Parallel TCP portscanner",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "host", help="Target (DNS name / Ipaddress)"
    )
    parser.add_argument(
        "--banner", action="store_true",
        help="Display service banners"
    )
    parser.add_argument(
        "-p", "--ports", default="1-1024",
        help="Ports to scan 1-1024,3000,8080"
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=0.5,
        help="TCP Socket timeout"
    )
    parser.add_argument(
        "-w", "--workers", type=int,
        default=min(64, (os_cpu_count() or cpu_count() or 1) * 4),
        help="Amount of parallel processes"
    )

    return parser.parse_args()


def get_servicename(port: int) -> str:
    '''
    get_servicename: Function to get servicename by a port
    
    :param port: portnumber
    :type port: int
    :return: servicename
    :rtype: str
    '''
    try:
        return getservbyport(port)
    except gaierror:
        return "unkown"
    except OSError:
        return "unknown"


def parse_ports(spec: str) -> list[int]:
    '''
    parse_ports: Function to create a list of ports to scan
    
    :param spec: port range provided by commandline argument
    :type spec: str
    :return: list of ports to scan
    :rtype: list[int]
    '''
    ports: set = set()
    
    for part in (spec or "").split(","):
        part = part.strip()
        
        if not part:
            continue
        
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            
            if a > b:
                a, b = b, a
            
            for p in range(max(1, a), min(65535, b) + 1):
                ports.add(p)
        else:
            p = int(part)
            if 1 <= p <= 65535:
                ports.add(p)
    
    return sorted(ports)


def resolve_target(host: str) -> tuple[int, str]:
    '''
    resolve_target: Function to get AdddresFamily and ipaddress
    
    :param host: Hostname/ipaddress
    :type host: str
    :return: AddressFamily, Ipaddress
    :rtype: tuple[int, str]
    '''
    infos:  AddressFamily = getaddrinfo(host, None, type=SOCK_STREAM)
    if not infos:
        raise RuntimeError(f'[!] No addresses found for {host}.')
    ipv4: list[Any] = [i for i in infos if i[0] == AF_INET]
    chosen: list[Any] = ipv4[0] if ipv4 else infos[0]
    family: int = chosen[0]
    ip: str = chosen[4][0]
    
    return family, ip


def scan_one(task: tuple[int, str, int, float, bool]) -> tuple[int, bool, bytes | None]:
    '''
    scan_one: Scanning a host / port. Pickable worker function taht can be used
    with multiprocessing.
    
    :param task: (family, ip, port, timeout, banner)
    :type task: tuple[int, str, int, float, bool]
    :return: (port, is_open, banner_bytes|None)
    :rtype: tuple[int, bool, bytes | None]
    '''
    family, ip, port, timeout, banner = task

    with socket(family, SOCK_STREAM) as sckt:
        try:
            sckt.settimeout(timeout)
            addr = (ip, port) if family == AF_INET else (ip, port, 0, 0)
            sckt.connect(addr)
            data: bytes | None = None
        
            if banner:
                try:
                    sckt.sendall(b"\r\n")
                    data = sckt.recv(1024)
                except Exception:
                    data = None
            
            return (port, True, data)
        except Exception:
            return (port, False, None)


def _init_worker():
    '''
    _init_worker: Worker funcrion to handle CTRL+C 
    '''
    try:
        signal(SIGINT, SIG_IGN)
    except Exception:
        pass


def main() -> None:
    args: ArgumentParser = get_arguments()
    family: AddressFamily
    ip: str

    try:
        family, ip = resolve_target(args.host)
    except Exception as e:
        print(f'[!] Could not resolve host: {e}', file=stderr)
        exit(2)

    ports: list[int] = parse_ports(args.ports)
    if not ports:
        print(f'[!] No vaild ports spacified.', file=stderr)
        exit(2)
    
    system('cls' if name == 'nt' else 'clear')
    display_header()
    print(f"Target : {args.host} ({ip})")
    print(f"Range: {args.ports}  | Workers: {args.workers}  | Timeout: {args.timeout}s  | Banner: {args.banner}")
    print("-" * 72)

    open_ports: list[tuple[int, bytes | None]] = []
    tasks: tuple[int, bool, bytes | None] = [(family, ip, p, args.timeout, args.banner) for p in ports]

    try:
        with Pool(processes=args.workers, initializer=_init_worker) as pool:
            with tqdm(total=len(tasks), desc="Scanning", unit="ports") as pbar:
                for port, is_open, banner_data in pool.imap_unordered(scan_one, tasks, chunksize=8):
                    pbar.update(1)
                    if is_open:
                        open_ports.append((port, banner_data))
    except KeyboardInterrupt:
        print(f'\n[!] User pressed CTRL+C.', file=stderr)
    except Exception as e:
        print(f'\n[!] Failure while scanning: {e}', file=stderr)

    if open_ports:
        open_ports.sort(key=lambda x: x[0])
        print(f'\nOpen port(s) found: ({len(open_ports)})')
        for port, banner_data in open_ports:
            svc: str = get_servicename(port)
            line: str = f"[{Fore.LIGHTGREEN_EX}+{Style.RESET_ALL}] {Fore.RED}{port:>5}/tcp{Style.RESET_ALL}  open   {Fore.LIGHTBLUE_EX}{svc}{Style.RESET_ALL}"
            if banner_data:
                try:
                    snippet = banner_data.decode(errors="ignore").strip().replace("\r", " ").replace("\n", " ")
                    if snippet:
                        line += f"  |  banner: {snippet[:100]}"
                except Exception:
                    pass
            print(line)
    else:
        print(f'\nThere are no open ports on {args.host}')

    print("-" * 72)


if __name__ == '__main__':
    main()