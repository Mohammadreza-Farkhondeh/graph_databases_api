from fastapi import APIRouter, HTTPException

from api.app.schemas.graph import UpsertJob, Connect
from api.app.tiger_graph import tg

router = APIRouter()


@router.post("/connect")
def connect(cnct: Connect):
    """
    - body:host, graphname, username, password required, secret is optional, if None, then conn.getSecret will be called
    - return: the connection id that should be in upcoming requests header
    """
    try:
        if not cnct.host.startswith("http"):
            cnct.host = "http://" + cnct.host
        result = tg.add_client(
            host=cnct.host,
            username=cnct.username,
            password=cnct.password,
            graphname=cnct.graphname,
            secret=cnct.secret)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return {"connection_id": result}


@router.get("/schema")
def get_schema():
    """
    - return: schema of the graph
        ### TigerGraph.getSchema: Retrieves the schema metadata (of all vertex and edge type and, if not disabled, the
                User-Defined Type details) of the graph.

            Args:
                udts:
                    If `True`, the output includes User-Defined Types in the schema details.
                force:
                    If `True`, retrieves the schema metadata again, otherwise returns a cached copy of
                    the schema metadata (if they were already fetched previously).

            Returns:
                The schema metadata.

            Endpoint:
                - `GET /gsqlserver/gsql/schema`
                    See xref:tigergraph-server:API:built-in-endpoints.adoc#_show_graph_schema_metadata[Show graph schema metadata]
    """
    try:
        result = tg.conn.getSchema()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result


@router.post("/load")
def load_data():
    """
    - send file to load its data in graph
    - note : in runLoadingJobWithFile, they use open(file_path) so we can path bytes also
    - return: idk
        ### TigerGraph.runLoadingJobWithFile: Execute a loading job with the referenced file.

        The file will first be uploaded to the TigerGraph server and the value of the appropriate
        FILENAME definition will be updated to point to the freshly uploaded file.

        NOTE: The argument `USING HEADER="true"` in the GSQL loading job may not be enough to
        load the file correctly. Remove the header from the data file before using this function.

        Args:
            filePath:
                File variable name or file path for the file containing the data.
            fileTag:
                The name of file variable in the loading job (DEFINE FILENAME <fileTag>).
            jobName:
                The name of the loading job.
            sep:
                Data value separator. If your data is JSON, you do not need to specify this
                parameter. The default separator is a comma `,`.
            eol:
                End-of-line character. Only one or two characters are allowed, except for the
                special case `\\r\\n`. The default value is `\\n`
            timeout:
                Timeout in seconds. If set to `0`, use the system-wide endpoint timeout setting.
            sizeLimit:
                Maximum size for input file in bytes.

        Endpoint:
            - `POST /ddl/{graph_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_run_a_loading_job[Run a loading job]
    """
    try:
        # TODO load file with bytes or dataframe?
        result = tg.conn.runLoadingJobWithFile()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result


@router.post("/upsert")
def upsert_data(upsert_job: UpsertJob):
    """
    - body: send a json in request body to load it in graph, {data, atmoic=False, ...}
    - return:  The result of upsert (number of vertices and edges accepted/upserted).
        ### TigerGraph.upsertData: Upserts data (vertices and edges) from a JSON file or a file with equivalent object structure.

        Args:
            data:
                The data of vertex and edge instances, in a specific format.
            atomic:
                The request is an atomic transaction. An atomic transaction means that updates to
                the database contained in the request are all-or-nothing: either all changes are
                successful, or none are successful.
            ackAll:
                If `True`, the request will return after all GPE instances have acknowledged the
                POST. Otherwise, the request will return immediately after RESTPP processes the POST.
            newVertexOnly:
                If `True`, the request will only insert new vertices and not update existing ones.
            vertexMustExist:
                If `True`, the request will only insert an edge if both the `FROM` and `TO` vertices
                of the edge already exist. If the value is `False`, the request will always insert new
                edges and create the necessary vertices with default values for their attributes.
                Note that this parameter does not affect vertices.
            updateVertexOnly:
                If `True`, the request will only update existing vertices and not insert new
                vertices.

        Returns:
            The result of upsert (number of vertices and edges accepted/upserted).

        Endpoint:
            - `POST /graph/{graph_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_upsert_data_to_graph[Upsert data to graph]
    """
    try:
        result = tg.conn.upsertData(**upsert_job.__dict)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result


@router.get("/query")
def query_graph(query: str):
    """run installed query and get response
    - param query: name of query that is installed before
    - return: output of query
        ### TigerGraph.runInstalledQuery: Runs an installed query.

        The query must be already created and installed in the graph.
        Use `getEndpoints(dynamic=True)` or GraphStudio to find out the generated endpoint URL of
        the query. Only the query name needs to be specified here.

        Args:
            queryName:
                The name of the query to be executed.
            params:
                Query parameters. A string of param1=value1&param2=value2 format or a dictionary.
                See below for special rules for dictionaries.
            timeout:
                Maximum duration for successful query execution (in milliseconds).
                See xref:tigergraph-server:API:index.adoc#_gsql_query_timeout[GSQL query timeout]
            sizeLimit:
                Maximum size of response (in bytes).
                See xref:tigergraph-server:API:index.adoc#_response_size[Response size]
            usePost:
                Defaults to False. The RESTPP accepts a maximum URL length of 8192 characters. Use POST if additional parameters cause
                you to exceed this limit, or if you choose to pass an empty set into a query for database versions >= 3.8
            runAsync:
                Run the query in asynchronous mode.
                See xref:gsql-ref:querying:query-operations#_detached_mode_async_option[Async operation]
            replica:
                If your TigerGraph instance is an HA cluster, specify which replica to run the query on. Must be a
                value between [1, (cluster replication factor)].
                See xref:tigergraph-server:API:built-in-endpoints#_specify_replica[Specify replica]
            threadLimit:
                Specify a limit of the number of threads the query is allowed to use on each node of the TigerGraph cluster.
                See xref:tigergraph-server:API:built-in-endpoints#_specify_thread_limit[Thread limit]
            memoryLimit:
                Specify a limit to the amount of memory consumed by the query (in MB). If the limit is exceeded, the query will abort automatically.
                Supported in database versions >= 3.8.
                See xref:tigergraph-server:system-management:memory-management#_by_http_header[Memory limit]

        Returns:
            The output of the query, a list of output elements (vertex sets, edge sets, variables,
            accumulators, etc.

        Notes:
            When specifying parameter values in a dictionary:

            - For primitive parameter types use
                `"key": value`
            - For `SET` and `BAG` parameter types with primitive values, use
                `"key": [value1, value2, ...]`
            - For `VERTEX<type>` use
                `"key": primary_id`
            - For `VERTEX` (no vertex type specified) use
                `"key": (primary_id, "vertex_type")`
            - For `SET<VERTEX<type>>` use
                `"key": [primary_id1, primary_id2, ...]`
            - For `SET<VERTEX>` (no vertex type specified) use
                `"key": [(primary_id1, "vertex_type1"), (primary_id2, "vertex_type2"), ...]`

        Endpoints:
            - `GET /query/{graph_name}/{query_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_run_an_installed_query_get[Run an installed query (GET)]
            - `POST /query/{graph_name}/{query_name}`
                See xref:tigergraph-server:API:built-in-endpoints.adoc#_run_an_installed_query_post[Run an installed query (POST)]
    """
    try:
        result = tg.conn.runInstalledQuery(query)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, e.__str__())
    return result
