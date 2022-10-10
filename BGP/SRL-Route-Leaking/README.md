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
* Create and add new routed VXLAN interface with a L3 transit VNI
* Create BGP peering between global VRF and customer VRF
 + Allocate VLAN on loop interfaces ethernet-1/{51,52}
