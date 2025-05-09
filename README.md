# cmsi662_webbank

A banking app for CMSI 662/5999 Homework #5

## About

This is a Python banking application for the storage and exchange of LEGO. This is the perfect app for LEGO builders who need a secure way to store their bricks.

_Did you know? 40 billion LEGO bricks stacked together would reach the moon_

![a lego chest](static/img/lego_chest.jpg)

## Security

This web app takes the security of its users very seriously. The following details the security measures taken to protect user data and prevent unauthorized access.

### XSS

All user input is sanitized and escaped before being displayed on the page. This prevents malicious users from injecting scripts into the app.

### CSRF

All forms in the app include a CSRF token that is verified on the server side. This prevents malicious users from submitting forms on behalf of other users.

### SQL Injection

All user input is sanitized and parameterized queries are used to prevent malicious users from injecting SQL code into the app.

### User Enumeration

The app does not reveal whether a username or password is incorrect. Instead, it simply returns a generic error message. Additionally, the login response time is the same regardless of whether the username or password is correct.

The app does not allow users to view other users' account details. If a user tries to access an account they do not own, they will be redirected to their own account page with an error message that does not disclose sensitive information about the account they tried to access.

_Did you know? Two eight-stud bricks can be combined 24 ways_

---

Lego facts are provided by the [Legoland Discovery Center](https://www.legolanddiscoverycenter.com/michigan/post/lego-facts/)
