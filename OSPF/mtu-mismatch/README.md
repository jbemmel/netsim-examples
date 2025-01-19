# The ticking time bomb aka "ignore MTU mismatch"

Network engineers have [long warned](https://blog.ipspace.net/2009/11/ip-ospf-mtu-ignore-is-dangerous-command/) that ignoring an MTU mismatch on an OSPF adjacency is a bad idea.
But how bad is it, really?

This lab aims to quantify the problem, by establishing the number of VLANs that triggers oversized OSPF database updates between a Dell OS9 and a Dell OS10 switch.
* In OS9 the default MTU for interfaces is 9216 [on S4048]((https://www.dell.com/support/manuals/en-kn/dell-emc-os-9/s4048-on-9.14.2.5-config-pub/configure-the-mtu-size-on-an-interface?guid=guid-2c62872c-1387-4fd1-b49c-a990c7e7ddc4&lang=en-us), and 1554 [on S5048F](https://www.dell.com/support/manuals/en-hk/dell-emc-os-9/s5048f-on-9.14.2.8-cli-pub/mtu?guid=guid-1e4ea3a2-6a71-4457-a464-32ddea227e23&lang=en-us)
* In OS10, [the default](https://www.dell.com/support/manuals/en-us/dell-emc-smartfabric-os10/smartfabric-os-user-guide-10-5-2-6/default-mtu-configuration?guid=guid-929ecde7-b507-49a8-a9e9-53bff7187110&lang=en-us) is 1532.

Can you see where this is going?

On OS10:
```
conf t
int eth1
ip ospf mtu-ignore
end
```

5 VLANs:
```
08:10:02.599914 eth1  M   ifindex 865 aa:c1:ab:f8:6e:c0 ethertype IPv4 (0x0800), length 392: (tos 0xc0, ttl 1, id 2025, offset 0, flags [none], proto OSPF (89), length 372)
    10.1.0.2 > 224.0.0.5: OSPFv2, LS-Update, length 352
	Router-ID 10.0.0.1, Backbone Area, Authentication Type: none (0), 2 LSAs
	  LSA #1
	  Advertising Router 10.0.0.1, seq 0x80000018, age 136s, length 148
	    Router LSA (1), LSA-ID: 10.0.0.1
	    Options: [External]
	    Router LSA Options: [none]
	      Stub Network: 10.0.0.1, Mask: 255.255.255.255
		topology default (0), metric 0
	      Stub Network: 10.1.0.0, Mask: 255.255.255.252
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.3, Interface Address: 172.16.0.1
		topology default (0), metric 10
	      Stub Network: 172.16.0.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.3, Interface Address: 172.16.1.1
		topology default (0), metric 10
	      Stub Network: 172.16.1.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.3, Interface Address: 172.16.2.1
		topology default (0), metric 10
	      Stub Network: 172.16.2.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.3, Interface Address: 172.16.3.1
		topology default (0), metric 10
	      Stub Network: 172.16.3.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.3, Interface Address: 172.16.4.1
		topology default (0), metric 10
	      Stub Network: 172.16.4.0, Mask: 255.255.255.0
		topology default (0), metric 10
	  LSA #2
	  Advertising Router 10.0.0.3, seq 0x80000015, age 136s, length 136
	    Router LSA (1), LSA-ID: 10.0.0.3
	    Options: [External]
	    Router LSA Options: [none]
	      Stub Network: 10.0.0.3, Mask: 255.255.255.255
		topology default (0), metric 0
	      Neighbor Router-ID: 10.0.0.1, Interface Address: 172.16.0.3
		topology default (0), metric 10
	      Stub Network: 172.16.0.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.1, Interface Address: 172.16.1.3
		topology default (0), metric 10
	      Stub Network: 172.16.1.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.1, Interface Address: 172.16.2.3
		topology default (0), metric 10
	      Stub Network: 172.16.2.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.1, Interface Address: 172.16.3.3
		topology default (0), metric 10
	      Stub Network: 172.16.3.0, Mask: 255.255.255.0
		topology default (0), metric 10
	      Neighbor Router-ID: 10.0.0.1, Interface Address: 172.16.4.3
		topology default (0), metric 10
	      Stub Network: 172.16.4.0, Mask: 255.255.255.0
		topology default (0), metric 10
```

10+10 VLANs OS10 (10.1.0.2) -> OS9 on eth1
```
08:55:45.057593 aa:c1:ab:b1:1a:f9 > 01:00:5e:00:00:05, ethertype IPv4 (0x0800), length 1394: (tos 0xc0, ttl 1, id 4798, offset 0, flags [none], proto OSPF (89), length 1380)
    10.1.0.2 > 224.0.0.5: OSPFv2, LS-Update, length 1360
```

20+20 VLANs:
```
09:19:31.857721 aa:c1:ab:f4:db:05 > 01:00:5e:00:00:05, ethertype IPv4 (0x0800), length 1430: (tos 0xc0, ttl 1, id 6344, offset 0, flags [none], proto OSPF (89), length 1416)
    10.1.0.1 > 224.0.0.5: OSPFv2, LS-Update, length 1396
```