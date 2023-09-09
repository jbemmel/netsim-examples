from box import Box

"""
Adds a new 'epipe' type service with evpn attributes
"""


def init(topology: Box) -> None:
    print("JvB: init epipe")
    topology.defaults.service.attributes["global"].type.valid_values.extend(["epipe"])

    # Distinguish between interface level or service level attribute
    topology.defaults.evpn.attributes.service_interface.eth_tag = (
        "int"  # Use evpn module attributes
    )

    # test
    topology.defaults.evpn.attributes.service.evi = {
        "type": "int",
        "service_type": "vxlan",
    }


def post_transform(topo: Box) -> None:
    """
    Processes links with 'epipe' type services, and resolves the 'peer' attribute to the loopback IP of the peer
    """
    print("JvB epipe post_transform")

    # Need to modify node.interfaces, not global topo.links
    for node in topo.nodes.values():
        print(f"JvB: Check {node.interfaces}")
        for link in node.get("interfaces", []):
            for s in link.get("service", []):
                print(f"Found service: {s.name} s={s}")
                if s.type == "epipe":
                    for n in link.get("neighbors", []):
                        for s2 in n.get("service", []):
                            if s.name == s2.name:
                                peer_ip = topo.nodes[n.node].loopback.ipv4
                                print(f"JvB: Resolved {link.service} to {peer_ip}")
                                n.epipe_peer = peer_ip
                                break
                # eth_tag is in neighbor too

    # Check consistency of models
    # print( f"POST: nodes={topo.nodes}" )
    # print( f"POST: links={topo.links}" )
