# Expense Tracker

A simple application to track expenses between 2 users.

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

---

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
| /owed/<payee>/<payer> | GET    | Returns how much <payee> owes to <payer>   |

---

## Sample Requests & Responses

### Balance Enquiry

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

### Amount Owed Enquiry

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

### Error Example

```
GET /balance/UnknownUser
```

Response:

```json
{
  "error": "Invalid user"
}
```

---

## Testing the Endpoints

You can test the API endpoints using `curl` commands or with tools like Postman. Below are sample `curl` commands for each endpoint:

- **Get Both Users’ Transactions and Balances**

  ```
  curl -X GET http://localhost:5000/users
  ```

- **Record a Bill Payment**

  ```
  curl -X POST http://localhost:5000/transactions \
    -H "Content-Type: application/json" \
    -d '{"payer": "A", "payee": "B", "total_amount": 100, "description": "Dinner"}'
  ```

- **List All Past Transactions**

  ```
  curl -X GET http://localhost:5000/transactions
  ```

- **Settle Outstanding Balance**

  ```
  curl -X POST http://localhost:5000/settle \
    -H "Content-Type: application/json" \
    -d '{"payer": "A", "payee": "B", "amount": 50}'
  ```

- **Enquire Individual User Balance**

  ```
  curl -X GET http://localhost:5000/balance/A
  ```

- **Check How Much One User Owes Another**

  ```
  curl -X GET http://localhost:5000/owed/A/B
  ```

You can also use Postman to send requests and view responses interactively.

---

## Edge Cases & Limitations

The following potential edge cases and limitations could be handled in the future:

- Negative or zero amounts: Endpoints should validate that amounts are positive and non-zero.
- Non-existent users: Ensure all user references are valid to prevent errors.
- Self-payment: Prevent users from paying or settling with themselves.
- Insufficient balance: Only the payer’s balance is checked; payee’s balance may also need validation.
- Malformed requests: Validate all required fields and data types in incoming requests.
- Division by zero: If the number of users or splits changes, fair share calculations could fail.
- Transaction history overflow: No limit on transaction history size; could grow indefinitely.
- Data type issues: Amounts and balances should be validated as numbers, not strings.
- Security: No authentication or authorization checks are currently implemented.

---

## Feature Ideas

Here are some ideas for future improvements:

- Add user authentication and registration
- Support multiple currencies
- Add expense categories and analytics
- Export transactions to CSV or PDF
- Add notifications for settlements or payments
- Mobile app integration
- Group expense tracking (for more than two users)
- Dashboard with charts and summaries

## How to Implement Feature Ideas

1. **User Authentication and Registration**

   - Integrate Flask-Login or similar authentication library
   - Add endpoints for user signup, login, and logout
   - Store user credentials securely (e.g., hashed passwords)

2. **Support Multiple Currencies**

   - Add a currency field to user and transaction models
   - Use a currency conversion API for calculations
   - Update endpoints to handle currency selection

3. **Expense Categories and Analytics**

   - Add a category field to transactions
   - Create endpoints to filter and summarize by category
   - Use charting libraries (e.g., Chart.js) for analytics dashboard

4. **Export Transactions**

   - Add endpoints to export data in CSV or PDF format
   - Use libraries like pandas (CSV) or ReportLab (PDF)

5. **Notifications**

   - Integrate email or push notification services
   - Trigger notifications on settlement or payment events

6. **Group Expense Tracking**

   - Update data models to support multiple users per transaction
   - Add endpoints for group creation and management
   - Implement algorithms to split expenses among groups, especially different splits

7. **Dashboard with Charts**

   - Build a frontend dashboard using a JS framework (React, Vue)
   - Integrate charting libraries for visual summaries

8. **Add budget balances**
   - Allow each user to top up their balances

---

## Design Decisions

- **RESTful API Structure:** Endpoints follow REST principles, making them predictable and easy to consume with standard tools (curl, Postman, etc.).
- **Modular Codebase:** Logic is separated into controllers, routes, and data modules to improve maintainability and allow for easier future expansion (e.g., adding new features or endpoints).
- **Extensibility:** The code and API are structured so that new features (like group expenses, authentication, analytics) can be added with minimal refactoring.
- **Error Handling:** Basic error checks are included for user existence and balance, with clear error messages returned to the client. More robust validation and security can be added as needed.
