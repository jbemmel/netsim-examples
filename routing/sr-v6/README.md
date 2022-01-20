![image](https://user-images.githubusercontent.com/2031627/149630377-12daa5ac-1c78-43af-90d8-b054e479462e.png)

# SRv6 with ISIS and BGP

This example shows an 8-node topology inspired by [a post from Juniper](https://www.juniper.net/documentation/us/en/software/junos/is-is/topics/example/isis-configuring-srv6-network-programming.html).
Edge nodes R0 and R8 form an SRv6-tunnel to transport IPv4 packets between Linux hosts h1 and h2, using BGP with SRv6 extensions (and R2 as Route Reflector)

# 7250 IXR support for SRv6
To answer a question about SRv6 support on 7250 IXR (being a non-FP platform), we can check [the VSR guide](https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/3HE17166AAADTQZZA01_V1_vSIM%20Installation%20and%20Setup%20Guide%2021.10.R1.pdf) to see that the [IXR-ec](https://onestore.nokia.com/asset/206825)
is supported.

![image](https://user-images.githubusercontent.com/2031627/150256373-c52931c8-86d9-4f48-91d8-2b2def0f2dc0.png)

For convenience, I added the following to vrnetlab:
```
"ixr-ec": {
        "deployment_model": "integrated",
        "min_ram": 4,  # minimum RAM requirements
        "max_nics": 30,
        **LINE_CARD(
            chassis="ixr-ec",
            card="cpm-ixr-ec",
            mda="m4-1g-tx+20-1g-sfp+6-10g-sfp+",
            integrated=True,
        ),
        "power": {"modules": {"ac/hv": 3, "dc": 4}},
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
```

After 'netlab up' we can verify the configuration:
