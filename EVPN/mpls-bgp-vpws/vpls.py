from box import Box

# from netsim.utils import log

"""
Adds a new 'vpls' type service with evpn attributes
"""


def init(topology: Box) -> None:
    print("JvB: init vpls")
    topology.defaults.service.attributes["global"].type.valid_values.extend(["vpls"])

    # Distinguish between interface level or service level attribute
    # topology.defaults.evpn.attributes.service_interface.eth_tag = (
    #    "int"  # Use evpn module attributes
    # )

    # test
    topology.defaults.evpn.attributes.service.evi = {
        "type": "int",
        "service_type": "vxlan",
    }


def post_transform(topo: Box) -> None:
    """
    Processes links with 'vpls' type services, remove any vlans
    """
    print("JvB vpls post_transform")

    # Need to modify node.interfaces, not global topo.links
    # for node in topo.nodes.values():
    #     for intf in node.get("interfaces", []):
    #         for s in intf.get("service", {}):
    #             print(f"Found service: {s.name} s={s}")
    #             if s.type == "vpls":
    #                 if 'sap-id' in s and s['sap-id'] == 'vlan':
    #                     if 'vlan' not in intf:
    #                         log.error(
    #                             f'No access VLAN on {intf.name} node {node.name}',
    #                             log.MissingValue,
    #                             "vpls",
    #                         )
    #                         return False
    #                     s['sap-id'] = None if 'access_id' in intf.vlan else 1 # TODO pick first VLAN in trunk?
    #                     intf.pop('vlan',None) # TODO remove SVI too

    # Check consistency of models
    # print( f"POST: nodes={topo.nodes}" )
    # print( f"POST: links={topo.links}" )
