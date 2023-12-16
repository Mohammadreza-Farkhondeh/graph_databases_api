const supportedAttributes = ["NAME", "SHORTNAME", "SUPERCLASS", "SUPERCLASSES", "OVERSIZE", "ADDCLUSTER",
                                     "REMOVECLUSTER", "STRICTMODE", "CLUSTERSELECTION", "CUSTOM", "ABSTRACT"];

const classRoutes = async (app, opts, done) => {

    app.get('/', async (request, reply) => {
        try {
            const {dbSession} = request;
            let classes = dbSession.query("list classes");
            reply.status(200).send({classes: classes});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    app.post('/', async (request, reply) => {
        try {
            const {dbSession, body} = request;
            const {className, superClass, abstract} = body;
            let command = `CREATE CLASS ${className}`;
            if (superClass) {
                command += `EXTENDS ${superClass}`;
            }
            if (abstract === true) {
                command += "ABSTRACT";
            }
            let result = dbSession.command(command);
            reply.status(201).send({message: `class ${className} created`});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");

        }
    })

    app.get('/:className', async (request, reply) => {
        try {
            const {dbSession, params} = request;
            const {className} = params;
            let result = dbSession.query(`select *
                                          from (select expand(classes) from metadata:schema)
                                          where name = '${className}'`);
            reply.status(200).send({result: result});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    app.put('/:className', async (request, reply) => {
        try {
            const {dbSession, params, body} = request;
            const {className} = params;
            const {properties} = body;
            let batch = "BEGIN ";

            for (let key in properties) {
                if (!supportedAttributes.includes(key)) {
                    let value = obj[key];

                    if (typeof value === "string") {
                        value = `"${value}"`;
                    } else if (typeof value === "boolean") {
                        value = value.toString().toLowerCase();
                    }

                    batch += `ALTER CLASS ${className} ${key}=${value} `;
                }
            }
            batch += "COMMIT";
            let result = dbSession.batch(batch);
            reply.status(200).send({result: result, message: "class altered successfully"});
        } catch (err) {
            console.error(err);
            reply.status(500).send("error occurred, check your request");
        }
    })

    done();
};

export default classRoutes;