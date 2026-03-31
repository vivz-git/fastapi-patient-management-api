# ----------- Import Lib. -----------
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime , timedelta 
from database import engine
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
import models

models.Base.metadata.create_all(bind=engine)

# Security config

SECRET_KEY = "mykey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Password_Hashing 

#"I need a tool that can hash passwords"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#"Take password → convert into secure format"
def get_password_hash(password):
    return pwd_context.hash(password)


#3. Verify Function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ----------- App Init API -----------
app = FastAPI()


# ----------- DB Session Handler -----------
# This function basically gives us a DB connection
# for each request and then safely closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------- Schemas (Input Validation) -----------

# Used when creating a new patient
class Patient(BaseModel):
    id: str
    name: str
    age: int

#======== User Authentication Schema ========#
class UserCreate(BaseModel):  #Used for registration
    name: str
    email: str
    password: str

class UserLogin(BaseModel): #Used for login
    email: str
    password: str

class Token(BaseModel):   #Used as a response 
    access_token: str
    token_type: str


# Used when updating (fields optional)
class PatientUpdate(BaseModel):
    name: str | None = None   # optional
    age: int | None = Field(None, gt=0)


# ----------- Basic Routes -----------

@app.get("/")
def home():
    return {"message": "Patient API is running 🚀"}

@app.get("/about")
def about():
    return {"message": "Backend built using FastAPI + PostgreSQL"}

# ----------- Register ----------- #

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    #Check if user exists 
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail= "User already exists")
    #else 
    hashed_password = get_password_hash(user.password)

    #create user object 
    new_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password =hashed_password

)
    #Save to DB 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  #Refreshes data from DB 

    return {"message": "User registered successfully"}

# ----------- Creating Token ----------- #
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# ----------- Token + JWT ----------- #
@app.post("/token", response_model=Token)
def user_login(user: UserLogin, db:Session = Depends(get_db)):

    #Check if the user exists 
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    #If it does not exists 
    if not db_user:
        raise HTTPException(status_code=400, detail= "Not found mate")
    
    #IF User exists but the password is entered wrong by the user 
    if not verify_password(user.password , db_user.hashed_password):
        raise HTTPException(status_code=400, detail= "wrong password try again")
    
    #else create token 
    access_token = create_access_token(data={"sub": db_user.email})

    return Token(access_token=access_token, token_type="bearer")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ----------- CREATE -----------

@app.post("/create")
def create_patient(patient: Patient, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    # check if patient already exists
    existing_patient = db.query(models.Patient).filter(
        models.Patient.id == patient.id
    ).first()

    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # create new patient object
    new_patient = models.Patient(
        id=patient.id,
        name=patient.name,
        age=patient.age
    )

    # add and save to DB
    db.add(new_patient)
    db.commit()

    return {"message": f"{patient.id} created successfully"}


# ----------- READ ALL -----------

@app.get("/patients")
def get_all_patients(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    # fetch all records
    patients = db.query(models.Patient).all()
    return patients


# ----------- READ BY ID -----------

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):

    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


# ----------- UPDATE -----------

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    # first check if record exists
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # only update what user sends
    update_data = patient_update.model_dump(exclude_unset=True)

    # dynamic update (important concept)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()

    return {"message": f"{patient_id} updated successfully"}


# ----------- DELETE -----------

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()

    return {"message": f"{patient_id} removed successfully"}

