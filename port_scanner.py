import socket
from common_ports import ports_and_services
import ipaddress
import tldextract
from common_sites import ip_and_sites

# 2 functions to verify the ip and urls entry paramters
def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def is_valid_url(url):
    domain = tldextract.extract(url).registered_domain
    return bool(domain)



# Below is the implementation with socket - unfortunately it is really slow so it has a timeout

def port_status_socket(target, port, timeout = False):
    """
    Returns the status of the port for the given target.
    Returns true for open or false for closed or non-reachable
    """
    s = socket.socket()

    # Code built on try-except-else-block to handle exceptions and execute code based on whether an exception occurs or not 
    try:
        if timeout: s.settimeout(timeout) # Optional argument to define timeout. Increases function but reduces accuracy
        s.connect((target, port))
        s.close()
        return True
    except:
        s.close()
        return False
    


def get_open_ports(target, port_range, verbose = False):
    introText = ""
    ip = ""
    hostname = ""

    if target[0].isdigit(): # If the first char is a digit then it can only be an ip
        if not is_valid_ip(target):
            # No valid ip address
            return "Error: Invalid IP address"
        # We try to get the URL either from our own list or from a DNS lookup. If both fail, than we stick to only IP
        try:
            try: 
                hostname = ip_and_sites[target]
            except:
                hostname = socket.gethostbyaddr(ip)[0]
        except:
            # open_ports_text needs to be adjusted to only IP
            introText = f"Open ports for {target}\n"
        ip = target
    else: # Otherwise we assume it is a hostname
        if not is_valid_url(target):
            # Not an ip but also not a valid url
            return "Error: Invalid hostname"
        ip = socket.gethostbyname(target)
        hostname = target

    open_ports = []
    

    for port in range(port_range[0], port_range[1] + 1, 1):
        if port_status_socket(ip, port,0.4):
            open_ports.append(port)

    if (not verbose): 
        return(open_ports)
    else:
        open_ports_text = "\n".join(f"{port}{' ' * (8 if len(str(port)) == 1 else 7 if len(str(port)) == 2 else 6)}{ports_and_services[port]}" for port in open_ports)
        if len(introText) < 5:
            introText = f"Open ports for {hostname} ({ip})\n"
        printText = f"{introText}PORT     SERVICE\n{open_ports_text}"
        return printText


print(get_open_ports("104.26.10.78",[440, 450], True))