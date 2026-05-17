# Subnet Calculator

## Creator info

### NAME:
*Teasdale, William*
### CLASS:
*Cyber Operations Academics*
### Purpose:
*Perform subnetting Calculations to include Multiple subnets and Variable
Length Subnet Masking (VLSM)*

# File info

## subs.py
Terminal based version of the subnet calculator
Take user ip and subnet by using flags

### Usage:
sub.py [-h] [-i IP] [-s SUBNET] [-c CIDR] [-m] [-v VLSM [VLSM ...]]  
  
options:  
  -h, --help            show this help message and exit  
  -i, --IP IP           The IP address to be worked. EX: x.x.x.x  
  -s, --Subnet SUBNET   The Subnet Mask. EX: x.x.x.x  
  -c, --CIDR CIDR       Subnet Mask in CIDR Format no /  
  -m, --Multiple        Print multiple subnets of the same size.  
  -v, --VLSM VLSM [VLSM ...]  
                        Create multiple subnets of varing length  


## gui_subs.py
moving subs.py into a graphical user interface with assitance from chatgpt

### Usage:
call the program in terminal and follow the input fields. Click run to get
results

### TODO:
Fix bugs in vlsm calculations


