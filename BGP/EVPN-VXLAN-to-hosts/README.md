# BGP EVPN VXLAN to Linux hosts with L3 anycast gateways on leaves

![image](https://user-images.githubusercontent.com/2031627/151012844-ac984a74-1803-433d-82f9-1157d87d26a8.png)

* Dual connected Linux hosts (FRR)
* Redundant dual eBGP sessions with pair of ToRs (7220 IXR-D2s)
* Double iBGP EVPN session from loopback towards Route Reflectors (spines, SR OS SR-1)

# Evaluating design alternatives
Given this reference topology, we can easily evaluate various design options:

## Unique AS numbers for spines
Some reference designs use a single AS for all spines, to get automatic route filtering based on AS path. To see what changes when we would use a unique AS for each spine:
```
netlab up -v -s nodes.spine2.bgp.underlay_as=65011
```
This changes the BGP peering session between the spines from iBGP to eBGP

Interestingly, this causes the leaves to now receive a default route, via the Linux host:
```
Different AS:
A:leaf1a# show network-instance default route-table ipv4-unicast summary                                                                                                                                           
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv4 unicast route table of network instance default
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+-------------------------------------+-------+------------+----------------------+----------------------+----------+---------+-----------------------+-----------------------+
|               Prefix                |  ID   | Route Type |     Route Owner      |     Active/Fib-      |  Metric  |  Pref   |    Next-hop (Type)    |  Next-hop Interface   |
|                                     |       |            |                      |     status(slot)     |          |         |                       |                       |
+=====================================+=======+============+======================+======================+==========+=========+=======================+=======================+
| 0.0.0.0/0                           | 0     | bgp        | bgp_mgr              | True/success         | 0        | 170     | 10.1.0.45 (indirect)  | None                  |
...

A:leaf1a# show network-instance default protocols bgp routes ipv4 prefix 0.0.0.0/0                                                                                             
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP routes to network "0.0.0.0/0" network-instance  "default"
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Network: 0.0.0.0/0
Received Paths: 2
  Path 1: <Valid,>
    Route source    : neighbor 0.0.0.0
    Route Preference: MED is -, LocalPref is 100
    BGP next-hop    : 0.0.0.0
    Path            :  ?
    Communities     : None
  Path 2: <Best,Valid,Used,>
    Route source    : neighbor 10.1.0.45
    Route Preference: MED is -, LocalPref is 100
    BGP next-hop    : 10.1.0.45
    Path            :  ? [65099, 65002]
    Communities     : None
Path 2 was advertised to: 
[ 10.1.0.45 ]
```
Obviously this is undesirable, and it could be prevented in a number of different ways. The main point is that a virtual setup like this one allows designers to verify the topology, and identify any gotchas like this.

# References
* [Scaleway (2016)](https://www.enog.org/wp-content/uploads/presentations/enog-16/18-Scaleway-P14-fabric-ENOG16.pdf)
* [SR Linux EVPN-VXLAN guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17913AAAA01_V1_SR%20Linux%20R21.11%20EVPN-VXLAN%20User%20Guide.pdf)
* [SR Linux Advanced Solutions guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17902AAAA01_V1_SR%20Linux%20R21.11%20%20Advanced%20Solutions%20Guide.pdf)
