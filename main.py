from fastapi import FastAPI, Request, HTTPException

title = "OpenERP Main API"
description = "This is the main API for OpenERP"
author = "@JRudransh"
version = "0.1.0"

app = FastAPI(title=title, description=description, version=version, author=author)


@app.get("/example/")
async def read_example(request: Request):
    if not request.state.has_permission('read', 'res_example'):
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"message": "This is an example read endpoint", "user": request.state.user_name}


@app.post("/example/")
async def create_example(request: Request):
    if not request.state.has_permission('create', 'res_example'):
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"message": "This is an example create endpoint", "user": request.state.user_name}


@app.put("/example/")
async def update_example(request: Request):
    if not request.state.has_permission('update', 'res_example'):
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"message": "This is an example update endpoint", "user": request.state.user_name}


@app.delete("/example/")
async def delete_example(request: Request):
    if not request.state.has_permission('delete', 'res_example'):
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"message": "This is an example delete endpoint", "user": request.state.user_name}
