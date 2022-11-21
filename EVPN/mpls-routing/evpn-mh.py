import typing, netaddr
from box import Box

from netsim import api

"""
Enable 'evpn.mh_lag' attribute on link interfaces
"""
def init(topology: Box) -> None:
  topology.defaults.evpn.attributes.interface = ['mh_lag']

"""
Trigger custom config file for any interfaces that are part of a MH lag
"""
def post_transform(topology: Box) -> None:

  # Iterate over node[x].interfaces
  for n, ndata in topology.nodes.items():
    for i in ndata.interfaces:
      if i.type in ['lan','p2p','svi'] and 'evpn' in i and 'mh_lag' in i.evpn:
          api.node_config(ndata,'sros_evpn_mh_lag.j2')
      elif i.type == 'vlan_member':
          parent_if = ndata.interfaces[ i.parent_ifindex - 1 ]
          if 'evpn' in parent_if and 'mh_lag' in parent_if.evpn:
            lag_id = parent_if.evpn.mh_lag
            lag_ifname = f"lag-{lag_id}"
            i.ifname = i.ifname.replace( i.parent_ifname, lag_ifname )
            i.parent_ifname = lag_ifname
