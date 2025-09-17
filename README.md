# 🎟️ Online Ticket System

A web-based platform for purchasing tickets to Māori cultural events, with support for multilingual interfaces and basic flight booking simulation.  
This project was developed as part of the **MSE800 Software Engineering** course at Yoobee Colleges.

## 📖 Project Overview

The **Online Ticket System** was designed to promote cultural inclusiveness by providing an accessible platform where users can:

- Browse Māori cultural events
- Purchase event tickets online
- Book flights (simulation)
- Learn about Māori culture via a dedicated introduction page

Special attention was given to the **principles of Te Tiriti o Waitangi (Treaty of Waitangi)**:

- **Partnership** → multilingual support (English, Māori, Chinese)
- **Protection** → accurate presentation of cultural information & user data privacy
- **Participation** → simplified ticket purchase to encourage cultural engagement

## ✨ Features (Completed)

- 🔑 User registration & login
- 🌐 Multilingual support (English, Māori, Chinese)
- 🎭 Event browsing, details view, and ticket purchase
- ✈️ Flight search and booking (demo only, no real API)
- 📦 Order management (events & flights)
- 📚 Māori culture introduction page
- 💳 Simulated payment workflow (demonstration only)

## 🏗️ System Design

- **Frontend**: HTML, CSS, JavaScript (responsive layout, dynamic text replacement)
- **Backend**: Python [Flask](https://flask.palletsprojects.com/)
- **Database**: MySQL
- **Architecture**:
  - Browser (UI) → Flask (business logic, RESTful APIs) → MySQL (persistent data)

### Database Models

- **User** (authentication, bookings)
- **Event** (cultural event info, tickets)
- **Flight** (flight schedules, seat pricing)
- **Booking** (event & flight orders)

## 🔄 Development Process

- **Agile iterations** with incremental delivery:
  1. User login/registration
  2. Event browsing & ticketing
  3. Flight booking simulation
  4. Order management
  5. Multilingual support
  6. Māori culture introduction page
- **Version control**: Git & GitHub
- **Daily self-review & task tracking** using Notion
- **Testing**:
  - Unit, integration, system, and user acceptance
  - Coverage includes login, ticketing, multilingual switching, and abnormal input handling

## 🧪 Testing

- Verified login and registration flows
- Tested multilingual interface switching
- Pagination for events & flights optimized with `LIMIT` and `OFFSET`
- Simulated payment process tested for workflow consistency

## 🚧 Challenges & Solutions

- **CSS & layout** → learned Grid/Flexbox for responsive UI
- **JavaScript async & i18n** → implemented dynamic text replacement and AJAX pagination
- **Database performance** → optimized queries using `LIMIT` & `OFFSET`
- **Cultural integration** → consulted resources to ensure respectful representation

## ⚠️ Current Limitations

- Payment function is simulation only (no real gateway)
- Tested locally only (not deployed online)
- Basic password security, lacks 2FA / advanced authentication

## 🚀 Future Improvements

- Integrate real payment gateways (Stripe, PayPal)
- Deploy on cloud servers for scalability
- Add advanced authentication (e.g. 2FA)
- Expand event types and add user reviews
- Enable social sharing of events

## 🖥️ Development Environment

- macOS
- Python 3.12.7, Flask 3.0.3, Werkzeug 3.0.4
- MySQL
- VS Code

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [JavaScript MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 👤 Author

**Yongfu Lin**  
MSE800 Software Engineering – Yoobee Colleges (2024)
