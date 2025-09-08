import asyncio
from exospherehost import StateManager, GraphNodeModel, UnitesModel, UnitesStrategyEnum
from nodes.add_database_pointer import AddDatabasePointerNode
from nodes.generate_items import GenerateItemsNode
from nodes.add_item_to_database import AddItemToDatabaseNode
from nodes.get_max_item import GetMaxItemNode
from nodes.add_ancestor_id import AddAncestorIdNode
from nodes.find_hot_threads import FindHotThreadsNode
from nodes.generate_insight import GenerateInsightNode
from nodes.send_analysis import SendAnalysisNode
from dotenv import load_dotenv

load_dotenv()

asyncio.run(StateManager(namespace="WhatPeopleWant").upsert_graph(
    graph_name="ScrapeYC",
    secrets={},
    graph_nodes=[
        GraphNodeModel(
            node_name=GetMaxItemNode.__name__,
            identifier="GetMaxItem",
            namespace="WhatPeopleWant",
            inputs={},
            next_nodes=[
                "AddDatabasePointer"
            ]
        ),
        GraphNodeModel(
            node_name=AddDatabasePointerNode.__name__,
            identifier="AddDatabasePointer",
            namespace="WhatPeopleWant",
            inputs={
                "item_id": "${{GetMaxItem.outputs.max_item}}"
            },
            next_nodes=[
                "GenerateItems"
            ]
        ),
        GraphNodeModel(
            node_name=GenerateItemsNode.__name__,
            identifier="GenerateItems",
            namespace="WhatPeopleWant",
            inputs={
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            next_nodes=[
                "AddItemToDatabase"
            ]
        ),
        GraphNodeModel(
            node_name=AddItemToDatabaseNode.__name__,
            identifier="AddItemToDatabase",
            namespace="WhatPeopleWant",
            inputs={
                "item_id": "${{GenerateItems.outputs.item_id}}"
            },
            next_nodes=[
                "AddAncestorId"
            ]
        ),
        GraphNodeModel(
            node_name=AddAncestorIdNode.__name__,
            identifier="AddAncestorId",
            namespace="WhatPeopleWant",
            inputs={
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            next_nodes=[
                "FindHotThreads"
            ],
            unites=UnitesModel(
                identifier="AddDatabasePointer",
                strategy=UnitesStrategyEnum.ALL_DONE
            )
        ),
        GraphNodeModel(
            node_name=FindHotThreadsNode.__name__,
            identifier="FindHotThreads",
            namespace="WhatPeopleWant",
            inputs={
                "start_id": "${{AddDatabasePointer.outputs.start_id}}",
                "end_id": "${{AddDatabasePointer.outputs.end_id}}"
            },
            next_nodes=[
                "GenerateInsight"
            ]
        ),
        GraphNodeModel(
            node_name=GenerateInsightNode.__name__,
            identifier="GenerateInsight",
            namespace="WhatPeopleWant",
            inputs={
                "thread_id": "${{FindHotThreads.outputs.thread_id}}"
            },
            next_nodes=[
                "SendAnalysis"
            ]
        ),
        GraphNodeModel(
            node_name=SendAnalysisNode.__name__,
            identifier="SendAnalysis",
            namespace="WhatPeopleWant",
            inputs={
                "insight": "${{GenerateInsight.outputs.insight}}",
                "thread_id": "${{GenerateInsight.outputs.thread_id}}"
            },
            next_nodes=[]
        )
    ]
))
