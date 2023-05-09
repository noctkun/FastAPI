from fastapi import FastAPI, Path, HTTPException, status, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}
@app.get("/get-item/{item_id}/{name}")
def get_item(name: str=Query(None,title="Name",description="The name of the item you would like to view",max_length=10,min_length=2)):
    return inventory[item_id]

@app.get("/get-by-name/{item_id}")
def get_by_name(* ,name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID Not Found.")
    # return {"Data": "Not Found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int,item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists."}
    inventory[item_id] = item #{"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item does not exist."}
    inventory[item_id].update(item)
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int=Query(...,description = "The ID of the item to delete",gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID Not Found.")
        # return {"Error": "Item ID not found"}
    del inventory[item_id]
    return {"Succes" : "Item Successfully Deleted"}

# @app.get("/")
# def home():
#     return {"Data": "Test"}
# @app.get("/about")
# def about():
#     return {"Data": "About"}
