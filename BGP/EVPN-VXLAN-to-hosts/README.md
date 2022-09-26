# BGP EVPN VXLAN to Linux hosts with FRR Route Leaking

![image](https://user-images.githubusercontent.com/2031627/192073414-2c224fd0-e457-47f5-9c7d-862518a4121a.png)

* Dual connected Linux hosts (FRR) with attached Linux hosts (representing VMs or containers)
* Redundant dual eBGP sessions with pair of ToRs (7220 IXR-D2s)
* Double iBGP EVPN session from loopback towards Route Reflectors (spines, 7220 IXR-D3)

## Prerequisites
* Netlab 'dev' branch: ```git clone https://github.com/ipspace/netlab.git --branch dev```

To deploy (assuming you have done ```source netlab/setup.sh```)
```
git clone https://github.com/jbemmel/netsim-examples.git --branch evpn-vxlan-to-hosts-v2
cd netsim-examples/BGP/EVPN-VXLAN-to-hosts
netlab up
```

## Underlay routing design
* eBGP over unnumbered ipv6 links with link-local addresses
* All FRR nodes have the same eBGP AS; this requires 'allowas-in' on FRR to install loopback route(s) to other frr nodes
* Every leaf has a unique eBGP AS
* All spines share the same eBGP AS towards leaves
  + They also use a unique local AS to peer eBGP amongst themselves, on a direct link
* Linux hosts static routes are inserted by Netlab

### FRR 'bgp bestpath as-path multipath-relax'

FRR requires a special flag 'bgp bestpath as-path multipath-relax' in order to treat eBGP routes with different AS path entries (via different leaves) as ECMP

# Routing policies

