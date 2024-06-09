Sure, here's the `README.md` file in English:

```markdown
# RediShop

RediShop is a web application for managing an online store, developed using FastAPI for the backend and Jinja2 for template rendering.

## Project Structure

```
backend/
    ├── app/
    │   ├── api/
    │   │   ├── auth.py
    │   │   ├── products.py
    │   │   ├── user.py
    │   │   └── cart.py
    │   ├── database/
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   └── crud.py
    │   ├── routers/
    │   │   └── main_routes.py
    │   ├── services/
    │   │   └── product_service.py
    │   ├── utils/
    │   │   └── auth.py
    │   ├── schemas/
    │   │   └── schemas.py
    │   ├── main.py
frontend/
    ├── static/
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── register.html
    │   └── user_profile.html
```

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/RediShop.git
cd RediShop
```

### Step 2: Create and Activate a Virtual Environment

#### For Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### For Unix/MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database

Run the following command to initialize the database:

```bash
uvicorn backend.app.main:app --reload
```

### Step 5: Start the Application

```bash
uvicorn backend.app.main:app --reload
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Main Routes

- `/` - Home Page
- `/register` - User Registration
- `/login` - User Login
- `/profile` - User Profile

## File Structure

### backend/app/main.py

The main application file containing settings and route inclusion.

### backend/app/api/

Contains modules for handling various routes such as authentication, products, users, and cart.

### backend/app/database/

Contains database configurations, models, and CRUD operations.

### backend/app/routers/main_routes.py

Contains the main routes of the application, such as registration, login, profile, and the root page.

### backend/app/services/

Contains the business logic of the application, such as product operations.

### backend/app/utils/

Contains utility modules, such as authentication.

### backend/app/schemas/

Contains data schemas for validation and serialization.

### frontend/static/

Contains static files such as CSS, JavaScript, and images.

### frontend/templates/

Contains HTML templates for rendering pages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This `README.md` file describes the main aspects of your project, including the project structure, installation and setup instructions, as well as the main routes and their purposes. You can further customize it to include additional details if needed.
