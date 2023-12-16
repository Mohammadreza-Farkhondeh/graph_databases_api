import orientjs from "orientjs";
import classRoutes from "./class.js";
import Pools from '../middlewares.js';
import NodeCache from "node-cache"

// this map will have several clients based on request header
const Clients = NodeCache()

const clientRoutes = async (app, opts, done) => {

    app.post('/connect', async (request, reply) => {
        try{
            const { X_HOST, X_PORT } = request.headers;
            const { username, password } = request.body;

            if (!X_HOST || !X_PORT){
                reply
                    .status(400)
                    .send({"error": "X_HOST and X_PORT should be in request headers"});
            }
            if (!username || !password){
                reply
                    .status(400)
                    .send({"error": "username and password should be in request body"});
            }

            let client = await orientjs.OrientDBClient.connect({
            host: X_HOST,
            port: X_PORT,
            });

            const key = `${X_HOST}:${X_PORT}`
            Clients.set(key, client);
            setTimeout(() => {
                Clients.delete(`${X_HOST}:${X_PORT}`);}, 1000 * 60 * 60 * 24);

            let databases = await client.listDatabases({username: username, password: password})

            reply
                .status(201)
                .send({"message": "connected to host successfully", "databases": databases});
        } catch (err) {
        reply
            .status(500)
            .send({"error": err.message});
        }
    })

    app.post('/database', async (request, reply) => {
        try {
            const { X_HOST, X_PORT } = request.headers;
              if (!X_HOST || !X_PORT){
                reply
                    .status(400)
                    .send({"error": "X_HOST and X_PORT should be in request headers"});
            }
            const key = `${X_HOST}:${X_PORT}`
            let client = Clients.get(key);
            if (!client) {
                throw new Error('Client not found, connect first');
            }
            const poolKey = `${key}/${name}`;
            let pool = Pools.get(poolKey);
            if (!pool) {
                pool = await client.sessions({ name, pool: { max: 10 } });
                Pools.set(poolKey, pool, 1800);
            }
            let session = await pool.acquire();
            let clusters = await session.cluster.list();
            await session.close();
            reply.status(200).send({
            message: 'Connected to database on OrientDB server',
            key: poolKey,
            clusters
            });
            } catch (err) {
            console.error(err);
            reply.status(500).send({ error: 'Error connecting to database on OrientDB server' });
            }
            });

    done();
};

export default clientRoutes;