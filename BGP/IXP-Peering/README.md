# Sample Netlab topology to emulate IXP peering

This topology uses a custom Peeringdb plugin to query PeeringDb API (https://www.peeringdb.com/api/) for the IP addresses used at a given IXP site.
The IXP site is defined by a custom **ixp** attribute on the first node

![image](https://user-images.githubusercontent.com/2031627/194957437-e9c74aa3-88af-433f-83be-390f0c28f5e8.png)

## PeeringDB and IRR scripted provisioning

The sample Ansible playbook under ./srl-ansible provisions BGP peering and filter policies based on queries.
PeeringDB is queried for IP addresses (for a given list of AS numbers), and irrexplorer.nlnog.net is consulted for a list of prefixes.

The prefixes are checked to be validated through RPKI - so although the routers themselves don't run RPKI, the net result is that only RPKI validated
prefixes are programmed.
