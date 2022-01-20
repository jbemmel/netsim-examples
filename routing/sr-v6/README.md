![image](https://user-images.githubusercontent.com/2031627/149630377-12daa5ac-1c78-43af-90d8-b054e479462e.png)

# SRv6 with ISIS and BGP

This example shows an 8-node topology inspired by [a post from Juniper](https://www.juniper.net/documentation/us/en/software/junos/is-is/topics/example/isis-configuring-srv6-network-programming.html).
Edge nodes R0 and R8 form an SRv6-tunnel to transport IPv4 packets between Linux hosts h1 and h2, using BGP with SRv6 extensions (and R2 as Route Reflector)

# SRv6 supported on 7250 IXR?
To answer a question about SRv6 support on 7250 IXR (being a non-FP platform), we can check [the VSR guide](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17166AAADTQZZA01_V1_vSIM%20Installation%20and%20Setup%20Guide%2021.10.R1.pdf) to see that the [IXR-ec](https://onestore.nokia.com/asset/206825)
is supported.

![image](https://user-images.githubusercontent.com/2031627/150256373-c52931c8-86d9-4f48-91d8-2b2def0f2dc0.png)

For convenience, I [added the following to vrnetlab](https://github.com/jbemmel/vrnetlab/blob/jvb-refactor-model-provisioning/sros/docker/launch.py#L149):
```
"ixr-ec": {
        "deployment_model": "integrated",
        "min_ram": 4,  # minimum RAM requirements
        "max_nics": 30,
        **LINE_CARD(
            chassis="ixr-ec",
            card="cpm-ixr-ec",
            card_type="imm4-1g-tx+20-1g-sfp+6-10g-sfp+",
            mda="m4-1g-tx+20-1g-sfp+6-10g-sfp+",
            integrated=True,
        ),
    }
```

we can then modify the topology to emulate 7250 IXR devices:
```
defaults:
  device: sros

  providers:
   clab:
    devices:
     sros:
      provider_type: ixr-ec # Single integrated VM
      interface_name: 1/1/%d # No connectors used
```

After 'netlab up' we can verify the configuration:
```
!(gl)[/configure router "Base" isis 0]
A:admin@r0# /show chassis 
===============================================================================
System Information
===============================================================================
  Name                              : r0
  Type                              : 7250 IXR-ec
  Chassis Topology                  : Standalone
  Location                          : (Not Specified)
  Coordinates                       : (Not Specified)
  CLLI code                         :           
  Number of slots                   : 2
  Oper number of slots              : 2
  Num of faceplate ports/connectors : 30
  Num of physical ports             : 30
  Over Temperature state            : OK
  Base MAC address                  : 52:54:00:f1:a9:00

===============================================================================
Chassis Summary
===============================================================================
Chassis   Role                Status
-------------------------------------------------------------------------------
1         Standalone          up
===============================================================================

!(gl)[/configure router "Base" isis 0]
A:admin@r0# tree | match segm
+-- segment-routing

```
Unfortunately, SRv6 is *not* supported on IXR
