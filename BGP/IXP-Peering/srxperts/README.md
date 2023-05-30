# 1. Emulating an IXP peering use case

The first topology [topology.clab.yml](./topology.clab.yml) emulates a [peering situation at AMS-IX](https://www.peeringdb.com/ix/26).
Filtering for 800G we find (potential) peers T-Mobile Thuis (AS 50266, IP 80.249.211.171) and NovoServe BV (AS 24875, IP 80.249.208.126) in 
subnet 80.249.208.0/22. 

Start this topology using
```
sudo clab deploy -t topology.clab.yml
```

and verify that route prefixes are being exchanged by logging into the SR Linux node:
```
ssh admin@clab-IXP-Peering-srlinux (password NokiaSrl1!)
/show network-instance default route-table all
```

