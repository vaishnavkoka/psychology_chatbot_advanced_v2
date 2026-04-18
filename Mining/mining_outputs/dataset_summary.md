# GitHub Gherkin Requirements Dataset

**Total Scenarios:** 4
**Projects:** 3
**Languages:** JavaScript, Python
**Domains:** authentication, api, dashboard, checkout

## 1. Successful login with valid credentials

**Project:** cucumber-js (JavaScript)
**Feature:** User Authentication
**Domain:** authentication

### Business Context
The user is using the authentication service. The business requires secure access, clear feedback on auth failures, and audit trails for compliance.

### Gherkin Scenario
- **Given:** A user has registered with valid credentials in the system
- **When:** The user enters their username and password on login page and clicks Login
- **Then:** The system should authenticate the user and redirect to dashboard

### Acceptance Criteria
- User receives success message
- User session is created with secure token
- User is redirected to dashboard within 2 seconds
- Login attempt is logged for audit

## 2. API returns 429 when rate limit exceeded

**Project:** cucumber-js (JavaScript)
**Feature:** API Rate Limiting
**Domain:** api

### Business Context
The user is using the API. The system needs rate limiting, error handling with clear messages, and stock/inventory constraints.

### Gherkin Scenario
- **Given:** A client has sent the maximum allowed requests in the window
- **When:** The client sends one more request
- **Then:** The system should return 429 status and Retry-After header

### Acceptance Criteria
- Response HTTP status is 429
- Retry-After header indicates wait time
- Client IP is logged for security
- Rate limit counter resets after window

## 3. Filter requirements by status

**Project:** behave (Python)
**Feature:** Dashboard Filters and Exports
**Domain:** dashboard

### Business Context
The user is using the dashboard. Business wants fast loading, accurate filtering, and clear feedback to complete analysis without unnecessary steps. Measurable outcomes and auditability required.

### Gherkin Scenario
- **Given:** The user is logged in and viewing the dashboard with requirements
- **When:** The user clicks the Status filter and selects 'In Progress'
- **Then:** The dashboard should display only In Progress requirements

### Acceptance Criteria
- Filter is applied within 1 second
- Only matching requirements are shown
- Filter badge indicates active filter
- Results count is accurate

## 4. Add to cart with stock constraints

**Project:** robotframework (Python)
**Feature:** Shopping Cart Management
**Domain:** checkout

### Business Context
The user is interacting with the system. Business requires clear feedback, accurate processing, and audit trails for all operations.

### Gherkin Scenario
- **Given:** A product with limited stock is displayed
- **When:** The user selects quantity and adds to cart
- **Then:** The system should add items and update stock

### Acceptance Criteria
- Cart quantity is updated
- Stock is decremented
- Insufficient stock error shown when needed
- User can proceed to checkout

