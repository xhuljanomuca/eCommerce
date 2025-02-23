# 🛒 eCommerce Django Application

## 📌 Overview
This is a full-featured **eCommerce platform** built with **Django**. The project supports **user authentication, product management, cart functionality, payments, and order tracking**. It allows sellers to list products and buyers to purchase them securely.

## ✨ Features
- 🔐 **User Authentication:** Register, login, logout, and profile management.
- 🏪 **Product Management:** Add, edit, and categorize products.
- 📷 **Image Uploads:** Supports product image.
- 🛍 **Cart & Checkout:** Add to cart, adjust quantity, and proceed to checkout.
- 💳 **Payments:** Simulated payment system with user wallet.
- 📦 **Order Management:** Tracks orders and seller earnings.
- 📂 **Media Handling:** Stores product images under `media/photos/`.

---

## ⚙️ Installation & Setup
### **1️⃣ Clone the Repository**
```
git clone https://github.com/xhuljanomuca/eCommerce.git
cd eCommerce
```

2️⃣ Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies

```
pip install -r requirements.txt
```
4️⃣ Configure the Database

```
python manage.py makemigrations
python manage.py migrate
```

5️⃣ Run the Development Server

```
python manage.py runserver
```

Access the application at http://127.0.0.1:8000/





