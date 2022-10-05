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

## Feature overview

* S1/S2: SR Linux nodes with symmetric IRB EVPN/VXLAN and proxy ARP; iBGP over ISIS IGP
* C1/C2: SR OS nodes with SRv6 over ISIS; no BGP
* PE1/PE2: L2 MPLS EVPN over LDP, OSPF IGP
