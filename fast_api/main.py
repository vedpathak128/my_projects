from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Annotated,Field,Literal,computed_field,Optional
app=FastAPI()

class Patient(BaseModel):

    id:Annotated[str,Field(..., description='id of the patient',examples=['P001'])]
    name: Annotated[str,Field(..., description='name of the patient')]
    city:Annotated[str,Field(..., description='city where the patient is living')]
    age:Annotated[int,Field(..., gt=0,lt=120,description='age of the patient')]
    gender:Annotated[literal['male','female','others'],Field(..., description='gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]
    @computed_field
    @property 
    def bmi(self) -> float: 
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self)-> str:
        if(self.bmi<18.5):
            return 'Under weight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:'Obese'

class patientupdate(BaseModel):

    name: Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]

def load_data():
    with open ('patients.json','r') as f:
        data=json.load(f)
    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
@app.get("/")
def hello():
    return {" message : patient management system api"}

@app.get('/about')
def about():
    return {'message': 'a full functional api to manage patients data'}

@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description='id of the patient in the DB', example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,deatil='patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(..., description="sort on the basis od height,weight,bmi"),order:str =Query('asc',description='sort in acs or dec order')):

    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='not a valid request')
    if order not in ['asc','dec']:
        raise HTTPException(status_code=400,detail=f'not a valid request from {['asc','dsc']}')
    data=load_data()
    
    sort_order=True if order=='dec' else False

    sorted_data =sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient:Patient): # patient is pydentic obj
    # 1 load the existing data
    data=load_data() # python dictionary
    # 2 check if it already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists')
    # 3 if not in dataset add the patient in the 
    # list
    data[patient.id]=patient.model_dump(exclude=['id'])
    # save info as json
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'the new patient is created'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:patientupdate):
    data=load_data() 
    if patient_id not in data:
        raise HTTPException(status_code=404,description='patient not found')
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.item():
        existing_patient_info[key]=value
    existing_patient_info["id"]=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)  
    patient_pydantic_object.model_dump(exclude="id")
    existing_patient_info=patient_pydantic_object
    data[patient_id]=existing_patient_info

    save_data(data)
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,description='patient not found')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})


