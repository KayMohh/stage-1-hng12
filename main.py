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
    return n > 0 and n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return n == sum(d ** power for d in digits)

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}", timeout=1)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        return "Fun fact unavailable."
    return "Fun fact unavailable."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/classify-number")
def classify_number(number: str = Query(None, description="The number to classify")):
    if number is None or not number.lstrip('-').isdigit():
        return {"error": True, "number": number}
    
    number = int(number)
    properties = []
    
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    
    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return result
