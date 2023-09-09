from box import Box

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
    Processes links with 'vpls' type services
    """
    print("JvB vpls post_transform")

    # Need to modify node.interfaces, not global topo.links
    # for node in topo.nodes.values():
    #     print(f"JvB: Check {node.interfaces}")
    #     for link in node.get("interfaces", []):
    #         for s in link.get("service", {}):
    #             print(f"Found service: {s.name} s={s}")
    #             if s.type == "vpls":
    #                 for n in link.get("neighbors", []):
    #                     if "service" in n:
    #                         peer_ip = topo.nodes[n.node].loopback.ipv4
    #                         print(f"JvB: Resolved {link.service} to {peer_ip}")
    #                         n.epipe_peer = peer_ip
    #             # eth_tag is in neighbor too

    # Check consistency of models
    # print( f"POST: nodes={topo.nodes}" )
    # print( f"POST: links={topo.links}" )
