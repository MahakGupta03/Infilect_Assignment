from typing import List
from fastapi import FastAPI, HTTPException, Body
from fastapi.concurrency import iterate_in_threadpool
from datetime import datetime
from sqlalchemy import DateTime, create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
    
def largest_rectangle(matrix: List[List[int]]) -> tuple:
    if not matrix or not matrix[0]:
        raise ValueError("Invalid matrix input")

    rows = len(matrix)
    cols = len(matrix[0])
    maxArea = 0
    result_number = None
    height = [[0] * cols for _ in range(rows)]
    left = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        col = len(matrix[i])
        for j in range(col):
            if i > 0 and matrix[i][j] == matrix[i - 1][j]:
                height[i][j] = height[i - 1][j] + 1
            else:
                height[i][j] = 1

            if j > 0 and matrix[i][j] == matrix[i][j - 1]:
                left[i][j] = left[i][j - 1] + 1
            else:
                left[i][j] = 1

            width = left[i][j]
            for h in range(height[i][j], 0, -1):
                width = min(width, left[i - h + 1][j])
                if width!=h:
                    area = width * h
                    if area > maxArea:
                        maxArea = area
                        result_number = matrix[i][j]

    return result_number, maxArea


# Define your SQLAlchemy model

class Rectangle(Base):
    __tablename__ = "rectangle"

    id = Column(Integer, primary_key=True, index=True)
    matrix = Column(String)
    result_number = Column(Integer)
    max_area = Column(Integer)
    request_time = Column(DateTime)
    response_time = Column(DateTime)
    turnaround_time = Column(Float)

app = FastAPI()

# Connect to SQLite database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@app.post("/largest_rectangle")
def find_largest_rectangle(body = Body()):
    try:
        matrix = body.get('matrix')
        result = largest_rectangle(matrix)

        start_time = datetime.utcnow()
        end_time = datetime.utcnow()

        db = SessionLocal()
        db_rectangle = Rectangle(
            matrix=str(matrix),
            result_number=result[0],
            max_area=result[1],
            request_time=start_time,
            response_time=end_time,
            turnaround_time=(end_time - start_time).total_seconds(),
        )
        db.add(db_rectangle)
        db.commit()
        db.close()

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



