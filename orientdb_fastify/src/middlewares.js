import NodeCache from "node-cache"
const Pools = NodeCache()

const PoolMiddleware = async (request, reply) => {
    try{
        const { host, port, name} = request.body
        if (!host || !port || !name) {
            throw new Error('Host, port, and database name headers are required');
        }
        const key = `${host}:${port}/${name}`;
        let pool = Pools.get(key);
        if (!pool) {
            throw new Error('Pool not found');
        }
        request.session = await pool.acquire();
        } catch (err) {
            console.error(err);
            reply.status(500).send({ error: 'Error creating or getting session or pool' });
}};


export  { Pools, PoolMiddleware}