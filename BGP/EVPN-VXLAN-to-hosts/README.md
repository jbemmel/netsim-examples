# BGP EVPN VXLAN to Linux hosts with L3 anycast gateways on leaves

![image](https://user-images.githubusercontent.com/2031627/151011637-45b90d56-da1c-48c8-8ef8-80e31c061957.png)

* Dual connected Linux hosts (FRR)
* Redundant dual eBGP sessions with pair of ToRs (7220 IXR-D2s)
* Double iBGP EVPN session from loopback towards Route Reflectors (spines, SR OS SR-1)

# References
* [Scaleway (2016)](https://www.enog.org/wp-content/uploads/presentations/enog-16/18-Scaleway-P14-fabric-ENOG16.pdf)
