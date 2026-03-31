from pydantic import BaseModel

class Address(BaseModel):
       city : str
       state : str
       pin : int

class Student(BaseModel):
       name : str
       gender : str
       age : int 
       address : Address

address_dict = {'city': 'Nashik' , 'state': 'maharashtra', 'pin': 422000  }

address1 = Address(**address_dict)

student_dict = {'name': 'Viv' , 'gender': 'male', 'age': 21, 'address': address1}

student1 = Student(**student_dict)
print(student1)
print(student1.name)
print(student1.address)

temp = student1.model_dump() #for dictionary 
temp2 = student1.model_dump_json()

print(temp)
print(temp2)

