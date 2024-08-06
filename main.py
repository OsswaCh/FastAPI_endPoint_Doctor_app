from fastapi import  FastAPI, HTTPException
from couchdb import Server
from pydantic import BaseModel
from couchdb.http import ResourceNotFound
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import CONFIG

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CouchDB configuration
couchdb_url = CONFIG["couchdb_url"]
couch = Server(couchdb_url)
db_asone = couch[CONFIG["db_asone"]]


@app.get("/")
def root():
    return {"message": "welcome AsOne4Health-dev"}

# -------- get specialities---------- #     
   
@app.get("/get_specialities")
async def get_specialities():  
    try:
        specialities_document_id ="asone:code:specialite"
        # Check if the specialities document exists in the database
        if specialities_document_id not in db_asone:
            raise HTTPException(status_code=404, detail="specialities document not found")
        # Retrieve the existing specialities document by ID 
        specialities_document = db_asone[specialities_document_id]["specialites"]
        #print(specialities_document)
        return JSONResponse(content=specialities_document,  headers={"Access-Control-Allow-Origin": "*"})
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="specialities document not found")
    

# -------- add a specility ---------- #
@app.put("/add_speciality")
async def add_speciality(speciality: str):
    try:
        specialties_document_id = "asone:code:specialite"
        # Check if the specialities document exists in the database
        if specialties_document_id not in db_asone:
            raise HTTPException(status_code=404, detail="specialities document not found")

        # Retrieve the existing document 
        doc = db_asone[specialties_document_id]

        # get the current specialities and make sure it is a list 
        specialties = doc.get("specialites", [])
        if isinstance(specialties, str):
            specialties = [specialties] 

        # add the new speciality to the list
        if speciality not in specialties:
            specialties.append(speciality)

        # update the document with the new specialities
        doc["specialites"] = specialties
        db_asone.save(doc)

        return JSONResponse(content={"message": "speciality added successfully"}, headers={"Access-Control-Allow-Origin": "*"})
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="specialities document not found")
    

# -------- delete a speciality ---------- #
@app.delete("/delete_speciality")
async def add_speciality(speciality: str):
    try:
        specialties_document_id = "asone:code:specialite"
        # Check if the specialities document exists in the database
        if specialties_document_id not in db_asone:
            raise HTTPException(status_code=404, detail="specialities document not found")

        # Retrieve the existing document 
        doc = db_asone[specialties_document_id]

        # get the current specialities and make sure it is a list 
        specialties = doc.get("specialites", [])
        if isinstance(specialties, str):
            specialties = [specialties] 

        # delete the speciality from the list
        if speciality in specialties:
            specialties.remove(speciality)

        # update the document with the new specialities
        doc["specialites"] = specialties
        db_asone.save(doc)

        return JSONResponse(content={"message": "speciality added successfully"}, headers={"Access-Control-Allow-Origin": "*"})
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="specialities document not found")
    

# -------- add a doctor ---------- #

class Doctor (BaseModel):
    name: str
    speciality: str
    phone: str
    email: str
    address: str
    city: str
    description: str


@app.post("/add_doctor")
async def add_doctor(doctor: Doctor):
    try:
        doc_id = "asone:code:doctors"

        # creation of a new document
        doc = {
            "id": doc_id,
            "name": doctor.name,
            "speciality": doctor.speciality,
            "phone": doctor.phone,
            "email": doctor.email,
            "address": doctor.address,
            "city": doctor.city,
            "description": doctor.description
        }

        db_asone.save(doc)

        return JSONResponse(content={"message": "doctor added successfully"}, headers={"Access-Control-Allow-Origin": "*"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

