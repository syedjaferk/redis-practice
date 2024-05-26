from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from gearsclient import GearsRemoteBuilder as GearsBuilder, execute
import redis


r = redis.Redis(host='localhost', port=6379, decode_responses=True)
app = FastAPI()

# Mongo Db Connection
MONGO_CONN_STR = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_CONN_STR)
database = mongo_client['test']
collection = database["todos"]

class Todo(BaseModel):
    id: str
    name: str
    description: str = None

@app.post("/todos/")
def create_todo(todo: Todo):
    collection.insert_one(todo.dict())
    return {} 

@app.get("/todos/{todo_id}", response_model=Todo)
def read_item(todo_id: str):
    res = GearsBuilder(reader='KeysOnlyReader', r=r).map(lambda x: execute('hgetall', x, todo_id)).run()
    print(res)
    # result = r.execute_command('RG.TRIGGER', 'read_through_cache', todo_id)
    # if result:
    #     return result[0]
    raise HTTPException(status_code=404, detail="Item not found")