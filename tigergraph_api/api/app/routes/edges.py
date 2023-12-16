from typing import Union, List
from fastapi import APIRouter, HTTPException

from api.app.schemas.edges import UpsertEdges, DeleteEdge
from api.app.tiger_graph import tg

router = APIRouter()


@router.post("/")
async def edge_upsert(upsert_edges: UpsertEdges):
    """
    - body: {edgeType, edges}, where edges is list of edges to be upserted
    - return: {"upserted": integer}, number of accepted edges to be upserted
        ### TigerGraph.upsertEdges:Upserts multiple edges (of the same type).

        Args:
            sourceVertexType:
                The name of the source vertex type.
            edgeType:
                The name of the edge type.
            targetVertexType:
                The name of the target vertex type.
            edges:
                A list in of tuples in this format:
                ```
                [
                    (<source_vertex_id>, <target_vertex_id>, {<attribute_name>: <attribute_value>, …}),
                    (<source_vertex_id>, <target_vertex_id>, {<attribute_name>: (<attribute_value>, <operator>), …})
                    ⋮
                ]
                ```
                Example:
                ```
                [
                    (17, "home_page", {"visits": (35, "+"), "max_duration": (93, "max")}),
                    (42, "search", {"visits": (17, "+"), "max_duration": (41, "max")})
                ]
                ```
                For valid values of `<operator>` see https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#operation-codes .

        Returns:
            A single number of accepted (successfully upserted) edges (0 or positive integer).

        Endpoint:
            - `POST /graph/{graph_name}`
                See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#upsert-data-to-graph
    """
    try:
        result = tg.conn.upsertEdges(upsert_edges["edgeType"], upsert_edges["edges"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return {"upserted": result}


@router.get("/")
async def edge_retrieve(by: str = "type",
                        edge_type: str = "", source_vertex_type: str = "", source_vertex_id: str = "",
                        select: str = "", where: str = "", limit: Union[int, str] = None, sort: str = ""):
    """
    - param by: get edges by (type, source)
    - param edge_type: required if by type
    - param source_vertex_id: required if by source
    - param source_vertex_type: required if by source
    - param select: gsql select
    - param where: gsql where
    - param limit: only by source
    - param sort: only by source
    - return: The (selected) details of the (matching) edge instances (sorted, limited)
        ### TigerGraph.getEdgesByType: Retrieves edges of the given edge type regardless the source vertex.

        Args:
            edgeType:
                The name of the edge type.
            fmt:
                Format of the results returned:
                - "py":   Python objects
                - "json": JSON document
                - "df":   pandas DataFrame
            withId:
                (When the output format is "df") Should the source and target vertex types and IDs
                be included in the dataframe?
            withType:
                (When the output format is "df") should the edge type be included in the dataframe?

        Returns:
            The details of the edge instances of the given edge type as dictionary, JSON or pandas
            DataFrame.
        ### getEdges: Retrieves edges of the given edge type originating from a specific source vertex.

        Only `sourceVertexType` and `sourceVertexId` are required.
        If `targetVertexId` is specified, then `targetVertexType` must also be specified.
        If `targetVertexType` is specified, then `edgeType` must also be specified.

        Args:
            sourceVertexType:
                The name of the source vertex type.
            sourceVertexId:
                The primary ID value of the source vertex instance.
            edgeType:
                The name of the edge type.
            targetVertexType:
                The name of the target vertex type.
            targetVertexId:
                The primary ID value of the target vertex instance.
            select:
                Comma separated list of edge attributes to be retrieved or omitted.
            where:
                Comma separated list of conditions that are all applied on each edge's attributes.
                The conditions are in logical conjunction (i.e. they are "AND'ed" together).
            sort:
                Comma separated list of attributes the results should be sorted by.
            limit:
                Maximum number of edge instances to be returned (after sorting).
            fmt:
                Format of the results returned:
                - "py":   Python objects
                - "json": JSON document
                - "df":   pandas DataFrame
            withId:
                (When the output format is "df") Should the source and target vertex types and IDs
                be included in the dataframe?
            withType:
                (When the output format is "df") Should the edge type be included in the dataframe?
            timeout:
                Time allowed for successful execution (0 = no time limit, default).

        Returns:
            The (selected) details of the (matching) edge instances (sorted, limited) as dictionary,
            JSON or pandas DataFrame.

        Endpoint:
            - `GET /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}`
                See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#list-edges-of-a-vertex
    """
    try:
        if by == "type" and edge_type:
            result = tg.conn.getEdgesByType(edge_type)
        elif by == "source" and source_vertex_type and source_vertex_id:
            result = tg.conn.getEdges(edge_type, select, where, limit, sort)
        else:
            raise HTTPException(400, "by parameter should be 'type' or 'source'")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result


@router.delete("/")
async def edge_delete(delete_edges: DeleteEdge):
    """
    - body: {sourceVertexType, sourceVertexId} is required,
     edgeType, Target and where are optional
    - return: {edgeType: number of deleted}
        ### TigerGraph.delEdges: Deletes edges from the graph.

        Only `sourceVertexType` and `sourceVertexId` are required.
        If `targetVertexId` is specified, then `targetVertexType` must also be specified.
        If `targetVertexType` is specified, then `edgeType` must also be specified.

        Args:
            sourceVertexType:
                The name of the source vertex type.
            sourceVertexId:
                The primary ID value of the source vertex instance.
            edgeType:
                The name of the edge type.
            targetVertexType:
                The name of the target vertex type.
            targetVertexId:
                The primary ID value of the target vertex instance.
            where:
                Comma separated list of conditions that are all applied on each edge's attributes.
                The conditions are in logical conjunction (they are connected as if with an `AND` statement).
            limit:
                Maximum number of edge instances to be returned after sorting.
            sort:
                Comma-separated list of attributes the results should be sorted by.
            timeout:
                Time allowed for successful execution. The default is `0`, or no limit.

        Returns:
             A dictionary of `edge_type: deleted_edge_count` pairs.

        Endpoint:
            - `DELETE /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/{target_vertex_type}/{target_vertex_id}`
                See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#delete-an-edge
    """
    try:
        result = tg.conn.delEdges(**delete_edges.__dict__)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result


@router.get("/types")
async def edge_types(edge_type: str = None):
    """
    - param edge_type: if None, get list of edge types, else get metadata of edge type parameter
    - return: {details: list | dictionary}
        ### TigerGraph.getEdgeTypes: Returns the list of edge type names of the graph.

        Args:
            force:
                If `True`, forces the retrieval the schema metadata again, otherwise returns a
                cached copy of edge type metadata (if they were already fetched previously).

        Returns:
            The list of edge types defined in the current graph.
        ### getEdgeType: Returns the details of the edge type.

        Args:
            edgeType:
                The name of the edge type.
            force:
                If `True`, forces the retrieval the schema details again, otherwise returns a cached
                copy of edge type details (if they were already fetched previously).

        Returns:
            The metadata of the edge type.
    """
    try:
        result = tg.conn.getEdgeType(edge_type) if edge_type else tg.conn.getEdgeTypes()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return {"detail": result}


@router.get("/attrs")
async def edge_attrs(edge_type: str):
    """
    - param edge_type: required
    - return: list of attributes of the type
        ### TigerGraph.getEdgeAttrs: Returns the names and types of the attributes of the edge type.

        Args:
            edgeType:
                The name of the edge type.

        Returns:
            A list of (attribute_name, attribute_type) tuples.
            The format of attribute_type is one of
             - "scalar_type"
             - "complex_type(scalar_type)"
             - "map_type(key_type,value_type)"
            and it is a string.
    """
    try:
        result = tg.conn.getEdgeAttrs(edge_type)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    # TODO discover the response
    return result


@router.get("/stats")
async def edge_stats(edge_type: Union[str, List[str]]):
    """
    - param edge_type: required
    - return: Attribute statistics of the edge; a dictionary of dictionaries.
        ### TigerGraph.getEdgeStats: Returns edge attribute statistics.

        Args:
            edgeTypes:
                A single edge type name or a list of edges types names or '*' for all edges types.
            skipNA:
                Skip those edges that do not have attributes or none of their attributes have
                statistics gathered.

        Returns:
            Attribute statistics of edges; a dictionary of dictionaries.

        Endpoint:
            - `POST /builtins/{graph_name}`
                See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#run-built-in-functions-on-graph
    """
    try:
        result = tg.conn.getEdgeStats(edge_type)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result
