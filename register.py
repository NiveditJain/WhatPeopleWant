import asyncio
from exospherehost import StateManager
from nodes.add_database_pointer import AddDatabasePointerNode
from nodes.generate_items import GenerateItemsNode
from nodes.add_item_to_database import AddItemToDatabaseNode
from nodes.get_max_item import GetMaxItemNode
from nodes.add_ancestor_id import AddAncestorIdNode
from nodes.find_hot_threads import FindHotThreadsNode
from nodes.generate_insight import GenerateInsightNode


asyncio.run(StateManager(namespace="WhatPeopleWant").upsert_graph(
    graph_name="ScrapeYC",
    secrets={},
    graph_nodes=[
        {
            "node_name": GetMaxItemNode.__name__,
            "identifier": "GetMaxItem",
            "namespace": "WhatPeopleWant",
            "inputs": {},
            "next_nodes": [
                "AddDatabasePointer"
            ]
        },
        {
            "node_name": AddDatabasePointerNode.__name__,
            "identifier": "AddDatabasePointer",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "item_id": "${{GetMaxItem.outputs.max_item}}"
            },
            "next_nodes": [
                "GenerateItems"
            ]
        },
        {
            "node_name": GenerateItemsNode.__name__,
            "identifier": "GenerateItems",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            "next_nodes": [
                "AddItemToDatabase"
            ]
        },
        {
            "node_name": AddItemToDatabaseNode.__name__,
            "identifier": "AddItemToDatabase",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "item_id": "${{GenerateItems.outputs.item_id}}"
            },
            "next_nodes": [
                "AddAncestorId"
            ]
        },
        {
            "node_name": AddAncestorIdNode.__name__,
            "identifier": "AddAncestorId",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            "next_nodes": [
                "FindHotThreads"
            ],
            "unites": { "identifier": "AddDatabasePointer" }
        },
        {
            "node_name": FindHotThreadsNode.__name__,
            "identifier": "FindHotThreads",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            "next_nodes": [
                "GenerateInsight"
            ]
        },
        {
            "node_name": GenerateInsightNode.__name__,
            "identifier": "GenerateInsight",
            "namespace": "WhatPeopleWant",
            "inputs": {
                "thread_id": "${{FindHotThreads.outputs.thread_id}}"
            },
            "next_nodes": []
        }
    ]
))
