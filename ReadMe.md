# I4 Lab Storehouse 

## Overview

This project aims to streamline the processes within a university lab's storehouse. It enables students to request parts for lab experiments, manage product inventory, and track the borrowing and retrieval of items. The system consists of a **backend** built with **Django Rest Framework** and a **frontend** built with **React** using **Vite** for fast development.

### Key Features

- **Product Management**: Manage products, categories, and parts in the inventory.
- **Request System**: Students can submit part requests through the frontend.
- **Approval Workflow**: Professors can approve or reject student requests via the Django admin.
- **Test & Borrow**: Parts can be tested before borrowing and tracked for retrieval.
- **Admin Dashboard**: A custom admin interface for managing the system, including viewing requests, approving/rejecting them, and assigning parts to requests.

## Project Structure

- **Backend**: A Django app that provides APIs to interact with products, requests, and users.
- **Frontend**: A React app for students and professors to interact with the system, submit requests, and manage inventory.

## Technologies

- **Backend**:
  - Django
  - Django Rest Framework
  - MySQL
  - Django Admin

- **Frontend**:
  - React
  - Vite
  - Axios for API calls

## Setup Instructions

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Node.js and npm/yarn

### 1. Clone the repository

```bash
git clone <repository-url>
cd storehouse
```

### 2. Set up the backend

#### Install Python dependencies

Create and activate a virtual environment (recommended):

```bash
python3 -m venv env
source ./env/bin/activate
```

Then, navigate to the backend directory and install the necessary dependencies.

#### Install backend dependencies

In the backend, make sure you have the following installed:

```
corsheaders
djangorestframework
```

#### Set up the database

Ensure you have MySQL installed, then configure your `settings.py` to connect to your MySQL database. Afterward, run the migrations:

```bash
python manage.py migrate
```

#### Running the backend

Start the Django development server:

```bash
python manage.py runserver
```

The backend should now be running at `http://127.0.0.1:8000/`.

### 3. Set up the frontend

#### Install frontend dependencies

Navigate to the frontend directory and install the required dependencies:

```bash
cd ../storehouse-frontend
yarn install
```

#### Running the frontend

Start the Vite development server:

```bash
npm run dev
```

The frontend should now be running at `http://127.0.0.1:3000/`.

## How to Use

- **Students**: 
  - Enter your student number and choose a professor.
  - Browse and select the products you need.
  - Add products to the cart and submit a request.
  
- **Admin**: 
  - Approve or reject student requests in the Django admin dashboard.
  - Assign parts and perform tests through the admin interface.

## Admin Dashboard

You can access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage students, professors, products, requests, and more. Make sure to create a superuser:

```bash
python manage.py createsuperuser
```