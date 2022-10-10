# SR Linux VRF Route Leaking

This sample topology illustrates VRF route leaking on SR Linux, using a physical loopback link on each leaf.

![image](https://user-images.githubusercontent.com/2031627/190536974-5075942e-83b9-4236-849d-cc8dee9ad539.png)

![image](https://user-images.githubusercontent.com/2031627/190538093-05786531-8e84-4d13-bcc5-70765a0f4a93.png)

## Bring up lab

The topology uses a tool called Netlab, it can be launched as follows:
```
netlab up
```

# Add customer VRF on leaf

The procedure to add a customer VRF on a leaf involves the following items:
* Create new IP VRF
    * Enable IPv4 forwarding for BGP unnumbered
    * Assign BGP-EVPN EVI
* Create and add new routed VXLAN interface
    * Assign a L3 transit VNI
* Create eBGP peering between global VRF and customer VRF
    * Allocate subinterface with VLAN tag on loop interfaces ethernet-1/{51,52}
    * Assign/use customer specific AS
    * Customer specific import/export policy with prefix list

For simplicity of provisioning, the various parameters could be allocated as follows:
1. Customer specific **ID**
2. VLAN tag / subinterface index: **ID**
3. Customer AS: \<base-AS\> (e.g. 65000) + **ID**
4. L3 transit VNI/EVPN EVI: same as **customer AS**
