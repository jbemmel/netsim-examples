#
# A plugin for PeeringDB - provisions interface IP addresses based on a lookup of the BGP AS
#
import typing, requests, json, netaddr
from box import Box
from netsim import data

"""
Adds a custom node ixp attribute (marks an IXP where peering is taking place)
"""
def init(topology: Box) -> None:
    topology.defaults.attributes.node.append('ixp')
    topology.defaults.bgp.attributes.interface.append('multihop')

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
Convert eBGP peerings with IXP to multihop peerings between connected nodes
"""
def post_transform(topology: Box) -> None:



    # Iterate over all IXP nodes, update interface IP addresses based on PeeringDB
    ixp = topology.get('ixp',"AMS-IX")
    for n, ndata in topology.nodes.items():
      if 'ixp' in ndata:
        for i in ndata.bgp.neighbors:

          def update_ips(ip,prefix,ipv):
            net = netaddr.IPNetwork( f"{ip}/{prefix}" )
            ip0, ip1 = [ str(i) for i in list(net) ]
            ixp_ip = ip0 if ip1==ip else ip1

            ndata.interfaces[i.ifindex-1][ipv] = f"{ixp_ip}/{prefix}"
            for nb in ndata.interfaces[i.ifindex-1].neighbors:
              peer = topology.nodes[ nb.node ]
              intf = [ l for l in peer.interfaces if l.ifname == nb.ifname ]
              if intf:
                intf[0][ipv] = f"{ip}/{prefix}"
                intf[0].bgp.multihop = True

          (ip4,ip6) = query_peeringdb( i['as'], n )
          if ip4 and 'ipv4' in ndata.af:
            update_ips(ip4,31,'ipv4')
          if ip6 and 'ipv6' in ndata.af:
            update_ips(ip6,127,'ipv6')

        ndata.pop('bgp',None)
