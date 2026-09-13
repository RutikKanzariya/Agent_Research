from fastapi import FastAPI,Query,HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to FastAPI"}

@app.get("/products/{id}")
def get_products(id : int):
    products = ["Brush","Laptop","Mouse","Moniter"]
    return products[id]
# http://127.0.0.1:8000/products/2

@app.get("/products")
def list_products(name: str = Query(
    default=None,
    min_length=1,
    max_length=50,
    description="Search by products name (case insensitive)",
)):
    prodcuts = get_all_products()

    if name:
        needle = name.strip().lower()
        product = [p for p in prodcuts if needle in p.get("name","").lower()]

        if not product:
            raise HTTPException(
                status_code=404,detail=f"No Product found matchin name={name}"
            )
        total = len(product)
    return {"total":total,"items":product}