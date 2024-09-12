# Flask-eComm-App

A simple e-commerce web app made using Flask and Flask Extensions. The app allows users to browse products, manage their cart and wishlist, place orders, and provide reviews for purchased products. The app also features an admin panel for managing users, orders, and products.

## Features

- User authentication (sign up, login, logout)
- Browse products and search functionality
- Pagination for products
- View reviews for products by other users
- Add products to cart and wishlist
- Place orders and view past orders
- Write reviews for purchased products
- Admin panel for managing users, products, and orders
- Admin functionalities for editing and adding database details
- Tailwind CSS for responsive styling
- PostgreSQL/SQLite database support

## Live Version

You can check out the live version of the Flask-eComm-App here:

[Live Demo](https://krisht16.pythonanywhere.com/)

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite/PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: Tailwind CSS
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF
- **Admin Interface**: Flask-Admin
- **Password Hashing**: Flask-Bcrypt

## Installation

### Prerequisites
- Python 3.x installed on your system

### Clone the Repository
```bash
git clone https://github.com/mahakal/Flask-eComm-App.git
cd flask-ecomm-app
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Environment Variables
Create a .env file in the project's root directory with the following contents:
```bash
DATABASE_URI=sqlite:////absolute_path_to_db/db.sqlite3
FLASK_APP=manager.py
FLASK_DEBUG=1
FLASK_ENV=development
SECRET_KEY=dev
```

### Initialize the Database
```bash
flask --app manager.py init-db
```

### Run the App
```bash
flask --app manager.py run
```

Your app should now be running at http://127.0.0.1:5000/.


## License
This project is licensed under the MIT License.
