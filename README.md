# 📘 Periplus Cart Functionality Testing

## 📌 Overview
This project demonstrates **manual and automation testing** for the *Periplus web application*, focusing on core user flows such as:

- User login
- Product search
- Add to cart
- Remove from cart

The objective is to ensure that the system behaves correctly, consistently, and meets functional requirements from an end-user perspective.

---

## 🧪 Test Scope

The testing includes the following scenarios:

1. **User Login**
   - Verify successful login using valid credentials
   - Ensure correct redirection after login

2. **Search & Add to Cart**
   - Search for available products
   - Select a product from search results
   - Add product to cart
   - Validate product details in the cart

3. **Remove from Cart**
   - Remove item from cart
   - Ensure item is no longer displayed in the cart

---

## 🛠️ Testing Type

- Functional Testing  
- Manual Testing  
- Basic Automation Testing  

---

## ⚙️ Test Environment

| Item        | Details                          |
|------------|----------------------------------|
| OS         | macOS                            |
| Browser    | Chrome (Latest Version)          |
| Tester     | Alisha                           |
| Test Date  | March 20, 2026                   |
| Framework  | Selenium with Python (unittest)  |

---

## 📂 Test Cases

### ✅ TC-01: Login Functionality
**Objective:**  
Verify that a registered user can log in successfully using valid credentials.

**Preconditions:**
- User already has a registered account
- Login page is accessible
- Stable internet connection

**Test Steps:**
1. Open browser and access login page  
2. Enter valid email  
3. Enter valid password  
4. Click Login  

**Expected Result:**
- Login is successful  
- User is redirected to homepage  

---

### ✅ TC-02: Search and Add to Cart
**Objective:**  
Verify that a user can search for a product, add it to cart, and view correct product details.

**Preconditions:**
- User is logged in  
- Product is available in stock  

**Test Steps:**
1. Enter product keyword in search bar  
2. Select product from results  
3. Click "Add to Cart"  
4. Open cart page  
5. Verify product in cart  

**Expected Result:**
- Search results are relevant  
- Product detail page opens correctly  
- Product is added to cart  
- Cart displays correct product name, quantity, and price  

---

### ✅ TC-03: Remove Product from Cart
**Objective:**  
Verify that a user can remove a product from the cart successfully.

**Preconditions:**
- User is logged in  
- Cart contains at least one product  

**Test Steps:**
1. Navigate to cart page  
2. Click "Remove" on a product  

**Expected Result:**
- Product is removed from cart  
- Product no longer appears in cart  

---

## 📎 Documentation

Test execution evidence (screen recordings):

- TC-01: https://docs.google.com/...
- TC-02: https://docs.google.com/...
- TC-03: https://docs.google.com/...

---

## 🔗 Repository Structure
