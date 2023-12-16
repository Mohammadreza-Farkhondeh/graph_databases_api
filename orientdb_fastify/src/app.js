import fastify from "fastify";
import classRouter from './routes/class.js'
import clientRouter from './routes/client.js'
import edgeRouter from './routes/edge.js'
import vertexRouter from './routes/vertex.js'

const app = fastify()

app.register(clientRouter, { prefix: '/' })
app.register(classRouter, { prefix: '/class' })
app.register(edgeRouter, { prefix: '/edge' })
app.register(vertexRouter, { prefix: '/vertex' })

const start = async () => {
  try{
    await fastify.listen(3000)
  } catch (err) {
      fastify.log.error(err);
      process.exit(1)
  }
}
