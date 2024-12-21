from fastapi import FastAPI, Depends,HTTPException,Path
from pydantic import BaseModel,Field
from function import generate_otp,validate_contact ,send_otp
from db import update_contact,fetch_contact,set_contact,delete_otp,delete_verified

app=FastAPI()


class Response(BaseModel):
    message: str

class PasswordRequest(BaseModel):
    contact: str = Field(..., description="Enter a valid email or phone number (include country code)")
    password: str = Field(..., description="Enter the password (min 8 characters)", min_length=8)
    confirm_password: str = Field(..., description="Confirm the password (min 8 characters)", min_length=8)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the password management API!"}

@app.post("/Signup/request_otp/{contact}",response_model=Response)
async def request_otp(
    contact:str=Path(...,description="enter the valid email or phone_number(include country code)" )
):
    """
    API to request otp
    """

    cleaned_data= contact.strip()
    if not cleaned_data:
        raise HTTPException(status_code=400, detail="This field cannot be empty")
    contact_type =validate_contact(cleaned_data)
    # check if the contact already exists or not
    existing_contact = fetch_contact(cleaned_data)
    if existing_contact:
        raise HTTPException(status_code=400, detail="Contact already exists")

    otp=generate_otp()
    otp_data={
        "user_id":contact,
        "otp":otp,
        "email_phone":contact_type
    }
    set_contact(cleaned_data,otp_data)
    send_otp(contact,otp,contact_type)

    return {"message": f"OTP sent to {contact_type}"}
    
@app.post("/Signup/verification/{contact}/{otp}",response_model=Response)
async def otp_verification(
    otp:str =Path(...,description="Enter the 4 digit otp"),
    contact:str=Path(...,description="enter the valid email or phone_number(include country code)" )
):
    """
    API to verify the otp
    """
    cleaned_data= contact.strip()
    stored_data= fetch_contact(cleaned_data)
    stored_otp= stored_data['otp']
    if not stored_data:
        raise HTTPException(status_code=400, detail="UserId not found")

    if str(otp).strip() != str(stored_otp).strip():
        raise HTTPException(status_code=400,detail="Invalid otp")

    # is the acount is verifies ,then creates a new bool field
    data={'is_verified':True}
    update_contact(cleaned_data,data) 
    # delete the otp from db after verification
    delete_otp(cleaned_data)
    return {"message": "OTP verified successfully"}

@app.post("/Signup/password/{contact}/{password}/{confirm_password}",response_model=Response)
async def create_password(
    contact: str = Path(..., description="Enter a valid email or phone number (include country code)"),
    password: str = Path(..., min_length=8, description="Enter the password"),
    confirm_password: str = Path(..., min_length=8, description="Confirm the password")
):
    """
    API to create the password
    """
    
    cleaned_data= contact.strip()
    stored_data= fetch_contact(cleaned_data)
    
    if not stored_data:
        raise HTTPException(status_code=400,detail="UserId not found")
    if stored_data.get("is_verified") != True:
        raise HTTPException(status_code=400, detail="Account is not verified")
    
    if password != confirm_password:
        raise HTTPException(status_code=400,detail="Password do not match")
    
    code = {"password":password}
    update_contact(cleaned_data,code)
    
    return  {"message": "Password created successfully"}


@app.post("/Signin/{contact}/{password}",response_model=Response)
async def signin(
    contact:str=Path(...,description="enter the valid email or phone_number(include country code)"),
    password:str=Path(...,description="Enter the password")
    
):
    """
    API to signin
    """
    cleaned_data= contact.strip()
    contact_data= fetch_contact(cleaned_data)
    if not contact_data:
        raise HTTPException(status_code=400, detail="No contact found")
    if contact_data['password']!= password:
        raise HTTPException(status_code=400,detail="Invalid contact or password")
    
    return {"message": "Login successful"}


@app.post("/forget_password/{contact}",response_model=Response)
async def reset_Password(
    contact:str=Path(...,description="enter the valid email or phone_number(include country code)"),

):
    """
    API to to request otp when forgot the password
    """
    cleaned_data= contact.strip()
    if not cleaned_data:
        raise HTTPException(status_code=400, detail="This field cannot be empty")
    stored_data= fetch_contact(cleaned_data)
    
    if not stored_data:
        raise HTTPException(status_code=400,detail="UserId not found")
    if stored_data.get("is_verified") != True:
        raise HTTPException(status_code=400, detail="Account is not verified")
    
    # generate otp
    otp=generate_otp()
    otp_data={
        "otp":otp,
    }
    update_contact(cleaned_data,otp_data)
    contact_type =validate_contact(cleaned_data)
    send_otp(contact,otp,contact_type)

    delete_verified(cleaned_data)

    return {"message": f"OTP sent to {contact}"}

@app.post("/forget_password/{contact}/verification/{otp}",response_model=Response)
async def verify_otp(
    contact:str=Path(...,description="enter the valid email or phone_number(include country code)"),
    otp:str =Path(...,description="Enter the 4 digit otp"),

):
    """
    API to verify the otp when forgot the password
    """
    cleaned_data= contact.strip()
    stored_data= fetch_contact(cleaned_data)
    stored_otp= stored_data['otp']
    if not stored_data:
        raise HTTPException(status_code=400, detail="UserId not found")

    if str(otp).strip() != str(stored_otp).strip():
        raise HTTPException(status_code=400,detail="Invalid otp")
    
    data={'is_verified':True}
    update_contact(cleaned_data,data) 
    delete_otp(cleaned_data)
    return {"message": "OTP verified successfully"}


@app.post("/forget_password/password/{contact}/{password}/{confirm_password}",response_model=Response)
async def create_password(
    contact: str = Path(..., description="Enter a valid email or phone number (include country code)"),
    password: str = Path(..., min_length=8, description="Enter the password"),
    confirm_password: str = Path(..., min_length=8, description="Confirm the password")
):
    """
    API to create the password when forgot password
    """
    try:
        
        
        # Clean and fetch data
        cleaned_data = contact.strip()
        stored_data = fetch_contact(cleaned_data)
        
        # Validation 
        if not stored_data:
            raise HTTPException(status_code=400, detail="UserId not found")
        
        if stored_data.get("is_verified") != True:
            raise HTTPException(status_code=400, detail="Account is not verified")
        
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Password do not match")
        
        # Update the password
        code = {"password": password}
        update_contact(cleaned_data, code)
        
        return {"message": "Password created successfully"}
    except Exception as e:
        print("Unexpected error:", str(e))
        raise e