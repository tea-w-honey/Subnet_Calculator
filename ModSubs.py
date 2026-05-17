#/usr/bin/python3

import ipaddress as ip
import math



def bin_con(ip_in):
    """Convert an IPv4 address or subnet mask to binary and return as a string."""
    ip_bin = f"{int(ip_in):#b}"
    binary = ""

    for i, val in enumerate(ip_bin):
        if i in (10, 18, 26):
            binary += "."
        if i >= 2:
            binary += val

    return binary



def nflb(ip_in, subnet_in):
    """Calculate and return Net ID, First Host, Last Host, and Broadcast ID as a string."""

    nid = int(ip_in) & int(subnet_in)
    bid = (nid | (~int(subnet_in))) & 0xFFFFFFFF

    return f"""
    NID = {ip.IPv4Address(nid)}
    First Host = {ip.IPv4Address(nid+1)}
    Last Host = {ip.IPv4Address(bid-1)}
    BID = {ip.IPv4Address(bid)}
    """



def hosts(subnet_in):
    """Calculate total hosts in subnet and return as a string."""

    subnet_bin = f"{int(subnet_in):#b}"
    total_ips = 2 ** (subnet_bin.count('0') - 1)
    num_hosts = total_ips - 2

    return f"Total IPs = {total_ips}\nTotal Hosts = {num_hosts}"

def num_subs(step):
    """Calculate step size and total subnets, return as a list."""

    octet = 1
    while step > 128:
        step //= 256
        octet += 1

    subs = 256 // step if step > 1 else 1

    return [step, subs, octet]

def same_nflb(nid, sub_in, holding, total):
    """Generate multiple subnets of the same size and return as a string."""

    inc = 0
    next_nid = int(nid) + total
    results = []

    while inc < holding[1] and next_nid < (int(nid) & (int(sub_in) << (8 - int(math.log2(holding[0]))))) + 256 ** holding[2]:
        bid = (next_nid | (~int(sub_in))) & 0xFFFFFFFF
        results.append(f"Subnet {inc+2}:\nNID = {ip.IPv4Address(next_nid)}\nFirst Host = {ip.IPv4Address(next_nid+1)}\nLast Host = {ip.IPv4Address(bid-1)}\nBID = {ip.IPv4Address(bid)}\n")
        next_nid += total
        inc += 1

    return "\n".join(results)

def vlsm(net_sizes, start_nid, sub_in):
    """Perform VLSM calculation and return results as a string."""

    results = []
    fcidr = 32
    net_sizes = sorted(net_sizes, reverse=True)

    for min_host in net_sizes:
        step = 1
        exp = round(math.log2(min_host))

        while step < exp:
            step += 1

        step = 2 ** step
        if min_host == step:
            step *= 2

        fcidr -= round(math.log2(step))
        if fcidr < 0:
            fcidr = 0  # Prevents negative CIDR

        cidr = (-1 << (32 - fcidr)) & 0xFFFFFFFF
        sub_in = ip.IPv4Address(cidr)
        results.append(f"Subnet to hold {min_host}:\nCIDR: {fcidr}\n{sub_in}")
        start_nid = int(start_nid) + (2 ** (sub_in.exploded.count('0') - 1))
        fcidr = 32

    return "\n".join(results)



def run_subnet_calculations(ip_addr, subnet_mask, multiple=False, vlsm_sizes=None):
    """Main function to process subnet calculations and return results."""

    host = ip.IPv4Address(ip_addr)
    subnet = ip.IPv4Address(subnet_mask)
    result = []
    result.append(f"{host} = {bin_con(host)}")
    result.append(f"{subnet} = {bin_con(subnet)}\n")

    NET_ID = nflb(host, subnet)
    TOTAL = hosts(subnet)
    result.append(NET_ID)
    result.append(TOTAL)



    if multiple:
        hold = num_subs(int(TOTAL.split("\n")[0].split(" = ")[1]))
        hold[1] -= 1
        result.append(same_nflb(NET_ID.split("\n")[0].split(" = ")[1], subnet, hold, int(TOTAL.split("\n")[0].split(" = ")[1])))

    if vlsm_sizes:
        print(vlsm_sizes)
        print(vlsm_sizes.split())
        sizes = [int(size) for size in vlsm_sizes.split()]
        print(NET_ID.split("\n")[0].split(" = ")[1])
        result.append(vlsm(sizes, NET_ID.split("\n")[0].split(" = ")[1], subnet))

    return "\n".join(result)


