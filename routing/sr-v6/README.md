![image](https://user-images.githubusercontent.com/2031627/149630377-12daa5ac-1c78-43af-90d8-b054e479462e.png)

# SRv6 with ISIS and BGP

This example shows an 8-node topology inspired by [a post from Juniper](https://www.juniper.net/documentation/us/en/software/junos/is-is/topics/example/isis-configuring-srv6-network-programming.html).
Edge nodes R0 and R8 form an SRv6-tunnel to transport IPv4 packets between Linux hosts h1 and h2, using BGP with SRv6 extensions (and R2 as Route Reflector)
