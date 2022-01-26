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


# References
* [Scaleway (2016)](https://www.enog.org/wp-content/uploads/presentations/enog-16/18-Scaleway-P14-fabric-ENOG16.pdf)
* [SR Linux EVPN-VXLAN guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17913AAAA01_V1_SR%20Linux%20R21.11%20EVPN-VXLAN%20User%20Guide.pdf)
* [SR Linux Advanced Solutions guide 21.11](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17902AAAA01_V1_SR%20Linux%20R21.11%20%20Advanced%20Solutions%20Guide.pdf)
