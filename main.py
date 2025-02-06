from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import JSONResponse


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return n == sum(d ** power for d in digits)

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}")
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        return "Fun fact unavailable."
    return "Fun fact unavailable."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 
    allow_methods=["GET"],  #
    allow_headers=["*"],  # 
)

@app.get("/")
async def root():
    return {"message": "Welcome to my HNG Api"}


@app.get("/api/classify-number")
async def classify_number(number: str):
    if not number.isdigit():
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

    number = int(number)
    properties = []
    
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return JSONResponse(content=response)
    
@app.get("/api/classify-numbers")
def classify_number(number: int = Query(..., description="The number to classify")):
    properties = []
    
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")
    
    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return result
