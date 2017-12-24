# nft-blacklist
Blacklist country specific IP blocks using nftables

# Requirements
To use this script, you will need to create a 'set' in your nftables configuration with the `type ipv4_addr` or `type ipv6_addr` and `flags interval` set properties. This set can belong to any table in your nftables configuration and is responsible for holding the blacklisted IP addresses. The syntax to create a set is :

`nft add set [table] [set-name] {set properties}`

Please refer the nftables wiki for more info on set operations: https://wiki.nftables.org/wiki-nftables/index.php/Sets

# Configuration

Edit the variables at the top of nft-blacklist.py to your liking
The ip\_file / ip6\_file variables should point to the files you want to store the blacklists in. The country\_codes tuple holds the 2 letter codes for the countries you wish to restrict access to.
Refer to http://www.ipdeny.com/ipblocks/data/countries/ or ISO 3166 ALPHA2 for the list of countries.

# Usage

After making the necessary configurations, run the script. The script will update the given files with the blacklisted IP blocks, which can then be used for inclusion in an nftables configuration file.

# Example

A sample dual-stack nftables configuration file is shown below for assistance:

```
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
        set ip_black_country {
                type ipv4_addr
                flags interval
                include "/etc/nftables/inet_filter_ip_black_country.inc"
        }

        set ip6_black_country {
                type ipv6_addr
                flags interval
                include "/etc/nftables/inet_filter_ip6_black_country.inc"
        }

        chain input {
                type filter hook input priority 0; policy drop;

                ct state invalid drop

                # allow established connections
                ct state established,related accept

                # allow all local connections
                iifname lo accept

                # drop all new packets that are not of type SYN
                tcp flags != syn drop

                # drop all packets from blacklist ips
                ip saddr @ip_black_country drop
                ip6 saddr @ip6_black_country drop

                # accept connections to some ports
                tcp dport {http, https, ssh} accept

                # accept valid icmp packets
                ip protocol icmp icmp type { echo-request, destination-unreachable, router-advertisement, time-exceeded, parameter-problem } accept
                ip6 nexthdr icmpv6 icmpv6 type { echo-request, destination-unreachable, packet-too-big, time-exceeded, parameter-problem, nd-router-advert, nd-neighbor-solicit, nd-neighbor-advert } accept

                # allow unix traceroute
                udp dport { 33434-33534 } reject
        }
}
```
