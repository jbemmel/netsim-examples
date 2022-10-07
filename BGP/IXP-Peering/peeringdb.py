#
# A plugin for PeeringDB - provisions interface IP addresses based on a lookup of the BGP AS
#
import typing, requests, json, netaddr
from box import Box
from netsim import data

"""
Lookup ASN in PeeringDB and return ipv4,ipv6 peering IPs at given IX
"""
def query_peeringdb(asn: int, ix: str) -> typing.Tuple[typing.Optional[str],typing.Optional[str]]:
  url = f"https://peeringdb.com/api/netixlan?asn={asn}&name={ix}"
  print( f"PeeringDB query: {url}" )
  resp = requests.get(url=url)
  pdb_json = json.loads(resp.text)
  print( pdb_json )
  if 'data' in pdb_json and pdb_json['data']:
    site = pdb_json['data'][0]
    return ( site['ipaddr4'], site['ipaddr6'] )
  return ( None, None )

"""
Update eBGP peering IP addresses at given IXP site
"""
def post_transform(topology: Box) -> None:

  # Iterate over all IXP nodes, update interface IP addresses based on PeeringDB
  for n, ndata in topology.nodes.items():
    print( f"Processing {n} bgp.neighbors" )
    updated_neighbors = []
    for i in ndata.bgp.neighbors:
      print(i)
      def update_ips(ip,prefix,ipv):
        net = netaddr.IPNetwork( f"{ip}/{prefix}" )
        ixp_ip = str( net[1] )
        ndata.interfaces[i.ifindex-1][ipv] = f"{ixp_ip}/{prefix}"
        for nb in ndata.interfaces[i.ifindex-1].neighbors:
          peer = topology.nodes[ nb.node ]
          intf = [ l for l in peer.interfaces if l.ifname == nb.ifname ]
          if intf:
            intf[0][ipv] = f"{ip}/{prefix}"

      if 'ixp' in ndata:
        (ip4,ip6) = query_peeringdb( i['as'], n )
        if ip4 and 'ipv4' in ndata.af:
          update_ips(ip4,22,'ipv4')    # Assume /22 is large enough
        if ip6 and 'ipv6' in ndata.af:
          update_ips(ip6,64,'ipv6')

        ndata.pop('bgp',None) # Remove BGP peerings from IXP node
      else:
        # Assumes IXP nodes are listed first...update peering IPs
        peer = topology.nodes[ i.name ]
        if 'ixp' in peer:
          continue
        for l in peer.interfaces:
          print(l)
          if l.ifname == ndata.interfaces[ i.ifindex-1 ].ifname:
            print( f"Found peering interface {l}" )
            if 'ipv4' in l and 'ipv4' in i:
              i.ipv4 = l.ipv4
            if 'ipv6' in l and 'ipv6' in i:
              i.ipv6 = l.ipv6
            updated_neighbors = [ i ]  # Keep only this one

    if updated_neighbors:
      ndata.bgp.neighbors = updated_neighbors
