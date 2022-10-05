# Next Level IXP network designs

In support of IXPs like DE-CIX who are deploying advanced peering solutions including
EVPN with proxy ARP over an MPLS RSVP-TE core, this example illustrates a combination
of various protocols and features in a single comprehensive Netlab topology

![image](https://user-images.githubusercontent.com/2031627/194090612-8494753e-3268-4e87-a46b-e984574df9df.png)

## Deploy the lab
```
git clone https://github.com/jbemmel/netlab.git --branch advanced-ixp-use-case
source netlab/setup.sh
netlab up
```

### Multi-vendor integration testing

Replace 's2' with FRR
```
netlab -s nodes.s2.device=frr up
```

## Feature overview

* S1/S2: SR Linux nodes with symmetric IRB EVPN/VXLAN and proxy ARP; iBGP over ISIS IGP
* C1/C2: SR OS nodes with SRv6 over ISIS; no BGP
* PE1/PE2: SR OS nodes with L2 MPLS EVPN over LDP; OSPF IGP

### Comprehensive topology validation ✅

```
jeroen@jvm:~/srlinux/netsim-examples/NextLevel$ docker exec -it clab-NextLevel-h2 ping 192.168.0.1 -c2
PING 192.168.0.1 (192.168.0.1): 56 data bytes
64 bytes from 192.168.0.1: seq=0 ttl=62 time=9.713 ms
64 bytes from 192.168.0.1: seq=1 ttl=62 time=4.950 ms

--- 192.168.0.1 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 4.950/7.331/9.713 ms
```
