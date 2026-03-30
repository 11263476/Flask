# 🎓 Viva Preparation Guide (Cheat Sheet)

This project is much more advanced than a standard Flask app. Use this guide to explain **WHY** you chose these technologies!

---

### **1. Core Advanced Technologies**

| Technology | Why is it used? (Examiner Explanation) |
| :--- | :--- |
| **JWT (JSON Web Token)** | To handle **Stateless Authentication**. Unlike standard sessions, we don't store "Login Info" on the server. The token is a signed piece of data that the browser carries in a **Secure Cookie**. |
| **Bcrypt Hashing** | To protect user passwords. Even if an attacker steals the `students.db`, the passwords are not readable (they are scrambled into a hash). |
| **Asynchronous DB (aiosqlite)** | To prevent the server from "Freezing" during heavy database work. It allows the server to handle other users while waiting for a database response. |
| **Pydantic V2** | For **Strong Data Validation**. It ensures that "Age" is actually a number and "Email" is a real address before it ever touches the database. |

---

### **2. Potential Examiner Q&A**

**Q: Why use Cookies for JWT instead of LocalStorage?**
> "By using **HttpOnly Cookies**, we gain a huge security boost. LocalStorage can be stolen by malicious JavaScript (XSS attacks), but HttpOnly cookies are invisible to JavaScript."

**Q: Why does the Admin have an email if they login with a Username?**
> "In a professional production system, every User record must be complete and identifiable. We use the email for unique identification and potential password recovery in the future. I enforced this at the database level (`nullable=False`) to ensure Data Integrity across the entire system."

**Q: What is the benefit of the 'Service Layer' (app/services)?**
> "I used a Service Layer to separate the **Business Logic** from the **Routes**. The Routes only handle web requests, while the Services handle the actual data work. This makes the code much easier to test and maintain."

**Q: How does the 'Search' functionality work?**
> "It uses a dynamic SQL `LIKE` query. It checks both the 'Name' and 'Course' columns simultaneously using the `%` wildcard to provide real-time filtering results."

**Q: What is RBAC in your project?**
> "I implemented **Role-Based Access Control**. The app checks if the `is_admin` claim in the JWT is `True`. If not, it blocks the user from reaching the 'Manage Users' or 'Delete' routes using a custom `@admin_required` decorator."

---

### **3. The "WOW" Factors to point out:**
1.  **Dark Mode Persistence**: "The app remembers your theme choice using `localStorage` in the browser."
2.  **Global UI Context**: "I used `@app.context_processor` in `main.py` so that every page knows whether the user is logged in automatically."

### **4. How to show the project?**
1.  Open the website.
2.  Switch to **Dark Mode** first (it looks more professional!).
3.  Login as **Admin** to show the hidden features (Export CSV, Manage Users).
4.  Show a "Search" to demonstrate how fast it is.
