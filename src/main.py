from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from src.scrapers.realu_lt import Realu_Lt
from src.db.database import get_db, engine
from src.db.models import FlatScraped, FlatForPrediction
from src import schemas
import pandas as pd


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the flat price predicting app!"}


@app.get("/realu_lt")
def write_scraped_data_to_db(db: Session = Depends(get_db)):
    realu_lt: Realu_Lt = Realu_Lt()
    flats = realu_lt.scrape(flats_count=1400, keyword="flat")
    for flat in flats:
        new_flat = FlatScraped(**flat.dict())
        print(new_flat)
        db.add(new_flat)
        db.commit()

    return {"message": "Writing operation sccuessfull!"}


@app.get("/flats")
def get_flats_from_db():
    flats_df = pd.read_sql_table("scraped_flats", con=engine)
    flats_df.to_csv("flat_data.csv")
    return {"message": "Data was successfully written to .csv file"}


@app.post("/", status_code=status.HTTP_201_CREATED)
def write_flats_data_for_prediction(flat: schemas.FlatCreate, db: Session = Depends(get_db)):
    new_flat = FlatForPrediction(**flat.dict())
    db.add(new_flat)
    db.commit()
    db.refresh(new_flat)

    return {new_flat}
