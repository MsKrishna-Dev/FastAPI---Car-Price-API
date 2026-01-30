# 🛒 FastAPI Product CRUD API (Learning Project)

This is a beginner-friendly **FastAPI backend project** built for learning purposes.  
It implements full **CRUD operations**, **dependency injection**, and **data persistence using a JSON file** instead of a database.

The project uses a sample dataset related to **hardware products** such as laptops, mobiles, PCs, etc.

---

## 🚀 Features

✅ FastAPI-based REST API  
✅ CRUD operations (Create, Read, Update, Delete)  
✅ Dependency Injection  
✅ Data stored in `products.json` file  
✅ Input validation using Pydantic models  
✅ API testing using Swagger UI  
✅ Beginner-friendly project structure  

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **Pydantic**

---

## 📂 Project Structure

```
FastAPI-CRUD-Products/
│
├── app/
│ ├── data/
│ │ ├── products.json
│ │ └── dummy.json
│ │
│ ├── schema/
│ │ └── product.py
│ │
│ ├── service/
│ │ └── products.py
│ │
│ ├── main.py
│ └── pycache/
│
├── requirements.txt
├── Swagger UI.png
├── README.md
└── venv/
```

---

## 📸 Screenshots

### 🔹 Swagger UI Interface
![Swagger UI](Swagger%20UI.png)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/MsKrishna-Dev/FastAPI-CRUD-Products.git
cd FastAPI-Product-CRUD
```

### 2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

---

### ▶️ Run the Server
uvicorn app.main:app --reload
Server will start at: http://127.0.0.1:8000

---

### 🧪 API Testing (Swagger UI)

Open in browser: http://127.0.0.1:8000/docs
You can test all endpoints directly from the UI without Postman.

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products |
| GET | `/products/{product_id}` | Get product by ID |
| POST | `/products` | Add a new product |
| PUT | `/products/{product_id}` | Update an existing product |
| DELETE | `/products/{product_id}` | Delete a product |

---

🎯 Learning Outcomes

- FastAPI routing and request handling
- CRUD API design
- JSON file persistence
- Dependency Injection
- Swagger UI testing
- Backend debugging

---

