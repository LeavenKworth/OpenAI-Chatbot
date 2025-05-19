from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_GATEWAY = os.getenv("APIGATEWAY_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = Flask(__name__)

token = ""

def login(text: str) -> str:
    global token
    try:
        username_match = re.search(r'username[: ]+(\w+)', text, re.IGNORECASE)
        password_match = re.search(r'password[: ]+(\w+)', text, re.IGNORECASE)

        if not username_match or not password_match:
            return "Please provide login like: 'Login with username: <username> password: <password>'"

        username = username_match.group(1)
        password = password_match.group(1)

        res = requests.post(
            f"{API_GATEWAY}/auth/login",
            json={"username": username,
                  "password": password}
        )

        if res.status_code == 200:
            token = res.json()["token"]

            return f"Login successful. Token: {token}"
        else:
            return f"Login failed: {res.status_code} - {res.text}"

    except Exception as e:
        return f"Error during login: {e}"

def add_flight(input_str: str) -> str:
    try:
        global token
        # input_str example: "N1, Istanbul, Izmır, 2025-05-18T17:37:06.561Z, 2025-05-18T17:37:06.561Z, 60, 100"
        parts = input_str.split(",")

        if len(parts) < 7:
            return "Invalid input format. Expected: flightNumber, airportFrom, airportTo, dateFrom, dateTo, duration, capacity"

        flightNumber = parts[0].strip()
        airportFrom = parts[1].strip()
        airportTo = parts[2].strip()
        dateFrom = parts[3].strip()
        dateTo = parts[4].strip()
        duration = int(parts[5].strip())
        capacity = int(parts[6].strip())

        payload = {
            "flightNumber": flightNumber,
            "airportFrom": airportFrom,
            "airportTo": airportTo,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "duration": duration,
            "capacity": capacity
        }

        response = requests.post(
            f"{API_GATEWAY}/flights/add",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        return response.text
    except Exception as e:
        return f"Add flight error: {str(e)}"



def query_flight(input_str: str) -> str:
    try:
        global token
        # input_str example:
        # "Istanbul, Izmır, 2025-05-18T17:37:06.561Z, 2025-05-18T17:37:06.561Z, 1, true"
        parts = input_str.split(",")

        if len(parts) < 6:
            return "Invalid input. Format: airportFrom, airportTo, dateFrom, dateTo, numberOfPeople, oneWay (e.g., true/false)"

        airportFrom = parts[0].strip()
        airportTo = parts[1].strip()
        dateFrom = parts[2].strip()
        dateTo = parts[3].strip()
        numberOfPeople = int(parts[4].strip())
        oneWay = parts[5].strip().lower() == "true"

        payload = {
            "airportFrom": airportFrom,
            "airportTo": airportTo,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "numberOfPeople": numberOfPeople,
            "oneWay": oneWay
        }

        response = requests.post(
            f"{API_GATEWAY}/flights/query?page=0&size=10",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        return response.text
    except Exception as e:
        return f"Flight query error: {str(e)}"


def buy_ticket(input_str: str) -> str:
    try:
        global token
        parts = input_str.split(",")

        if len(parts) < 3:
            return "Invalid input. Format: flightNumber, date, passengerName"

        flightNumber = parts[0].strip()
        date = parts[1].strip()
        passengerName = parts[2].strip()

        payload = {
            "flightNumber": flightNumber,
            "date": date,
            "passengerNames": [passengerName]
        }

        response = requests.post(
            f"{API_GATEWAY}/tickets/buy",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        return response.text
    except Exception as e:
        return f"Ticket buying error: {str(e)}"


def check_in(input_str: str) -> str:
    try:
        global token
        parts = input_str.split(",")

        if len(parts) < 3:
            return "Invalid input. Format: flightNumber, date, passengerName"

        flightNumber = parts[0].strip()
        date = parts[1].strip()
        passengerName = parts[2].strip()

        payload = {
            "flightNumber": flightNumber,
            "date": date,
            "passengerName": passengerName
        }

        response = requests.post(
            f"{API_GATEWAY}/tickets/check-in",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        return response.text
    except Exception as e:
        return f"Check-in error: {str(e)}"


def passenger_list(input_str: str) -> str:
    try:
        global token
        parts = input_str.split(",")

        if len(parts) < 2:
            return "Invalid input. Format: flightNumber, date"

        flightNumber = parts[0].strip()
        date = parts[1].strip()

        response = requests.get(
            f"{API_GATEWAY}/tickets/passenger-list",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "flightNumber": flightNumber,
                "date": date,
                "page": 0,
                "size": 10
            }
        )
        return response.text
    except Exception as e:
        return f"Passenger list query error: {str(e)}"


tools = [
    Tool(
        name="Login",
        func=login,
        description="Use this to log in when user want to login with his/her username and password"
                    "when user input includes username and password use this tool"
                    ". Input format: Login with username: <username> password: <password>"

    ),
    Tool(
        name="AddFlight",
        func=add_flight,
        description="Use this to add a flight. Input format: flightNumber, airportFrom, airportTo, dateFrom, dateTo, duration, capacity (e.g., N1, Istanbul, Izmir, 2025-05-18T17:00:00Z, 2025-05-18T19:00:00Z, 60, 100)"
    ),
    Tool(
        name="QueryFlight",
        func=query_flight,
        description="Use this to query a flight. Input format: airportFrom, airportTo, dateFrom, dateTo, numberOfPeople, oneWay (e.g., Istanbul, Ankara, 2025-05-20T10:00:00Z, 2025-05-22T18:00:00Z, 1, true)"
    ),
    Tool(
        name="BuyTicket",
        func=buy_ticket,
        description="Use this to buy a ticket. Input format: flightNumber, date, passengerName (e.g., N5, 2025-05-20T10:00:00Z, Serkan Acar)"
    ),
    Tool(
        name="CheckIn",
        func=check_in,
        description="Use this to check in to a flight. Input format: flightNumber, date, passengerName (e.g., N5, 2025-05-20T10:00:00Z, Serkan Acar)"
    ),
    Tool(
        name="PassengerList",
        func=passenger_list,
        description="Use this to get the passenger list for a flight. Input format: flightNumber, date (e.g., N5, 2025-05-20T10:00:00Z)"
    )
]


llm = ChatOpenAI(temperature=0, model="gpt-4")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"response": "Please provide a message."})

    try:
        result = agent.invoke(user_message)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(port=8000)
