#!/usr/bin/python3

"""FILE: subs.py"""
#NAME: Teasdale, William
#CLASS: 17C Academics
#Purpose: Perform subnetting verification durring practice hours. NOT TO BE USED ON TESTS
#BUGS: N/A


import sys
import ipaddress as ip
import math
import argparse


#NAME:      bin_con
#Purpose:   Change the sent IPv4 or Subnet Mask to Binary, print the print binary to
#           console, then return.
#Inputs:    (ip object) ip_in = the ip address to be converted imput in DDN
#Outputs:   N/A
def bin_con(ip_in):
    """Change the sent IPv4 or Subnet Mask to Binary and print"""
    ip_in = f"{int(ip_in):#b}"
    #ip_in = '{:#b}'.format(int(ip_in))
    tmp = ''
    for ind, val in enumerate(ip_in):
        if ind in (10, 18, 26):
            tmp += '.'
            tmp += val
        elif ind < 2:
            pass
        else:
            tmp += val

    print(tmp)


#NAME:      nflb
#Purpose:   Calculate and print the Net ID, First Host, Last Host, and Broadcast ID
#Inputs:    (ip object) ip_in = the host IP provided by the user
#           (ip object) subnet_in = the subnet mask provided by the user
#Outputs:   (int) nid = the Network ID of the Subnet
def nflb(ip_in, subnet_in):
    """Calculate and print the Net ID, First Host, Last Host, and Broadcast ID"""
    nid = int(ip_in) & int(subnet_in)
    bid = (nid | (~int(subnet_in))) & 0xffffffff
    print('NID = ', str(ip.IPv4Address(nid)))
    print('FAI = ', str(ip.IPv4Address(nid+1)))
    print('LAI = ', str(ip.IPv4Address(bid-1)))
    print('BID = ', str(ip.IPv4Address(bid)), '\n')
    return nid


#NAME:      hosts
#PURPOSE:   print the total hosts and ips in a subnet
#INPUTS:    (ip object) ip_in = the host IP provided by the user
#           (ip object) subnet_in = the subnet mask provided by the user
#OUTPUTS:   (int) tot = The total number of IPs available within a subnet
def hosts(subnet_in):
    """Print the total hosts and ips in a subnet"""
    sub = f"{int(subnet_in):#b}"
    #sub = '{:#b}'.format(int(subnet_in))
    tot = (2 ** (sub.count('0')-1))
    num_hosts = tot - 2
    print('Total IPs = ', tot)
    print('Total Hosts = ', num_hosts, '\n')
    return tot

#NAME:      num_subs
#PURPOSE:   prints the step size and the total number of same size subnets within an octet
#INPUTS:    (int) step = the total number of IPs from a given subnet mask
#OUTPUTS:   (list) holding = holding[0] = the step size of the network
#                            holding[1] = the number of similar sized subnets
#                            holding[2] = the Octet the user is currently
#                                           working in
def num_subs(step):
    """Prints the step size and the total number of same size subnets in an octet"""
    octet = 1
    while step > 128:
        step //= 256
        octet += 1

    print('Step Size = ',step)

    if step == 1:
        subs = 1
    else:
        subs = 256 // step

    print('Number of Same Size Subnets: ', subs, '\n')

    holding = [step, subs, octet]
    return holding

#NAME:      same_nflb
#PURPOSE:   Print out a list of NFLBs for similar sized subnets to the provided
#           subnet and IP
#INPUTS:    (ip object) nid = the acting network ID
#           (ip object) sub_in = the current working subnet
#           (list) holding = the output of num_subs with (hold[0] - 1) to account
#                           for off by one error
#           (int) total = the total number of IPs in a given subnet
#OUTPUTS:   N/A
def same_nflb(nid, sub_in, holding, total):
    """Print a list of NFLB for similar sized subnets."""
    inc = 0
    af8 = 8 - int(math.log2(holding[0]))

    next_nid = int(nid) + total

    lowest = int(nid) & (int(sub_in) << af8)

    next_oct = int(lowest) + 256**holding[2]

    while inc < holding[1] and next_nid < next_oct:
        bid = (next_nid | (~int(sub_in))) & 0xffffffff
        print(f"Subnet{inc+2}")
        #print('Subnet #{}'.format(inc+2))
        print('NID = ', str(ip.IPv4Address(next_nid)))
        print('FAI = ', str(ip.IPv4Address(next_nid+1)))
        print('LAI = ', str(ip.IPv4Address(bid-1)))
        print('BID = ', str(ip.IPv4Address(bid)), '\n')

        next_nid += total
        inc += 1

#NAME:      vlsm
#PURPOSE:   Calculate Multiple subnets of varying length
#INPUTS:    (list) arg = the input values from the user when using the -v flag
#           (ip object) start_nid : the starting network ID for the VLSM
#           (ip object) sub_in: the initial subnet mask the user input
#OUTPUTS: N/A
def vlsm(net_size, start_nid, sub_in):
    """Calculate Multiple subnets of varying length."""
    octet = step = 1
    fcidr = 32
    net_size = sorted(net_size, reverse = True)
    for min_host in net_size:
        later = min_host
  #     print(min_host)
        while min_host > 256:
            min_host //= 256
            octet += 1
    #    print(min_host)
        exp = round(math.log2(min_host))
        while step < exp:
            step += 1

    #    print(step, exp)
        step = 2 ** step
        if min_host == step:
            step *= 2
      #      print(step)

        fcidr -= round(math.log2(step))
        if octet > 1:
            for inc in range(octet-1):
                inc = (inc + 1) - 1 #I am using this to get rid of the warning
                fcidr -= 8
       # print(min_host, step, fcidr)

        cidr = (-1<<(32-fcidr)) & 0xffffffff

        sub = f"{int(cidr):#b}"
        #sub = '{:#b}'.format(int(cidr))
        tot = (2 ** (sub.count('0')-1))
       # print(tot, later)
        if tot < later:
            fcidr -= 1
            cidr = (-1<<(32-fcidr)) & 0xffffffff

        sub_in = ip.IPv4Address(cidr)
        print("Found CIDR value = ", fcidr)
        print("A network to hold ", later)
        start_nid = nflb(start_nid, sub_in)
        total = hosts(sub_in)
        start_nid = int(start_nid) + total
        fcidr = 32
        octet = step = 1


if __name__ == '__main__':
#argparse flag intake
    parser = argparse.ArgumentParser(
                        prog = 'sub.py',
                        description = 'Takes in an IP and Subnet Mask to output Subnet information',
                        epilog = 'Well Wishes')

    parser.add_argument("-i", "--IP", required=True, help='The IP address to be worked. EX: -i x.x.x.x')

    # -s and -c are mutually exclusive but one is required
    mask_group = parser.add_mutually_exclusive_group(required=True)
    mask_group.add_argument("-s", "--Subnet", help="The Subnet Mask. EX: -s x.x.x.x")
    mask_group.add_argument("-c", "--CIDR", help="Subnet Mask in CIDR Format no /")

    parser.add_argument("-m", "--Multiple", action='store_true', help="Print multiple subnets of the same size.")
    parser.add_argument("-v", "--VLSM", nargs='+', help="Create multiple subnets of varing length Ex: -v 152 126 32 5")


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
#end argparse


    host = ip.IPv4Address(args.IP)
    if args.Subnet:
        subnet = ip.IPv4Address(args.Subnet)
    elif args.CIDR:
        CIDR = int(args.CIDR)
        CIDR = (-1<<(32-CIDR)) & 0xffffffff
        subnet = ip.IPv4Address(CIDR)
    else:
        CIDR = (-1<<(32-24)) & 0xffffffff
        subnet = ip.IPv4Address(CIDR)

    print(str(ip.IPv4Address(host)), ' = ', end='')
    bin_con(host)

    print(str(ip.IPv4Address(subnet)), ' = ', end='')
    bin_con(subnet)
    print()

    NET_ID = nflb(host, subnet)
    TOTAL = hosts(subnet)


    if args.Multiple:
        hold = num_subs(TOTAL)
        hold[1] -= 1
        same_nflb(NET_ID, subnet,hold, TOTAL)

    if args.VLSM:
        arg = args.VLSM
        for i in range(len(arg)):
            arg[i] = int(arg[i])
        vlsm(arg, NET_ID, subnet)

    sys.exit(0)
