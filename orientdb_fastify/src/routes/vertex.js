import classRoutes from "./class.js";

const vertexRoutes = async (app, opts, done) => {

    app.post('/', async (request, reply) => {
        try {
            const { dbSession, body} = request;
            const { className, properties } = body;

            let result = dbSession.create("VERTEX", className)
                .set(properties)
                .one();

            reply.status(201).send({message: `vertex in ${className} created`, result:result});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    app.get('/', async (request, reply) => {
        try {
            const { dbSession, params } = request;
            const { filter, className } = params
            let c = className ? (className) : "E"

            let result = dbSession.select()
                .from(c)
                .where(filter)
                .all();

            reply.status(200).send({result: result});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    app.put('/', async (request, reply) => {
        try {
        const { dbSession, params, body } = request;
        const { properties, rid, className, filter } = body;
        let result;

        if (rid) {
            result = dbSession.update(rid)
                .set(properties)
                .one();
        } else if (className && filter) {
            result = dbSession.update(className)
                .set(properties)
                .where(filter)
                .one();
        }

        reply.status(200).send({result: result, message:"record updated successfully"});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    app.delete('', async (request, reply) => {
        try {
        const { dbSession, body } = request;
        const { rid, className, filter } = body;
        let result;

        if (rid) {
            result = dbSession.command(`DELETE ${rid}`)
        } else if (className && filter) {
            result = dbSession.delete(className)
                .where(filter);
        }
        reply.status(204).send({result: result});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    done();
};

export default vertexRoutes;