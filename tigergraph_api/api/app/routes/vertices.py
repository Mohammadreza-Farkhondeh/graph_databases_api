from typing import Union, List
from fastapi import APIRouter, HTTPException

from api.app.schemas.vertices import UpsertVertices, DeleteVertex
from api.app.tiger_graph import tg

router = APIRouter()


@router.post("/")
async def vertex_upsert(upsert_vertices: UpsertVertices):
    """
    - body: {vertexType, vertices}, where vertices is list of vertices to be upserted
    - return: {"upserted": integer}, number of accepted vertices to be upserted
        ### TigerGraph.upsertVertices: Upserts multiple vertices (of the same type).

        See the description of ``upsertVertex`` for generic information.

        Args:
            vertexType:
                The name of the vertex type.
            vertices:
                A list of tuples in this format:

                [source.wrap,json]
                ----
                [
                    (<vertex_id>, {<attribute_name>: <attribute_value>, …}),
                    (<vertex_id>, {<attribute_name>: (<attribute_value>, <operator>), …}),
                    ⋮
                ]
                ----

                Example:

                [source.wrap, json]
                ----
                [
                    (2, {"name": "Balin", "points": (10, "+"), "bestScore": (67, "max")}),
                    (3, {"name": "Dwalin", "points": (7, "+"), "bestScore": (35, "max")})
                ]
                ----

                For valid values of `<operator>` see xref:tigergraph-server:API:built-in-endpoints.adoc#_operation_codes[Operation codes].

        Returns:
            A single number of accepted (successfully upserted) vertices (0 or positive integer).

        Endpoint:
            - `POST /graph/{graph_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_upsert_data_to_graph[Upsert data to graph]
    """
    try:
        result = tg.conn.upsertVertices(upsert_vertices["vertexType"], upsert_vertices["vertices"])
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())


@router.get("/")
async def vertex_retrieve(vertex_type: str, select: str = "", where: str = "",
                          limit: Union[int, str] = None, sort: str = ""):
    """
    - param by: get vertices by (type, source)
    - param vertex_type: required if by type
    - param source_vertex_id: required if by source
    - param source_vertex_type: required if by source
    - param select: gsql select
    - param where: gsql where
    - param limit: only by source
    - param sort: only by source
    - return: The (selected) details of the (matching) vertex instances (sorted, limited)
        ### TigerGraph.getVertices: Retrieves vertices of the given vertex type.

        *Note*:
            The primary ID of a vertex instance is NOT an attribute, thus cannot be used in
            `select`, `where` or `sort` parameters (unless the `WITH primary_id_as_attribute` clause
            was used when the vertex type was created). /
            Use `getVerticesById()` if you need to retrieve vertices by their primary ID.

        Args:
            vertexType:
                The name of the vertex type.
            select:
                Comma separated list of vertex attributes to be retrieved.
            where:
                Comma separated list of conditions that are all applied on each vertex' attributes.
                The conditions are in logical conjunction (i.e. they are "AND'ed" together).
            sort:
                Comma separated list of attributes the results should be sorted by.
                Must be used with `limit`.
            limit:
                Maximum number of vertex instances to be returned (after sorting).
                Must be used with `sort`.
            fmt:
                Format of the results:
                - "py":   Python objects
                - "json": JSON document
                - "df":   pandas DataFrame
            withId:
                (When the output format is "df") should the vertex ID be included in the dataframe?
            withType:
                (When the output format is "df") should the vertex type be included in the dataframe?
            timeout:
                Time allowed for successful execution (0 = no limit, default).

        Returns:
            The (selected) details of the (matching) vertex instances (sorted, limited) as
            dictionary, JSON or pandas DataFrame.

        Endpoint:
            - `GET /graph/{graph_name}/vertices/{vertex_type}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_list_vertices[List vertices]
    """
    try:
        result = tg.conn.getVertices(vertex_type, select=select, where=where, limit=limit, sort=sort)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())


@router.delete("/")
async def vertex_delete(delete_vertices: DeleteVertex):
    """
    - body: {sourceVertexType, sourceVertexId} is required,
     vertexType, Target and where are optional
    - return: {vertexType: number of deleted}
        ### TigerGraph.delVertices: Deletes vertices from graph.

        *Note*:
            The primary ID of a vertex instance is not an attribute. A primary ID cannot be used in
            `select`, `where` or `sort` parameters (unless the `WITH primary_id_as_attribute` clause
            was used when the vertex type was created). /
            Use `delVerticesById()` if you need to retrieve vertices by their primary ID.

        Args:
            vertexType:
                The name of the vertex type.
            where:
                Comma separated list of conditions that are all applied on each vertex' attributes.
                The conditions are in logical conjunction (i.e. they are "AND'ed" together).
            sort:
                Comma separated list of attributes the results should be sorted by.
                Must be used with `limit`.
            limit:
                Maximum number of vertex instances to be returned (after sorting).
                Must be used with `sort`.
            permanent:
                If true, the deleted vertex IDs can never be inserted back, unless the graph is
                dropped or the graph store is cleared.
           timeout:
                Time allowed for successful execution (0 = no limit, default).

        Returns:
             A single number of vertices deleted.

        The primary ID of a vertex instance is NOT an attribute, thus cannot be used in above
            arguments.

        Endpoint:
            - `DELETE /graph/{graph_name}/vertices/{vertex_type}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_delete_vertices[Delete vertices]
    """
    try:
        result = tg.conn.delVertices(**delete_vertices.__dict__)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())


@router.get("/types")
async def vertex_types(vertex_type: str = None):
    """
    - param vertex_type: if None, get list of vertex types, else get metadata of vertex type parameter
    - return: {details: list | dictionary}
        ### TigerGraph.getVertexTypes: Returns the list of vertex type names of the graph.

        Args:
            force:
                If `True`, forces the retrieval the schema metadata again, otherwise returns a
                cached copy of vertex type metadata (if they were already fetched previously).

        Returns:
            The list of vertex types defined in the current graph.
        * getVertexType: Returns the details of the specified vertex type.

        Args:
            vertexType:
                The name of the vertex type.
            force:
                If `True`, forces the retrieval the schema metadata again, otherwise returns a
                cached copy of vertex type details (if they were already fetched previously).

        Returns:
            The metadata of the vertex type.
    """
    result = tg.conn.getVertexType(vertex_type) if vertex_type else tg.conn.getVertexTypes()
    return result


@router.get("/attrs")
async def vertex_attrs(vertex_type: str):
    """
    - param vertex_type: required
    - return: list of attributes of the type
        ### TigerGraph.getVertexAttrs: Returns the names and types of the attributes of the vertex type.

        Args:
            vertexType:
                The name of the vertex type.

        Returns:
            A list of (attribute_name, attribute_type) tuples.
            The format of attribute_type is one of
             - "scalar_type"
             - "complex_type(scalar_type)"
             - "map_type(key_type,value_type)"
            and it is a string.
    """
    result = tg.conn.getVertexAttrs(vertex_type)
    return result


@router.get("/stats")
async def vertex_stats(vertex_type: str):
    """
    - param vertex_type: required
    - return: Attribute statistics of the vertex; a dictionary of dictionaries.
        ### TigerGraph.getVertexStats: Returns vertex attribute statistics.

        Args:
            vertexTypes:
                A single vertex type name or a list of vertex types names or "*" for all vertex
                types.
            skipNA:
                Skip those non-applicable vertices that do not have attributes or none of their
                attributes have statistics gathered.

        Returns:
            A dictionary of various vertex stats for each vertex type specified.

        Endpoint:
            - `POST /builtins/{graph_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_run_built_in_functions_on_graph[Run built-in functions]
    """
    result = tg.conn.getVertexStats(vertex_type)
    return result
