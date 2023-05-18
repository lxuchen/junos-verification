DIRECTORY = "config"


DEVICE_OBJECTS = {
    "group_1": [
        {
            "ip": ["router_1", "router_2", "router_3"],
            "commands": [
                "show route summary",
                "show route protocol ldp",
                "show route protocol ospf",
                "show bgp summary"
            ]
        }
    ],
    "group_2": [
        {
            "ip": [
                "router_4",
                "router_5"
            ],
            "commands": [
                "show route 0.0.0.0/0 exact",
                "show bgp summary group TestGroup"
            ]
        }
    ]
}
