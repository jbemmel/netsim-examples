# Sample Netlab topology to emulate IXP peering

This topology uses a custom Peeringdb plugin to query PeeringDb API (https://www.peeringdb.com/api/) for the IP addresses used at a given IXP site.
The IXP site is defined by a custom **ixp** attribute on the first node

![image](https://user-images.githubusercontent.com/2031627/194957437-e9c74aa3-88af-433f-83be-390f0c28f5e8.png)

## PeeringDB and IRR scripted provisioning

The sample Ansible playbook under ./srl-ansible provisions BGP peering and filter policies based on queries.
PeeringDB is queried for IP addresses (for a given list of AS numbers), and irrexplorer.nlnog.net is consulted for a list of prefixes.

The prefixes are checked to be validated through RPKI - so although the routers themselves don't run RPKI, the net result is that only RPKI validated
prefixes are programmed.

## Figuring out % of RPKI prefixes

One way:
- Create a policy to set local-preference for prefixes matching a list
```
policy as15169 {
        default-action {
            policy-result reject
        }
        statement rpki {
            match {
                prefix-set rpki-validated-15169
            }
            action {
                policy-result accept
                bgp {
                    local-preference {
                        set 101
                    }
                }
            }
        }
    }
```

``` 
A:Apple# info from state /network-instance default bgp-rib afi-safi ipv4-unicast ipv4-unicast rib-in-out | grep attr 
                                attr-id 12
                                attr-id 12
                                attr-id 12
                                attr-id 11
                                attr-id 10
                                attr-id 9
                                attr-id 11
                                attr-id 12
                                attr-id 16  <-- This attribute set has local-pref 101
                                attr-id 16
                                attr-id 11
                                attr-id 10
                                attr-id 9
                                attr-id 11
                                attr-id 7
                                attr-id 8
```

Use ```grep -c``` to count number of prefixes having this attribute set

## Generating IRR prefix lists

For SR OS, using [bgpq4](https://github.com/bgp/bgpq4)
```
jeroen@jvb-vm:~/srlinux/bgpq4$ ./bgpq4 -nl eltel AS20597
/configure policy-options
delete prefix-list "eltel"
prefix-list "eltel" {
    prefix 81.9.0.0/20 type exact {
    }
    prefix 81.9.32.0/20 type exact {
    }
    prefix 81.9.96.0/20 type exact {
    }
    prefix 81.222.128.0/20 type exact {
    }
    prefix 81.222.160.0/20 type exact {
    }
    prefix 81.222.192.0/18 type exact {
    }
    prefix 85.249.8.0/21 type exact {
    }
    prefix 85.249.224.0/19 type exact {
    }
    prefix 89.112.0.0/17 type exact {
    }
    prefix 217.170.64.0/19 type exact {
    }
}
```