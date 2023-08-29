from box import Box

"""
Adds custom epipe attributes
"""
def init(topology: Box) -> None:
    attr = topology.defaults.attributes 
    attr['global'].epipes = "dict"
    attr.link.service = "id" # refers to global 'services' dict
    attr.interface.service = "id" # refers to global 'services' dict
    topology.defaults.evpn.attributes.interface.epipe_eth_tag = "int" # Use evpn module attributes

    # attr.extra['global'].extend( ["services"] )
    attr['global'].services = "dict"
    # attr.extra['node'] = [ "services" ]
    attr['global'].service = {
       "id": { "type": "int", "min_value": 1, "max_value": 4095 },
       "type": { "type": "id", "valid_values": [ "vlan", "epipe" ] }
     }

def post_transform(topo: Box) -> None:
  """
  Processes links with 'epipe' attribute, and resolves the 'peer' attribute to the loopback IP of the peer
  """
  print( "JvB epipe post_transform" )

  # Promote link-level service attributes to all interfaces on that link
  for link in topo.links:
    if 'service' in link:
      for intf in link.interfaces:
        if 'service' not in intf:
          intf.service = link.service

  # Need to modify node.interfaces, not global topo.links
  for node in topo.nodes.values():
   # print( f"JvB: Check {node.interfaces}" )
   for link in node.interfaces:
    if 'service' in link:
       svc = topo.services[ link.service ]
       print( f"Found service: {svc}" )
       link.service = {
         "name": link.service,
         **svc
       }
       def resolve_peer_intf(peer):
          for l2 in topo.links:
           for i in l2.interfaces:
            if i.node == peer and 'service' in i:
              if i.service == link.service.name or i.service.name == link.service.name:
                if (('evpn' in link and 'epipe_eth_tag' in link.evpn) ^ 
                    ('evpn' in i and 'epipe_eth_tag' in i.evpn)):
                  continue # Skip if one is EVPN and the other isn't
                return i
          return None
       for n in link.get('neighbors',[]):
         intf = resolve_peer_intf(n.node)
         if intf:
           peer_ip = topo.nodes[ intf.node ].loopback.ipv4
           print( f"JvB: Resolved {link.service} to {peer_ip}" )
           n.service_peer = peer_ip
          # eth_tag is in neighbor too

  # Check consistency of models
  # print( f"POST: nodes={topo.nodes}" )
  # print( f"POST: links={topo.links}" )
