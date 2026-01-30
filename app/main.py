from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from service.products import get_all_products, add_product, remove_product, change_product, load_data
from schema.product import Product, ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Dict

load_dotenv()
app = FastAPI()

def common_logic():
    # print("Hello World")
    return "Hello there"

@app.get('/', response_model=dict)
def root(dep = Depends(common_logic)):
    DB_PATH = os.getenv("BASE_URL")
    return {"Message" : "Welcome to FastAPI", "Dependency": dep, "Data_Path": DB_PATH}


# @app.get('/products/')
# def get_products():
#    return get_all_products()

@app.get('/products')
def list_products(
    dep = Depends(load_data),
    name:str | None = Query(
    default=None,
    min_length=1,
    max_length=50,
    description="Search by product name"
    ),
    sort_by_price:bool = Query(
        default=False,
        description="Sort products by price"
    ),
    order : str = Query(
        default="asc",
        description="Sort order when sort_by_price = true (asc, desc)"
    ),
    limit : int = Query(
    default=5,
    ge = 1,
    le=100,
    description="Number of items return"
    ),
    offset : int = Query(
    default=0,
    ge =0,
    description="Pagination Offset"
    )
):
    products = dep

    if name: 
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail=f"No product found matching name={name}"
        )

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    products = products[offset:offset+limit]

    return {
        "Total" : len(products),
        "Limit" : limit,
        "items" : products
    }

@app.get('/products/{product_id}')
def get_product_id(
    product_id : str = Path(
        ..., 
        min_length = 36,
        max_length= 36,
        description = "UUID of the product",
        examples = "394d40e7-2a95-445d-8738-c6af6be5a97e"
    )
):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail=f"Product not found with id = {product_id}")



@app.put('/products', status_code=201)
def create_product(product:Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"
    try:
        add_product(product_dict)
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")   
    return product.model_dump(mode="json")


@app.delete('/products/{product_id}')
def delecte_product(product_id : UUID = Path(..., description= "Product UUID")):
    try:
        data = remove_product(str(product_id))
        return data
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))
    

@app.put('/products/{product_id}')
def update_product(product_id : UUID = Path(..., description= "Product UUID"), payload : ProductUpdate = ...,):
    try:
        update_product= change_product(str(product_id), payload.model_dump(mode="json",exclude_unset=True))
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))