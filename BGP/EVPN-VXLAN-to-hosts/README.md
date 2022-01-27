# BGP EVPN VXLAN to Linux hosts with L3 anycast gateways on leaves

![image](https://user-images.githubusercontent.com/2031627/151012844-ac984a74-1803-433d-82f9-1157d87d26a8.png)

* Dual connected Linux hosts (FRR)
* Redundant dual eBGP sessions with pair of ToRs (7220 IXR-D2s)
* Double iBGP EVPN session from loopback towards Route Reflectors (spines, SR OS SR-1)

## Prerequisites
* Netsim-Tools [dev branch](https://github.com/ipspace/netsim-tools/tree/dev)
* [PR to add EVPN module](https://github.com/ipspace/netsim-tools/pull/188)
* [PR with some BGP enhancements](https://github.com/ipspace/netsim-tools/pull/187)

To deploy (assuming you have ```source netsim-tools/setup.sh```)
```
netlab up
```

## Underlay routing design
* Linux hosts receive a default route from each leaf, and advertise their ipv4 loopback (eBGP) over a pair of /30 links to the leaves
* All Linux hosts have the same eBGP AS; this is possible because of the default routes
* Every leaf has a unique eBGP AS
* All spines share the same eBGP AS towards leaves
  + TODO they may need a unique AS to peer amongst themselves, in case of a direct link
* Because the Linux hosts already have 0.0.0.0/0 via management, the fabric announces 0.0.0.0/1 and 128.0.0.0/1 (longer prefix match)

### FRR 'bgp bestpath as-path multipath-relax'

FRR requires a special flag 'bgp bestpath as-path multipath-relax' in order to treat eBGP routes with different AS path entries (via different leaves) as ECMP

# Basic L2 VXLAN connectivity
Once deployed, basic L2 VXLAN connectivity between Linux hosts works:
```
jeroen@jvm:~/srlinux/netsim-examples/BGP/EVPN-VXLAN-to-hosts$ docker exec -it clab-EVPN-VXLAN-to-hosts-h1 ping 10.100.0.109 -c2
PING 10.100.0.109 (10.100.0.109): 56 data bytes
64 bytes from 10.100.0.109: seq=0 ttl=64 time=2.219 ms
64 bytes from 10.100.0.109: seq=1 ttl=64 time=1.528 ms

--- 10.100.0.109 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 1.528/1.873/2.219 ms
```

The resulting EVPN MAC tables can be viewed:
```
--{ + running }--[  ]--                                                                                                                                                                                            
A:leaf1a# show network-instance overlay-router-l2-100 bridge-table mac-table all                                                                                                                                   
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Mac-table of network instance overlay-router-l2-100
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
+--------------------+-------------------------------------------------------------+------------+-------------------+---------+--------+-------------------------
|      Address       |                         Destination                         | Dest Index |       Type        | Active  | Aging  |     Last Update      
+====================+=============================================================+============+===================+=========+========+=========================
| 00:00:5E:00:01:01  | irb                                                         | 0          | irb-interface-    | true    | N/A    | 2022-01-27T04:16:56.000Z                                    |
|                    |                                                             |            | anycast           |         |        |                                                             |
| 1A:B0:03:FF:00:41  | irb                                                         | 0          | irb-interface     | true    | N/A    | 2022-01-27T04:16:56.000Z                                    |
| 1A:B0:04:FF:00:41  | vxlan-interface:vxlan0.100 vtep:10.0.0.2 vni:100            | 3304803020 | evpn-static       | true    | N/A    | 2022-01-27T04:17:02.000Z                                    |
|                    |                                                             | 5          |                   |         |        |                                                             |
| 1A:B0:05:FF:00:41  | vxlan-interface:vxlan0.100 vtep:10.0.0.3 vni:100            | 3304803021 | evpn-static       | true    | N/A    | 2022-01-27T04:17:02.000Z                                    |
|                    |                                                             | 1          |                   |         |        |                                                             |
| 1A:B0:06:FF:00:41  | vxlan-interface:vxlan0.100 vtep:10.0.0.4 vni:100            | 3304803020 | evpn-static       | true    | N/A    | 2022-01-27T04:17:02.000Z                                    |
|                    |                                                             | 7          |                   |         |        |                                                             |
| 4A:86:FB:E1:61:43  | vxlan-interface:vxlan0.100 vtep:10.0.0.9 vni:100            | 3304803021 | evpn              | true    | N/A    | 2022-01-27T04:16:58.000Z                                    |
|                    |                                                             | 3          |                   |         |        |                                                             |
| 4E:D3:17:F9:21:CA  | vxlan-interface:vxlan0.100 vtep:10.0.0.8 vni:100            | 3304803021 | evpn              | true    | N/A    | 2022-01-27T04:16:58.000Z                                    |
|                    |                                                             | 7          |                   |         |        |                                                             |
+--------------------+-------------------------------------------------------------+------------+-------------------+---------+--------+-------------------------
Total Irb Macs            :    1 Total    1 Active
Total Static Macs         :    0 Total    0 Active
Total Duplicate Macs      :    0 Total    0 Active
Total Learnt Macs         :    0 Total    0 Active
Total Evpn Macs           :    2 Total    2 Active
Total Evpn static Macs    :    3 Total    3 Active
Total Irb anycast Macs    :    1 Total    1 Active
Total Macs                :    7 Total    7 Active
```

Linux hosts can also reach the anycast gateway, and each of the non-anycast interface IPs:
```
jeroen@jvm:~/srlinux/netsim-examples/BGP/EVPN-VXLAN-to-hosts$ docker exec -it clab-EVPN-VXLAN-to-hosts-h1 ping 10.100.0.1 -c2
PING 10.100.0.1 (10.100.0.1): 56 data bytes
64 bytes from 10.100.0.1: seq=0 ttl=64 time=5.695 ms
64 bytes from 10.100.0.1: seq=1 ttl=64 time=6.112 ms

--- 10.100.0.1 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 5.695/5.903/6.112 ms
jeroen@jvm:~/srlinux/netsim-examples/BGP/EVPN-VXLAN-to-hosts$ docker exec -it clab-EVPN-VXLAN-to-hosts-h1 ping 10.100.0.2 -c2
PING 10.100.0.2 (10.100.0.2): 56 data bytes
64 bytes from 10.100.0.2: seq=0 ttl=64 time=7.286 ms
64 bytes from 10.100.0.2: seq=1 ttl=64 time=5.850 ms

--- 10.100.0.2 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 5.850/6.568/7.286 ms
jeroen@jvm:~/srlinux/netsim-examples/BGP/EVPN-VXLAN-to-hosts$ docker exec -it clab-EVPN-VXLAN-to-hosts-h1 ping 10.100.0.3 -c2
PING 10.100.0.3 (10.100.0.3): 56 data bytes
64 bytes from 10.100.0.3: seq=0 ttl=64 time=6.474 ms
64 bytes from 10.100.0.3: seq=1 ttl=64 time=5.260 ms

--- 10.100.0.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 5.260/5.867/6.474 ms
```

## L3 VNIs
The current configuration does not yet include L3 VNIs (routed VXLAN interfaces). Those would require non-default ip-vrf network instance(s)

## Anycast gateway in underlay (A/S links)
It would be possible to have an anycast gateway (IRB interface) in the underlay, towards each server:
```
Current:
0.0.0.0/0 via next hops 10.1.0.46, 10.1.0.50 (ECMP)

With anycast gw:
0.0.0.0/0 via next hop 10.1.0.1
```
Every server would pick one of the two leaf links (unless a bonded LAG links were used)

## Identical IP configuration towards each server
Instead of unique link IP pairs, both switch pairs could reuse the same sequence of IPs

# Evaluating design alternatives
Given this reference topology, we can evaluate various design options:

## Unique AS numbers for spines
Some reference designs use a single AS for all spines, to get automatic route filtering based on AS path. To see what changes when we would use a unique AS for each spine:
```
netlab up -v -s nodes.spine2.bgp.underlay_as=65011
```
This changes the BGP peering session between the spines from iBGP(EVPN) to eBGP(IPv4). Some changes would be required to make this a "fair" comparison, but the point remains
that various design options can be explored through relatively minor tweaks.



# References
* [Scaleway (2016)](https://www.enog.org/wp-content/uploads/presentations/enog-16/18-Scaleway-P14-fabric-ENOG16.pdf)
* [SR Linux EVPN-VXLAN guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17913AAAA01_V1_SR%20Linux%20R21.11%20EVPN-VXLAN%20User%20Guide.pdf)
* [SR Linux Advanced Solutions guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17902AAAA01_V1_SR%20Linux%20R21.11%20%20Advanced%20Solutions%20Guide.pdf)
