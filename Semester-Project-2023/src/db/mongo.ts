import {MongoClient} from 'mongodb';
import { MONGO_URL } from '$env/static/private'

const client = new MongoClient(MONGO_URL);

export function start_mongo(): Promise<MongoClient> {
    console.log("Starting Mongo...")
    client.connect()
    client.db("kafka")
    return client.connect()
}

export default client.db("kafka")
