# import packages
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import pandas as pd

# create FastAPI object
app = FastAPI()

password = "12345"


class Profile(BaseModel):
    '''
    Profile class - used for making request body
    '''
    name: str
    location: str


@app.get('/')
def getHome():
    '''
    endpoint 1 - home page
    '''

    return {
        "msg": "Hello world!"
    }


@app.get('/profiles')
def getProfiles():
    '''
    endpoint 2 - get all profiles
    '''

    # complete this endpoint
    df = pd.read_csv('dataset.csv')

    if len(df) == 0:
        raise HTTPException(status_code = 404, detail="Data not Found!")
    #Tidak Else Karena Setelah Raise Maka Code Bawah Tidak Dilihat
    return{
        "Data": df.to_dict(orient= 'records')
    }  


@app.get('/profiles/{id}')
def getProfile(id: int):
    '''
    endpoint 3 - get profile by id
    '''

    # complete this endpoint
    df = pd.read_csv('dataset.csv')
    result = df.query(f"id == {id}")

    return {
        "Data": result.to_dict(orient= 'records')
    }


@app.delete('/profiles/{id}')
def deleteProfile(id: int, api_key: str = Header(None)):
    '''
    endpoint 4 - delete profile by id
    '''
    if(api_key == None) or (api_key != password):
        raise HTTPException(status_code = 401, detail="Unauthorized Access!")

    df = pd.read_csv('dataset.csv')
    result = df[df.id != id]
    result.to_csv('dataset.csv', index = False)

    return {
        "Data": result.to_dict(orient= 'records')
    }
    


@app.put('/profiles/{id}')
def updateProfile(id: int, profile: Profile):
    '''
    endpoint 5 - update profile by id
    '''

    # complete this endpoint
    pass


@app.post('/profiles')
def createProfile(profile: Profile):
    '''
    endpoint 6 - create new profile
    '''

    # complete this endpoint
    df = pd.read_csv('dataset.csv')
    new = pd.DataFrame({
        "id": [len(df) + 1],
        "name": [profile.name],
        "location": [profile.location]
    })

    df = pd.concat([df, new])

    df.to_csv('dataset.csv', index = False)

    return {
        "msg": "Data Berhasil Di Create"
    }
