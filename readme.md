# Expense Tracker

A simple application to track your expenses.

## Features

- View both users’ transactions and balances
- Record bill payments (who paid, total amount)
- List all past transactions with payer and split details
- Settle outstanding balances between users
- Enquire individual user balances
- Check how much one user owes another

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/clement7903/expense_tracker.git
   ```
2. Install dependencies:
   ```
   cd expense_tracker
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```
2. Access the app via your browser or terminal as instructed.

## API Endpoints

### Required Endpoints

| Endpoint      | Method | Description                                        |
| ------------- | ------ | -------------------------------------------------- |
| /users        | GET    | Returns both users’ transactions and balances      |
| /transactions | POST   | Records a bill payment: who paid, total amount     |
| /transactions | GET    | Lists all past transactions with who paid & splits |
| /settle       | POST   | Allows a user to settle their outstanding balance  |

### Additional Endpoints

| Endpoint              | Method | Description                                |
| --------------------- | ------ | ------------------------------------------ |
| /balance/<username>   | GET    | Returns the balance for the specified user |
| /owed/<payer>/<payee> | GET    | Returns how much <payer> owes to <payee>   |

### Sample Requests & Responses for additional endpoints

**Balance Enquiry**

```
GET /balance/A
```

Response:

```json
{
  "username": "A",
  "balance": 500.0
}
```

**Amount Owed Enquiry**

```
GET /owed/A/B
```

Response:

```json
{
  "payer": "A",
  "payee": "B",
  "amount_owed": 0.0
}
```

**Error Example**

```
GET /balance/UnknownUser
```

Response:

```json
{
  "error": "Invalid user"
}
```