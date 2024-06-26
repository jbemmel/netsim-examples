from box import Box

"""
Adds custom epipe and local_epipe link->node (interface) attributes
"""
def init(topology: Box) -> None:
    attr = topology.defaults.attributes
    attr.interface.epipe = 'str'
    attr.interface.local_epipe = 'int'

def post_transform(topo: Box) -> None:
  """
  Processes links with 'epipe' attribute, and resolves to the loopback IP of the peer
  """
  print( f"JvB epipe post_transform" )

  # Need to modify node.interfaces, not global topo.links
  for node in topo.nodes.values():
   for link in node.interfaces:
    if 'epipe' in link:
       peer = topo.nodes[ link.epipe ].loopback.ipv4
       print( f"JvB: Resolved {link.epipe} to {peer}" )
       link.epipe_peer = peer

  # Check consistency of models
  # print( f"POST: nodes={topo.nodes}" )
  # print( f"POST: links={topo.links}" )
