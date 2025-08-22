from exospherehost import Runtime

from nodes.add_database_pointer import AddDatabasePointerNode
from nodes.generate_items import GenerateItemsNode
from nodes.add_item_to_database import AddItemToDatabaseNode
from nodes.get_max_item import GetMaxItemNode
from nodes.add_ancestor_id import AddAncestorIdNode
from nodes.generate_insight import GenerateInsightNode
from nodes.find_hot_threads import FindHotThreadsNode
from nodes.send_analysis import SendAnalysisNode

Runtime(
    namespace="WhatPeopleWant",
    name="main_runtime_0",
    nodes=[
        AddDatabasePointerNode,
        GenerateItemsNode,
        AddItemToDatabaseNode,
        GetMaxItemNode,
        AddAncestorIdNode,
        FindHotThreadsNode,
        GenerateInsightNode,
        SendAnalysisNode,
    ]
).start()