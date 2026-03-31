from pydantic import BaseModel , EmailStr , Field , field_validator , model_validator , computed_field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):  #Creating Pydantic Model
        
       name: str
       email: EmailStr
       age: int  # = Field(gt=0, lt=23)
       weight : float = Field(gt=0) #gt means greater than 0 it should be 
       height: float
       married : bool 
       allergies : Optional[List[str]] = None   
       contact : Dict[str, str]

       @computed_field
       @property 
       def bmi(self) -> float:
              bmi = round(self.weight/(self.height**2),2)
              return bmi
                
def insert_patient_data(pat: Patient):
       
              print(pat.name)
              print(pat.email)
              print(pat.age)
              print(pat.weight)
              print(pat.contact)
              print(pat.allergies)
              print(pat.married)
              print('BMI', pat.bmi)
              print("Inserted Into DB")

patient_info = {'name': 'viv' , 'email': 'viv@idfc.com', 'age': 21
                 , 'weight' : 78.99 , 'height': 366 , 'married': True , 'contact': {'emergency': '22255', 'Body_Count': '45'} }  #PY Dict

patient1 = Patient(**patient_info)  #Unpacking Dictionary with ** 

insert_patient_data(patient1)
