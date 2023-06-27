import port_scanner

print(">> Welcome to the port scanner! Which IP or address do you want to scan?")
target = input("IP/Address: ")
port_start = int(input("\n>> What is the starting port number? Starting port: "))
port_end = input("\n>> What is the ending port number (leave empty if only 1)? Ending port: ")
print("Testing ports - please wait...")
port_end = int(port_end) if port_end != "" else port_start

openports = port_scanner.get_open_ports(target, [port_start, port_end], True)

print("Open ports list:")
print(openports)