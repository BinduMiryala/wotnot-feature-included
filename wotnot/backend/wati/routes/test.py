from fastapi import FastAPI, UploadFile, File

app = FastAPI()

async def get_file_length(file: UploadFile):
    file_content = await file.read()  # Read file content asynchronously
    return len(file_content)  # Get length in bytes

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_length = await get_file_length(file)

    import requests
    access_token='EAAlQiHyuxU0BO29ZAFWfZA50lZAAgOtITqHFuA0Lj77rqcgzvn0HTBEeoEhgnGAUbZACwZAkPlddJTZC9WZBJFcYTMApZBZCTD4ZCVM01fRWO1FClFXjYSQSUncZAJZArWZAtNsBfPDezDZAzmFffX5f1bTJWnyCqZBBVsoBzZAYAhvyvF7ClZBvH98jqsLJOvakV5G4yly1PpAZDZD'
    url = f"https://graph.facebook.com/v20.0/upload:MTphdHRhY2htZW50OjgxNWY4NWQwLWE4NDktNGQxZi1hOTM1LTZhYzk0MTFjOWRiYz9maWxlX2xlbmd0aD0zMjI1MyZmaWxlX3R5cGU9aW1hZ2UlMkZqcGVnJmZpbGVfbmFtZT1kcC5qcGc=?sig=ARYsVecNqLd04O-6Z6c&access_token={access_token}"



    file_content = await file.read()


    payload = file_content
    headers = {
    
    'Content-Type': 'text/plain',
    'accept': 'application/json',
    'file_offset': '0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

            # Print the request details
    print("===== REQUEST DETAILS =====")
    print("URL:", response.request.url)
    print("Method:", response.request.method)
    print("Headers:", response.request.headers)
    print("Body:", response.request.body[:500] if response.request.body else "No Body")  # Print first 500 bytes if body exists


    print(response.text)

    return {"filename": response.text, "size_in_bytes": file_length}




