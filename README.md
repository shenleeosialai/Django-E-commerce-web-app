# OSHEN COMICS  
_Your One-Stop Comic Book & Merchandise Store_

OSHEN COMICS is a feature-rich e-commerce platform designed for comic book fans. It allows users to browse, shop, and pay for comic books and related merchandise using M-Pesa and Stripe payment methods. It supports intelligent product recommendations, promotional tools like coupon codes and countdown deals, and efficient cart handling with Redis-backed sessions.

![FireShot Capture 001 - Products - oshenproject com](https://github.com/user-attachments/assets/01f0b4df-2a0a-4aea-a600-d8b9a276bc03)

## Features


- **Comic & Merchandise Catalog**  
  Browse a collection of comic books and fan merchandise.

- **User Authentication** (working on this) 
  Register, login, and manage profiles securely.

- **Cart System with Redis**  
  Fast, scalable session management for shopping carts.

- **Payments**  
  - **M-Pesa**: Seamless mobile payments for Kenyan users.  
  - **Stripe**: Secure international credit/debit card support.

- **Promotional Tools**  
  - Coupon code discounts  
  - Countdown deals via a custom API

- **Recommendation Engine**  
  Personalized product suggestions based on user behavior.

- **Admin Panel**  
  Product, user, and order management via Django admin.

- **Asynchronous Tasks with Celery**  
  For email notifications, background processing, etc.

- **Dockerized Deployment**  
  Easily run the project locally or in production via Docker.



## Tech Stack

- **Backend**: Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: PostgreSQL  
- **Task Queue**: Celery  
- **Broker**: Redis  
- **Caching & Session Storage**: Redis  
- **Payments**: M-Pesa API, Stripe API  
- **Deployment**: Docker & Docker Compose  

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shenleeosialai/Django-E-commerce-web-app.git
cd oshen-comics

Build with Docker
bash

docker-compose up --build

Install Python Dependencies
bash
docker-compose exec web pip install -r requirements.txt

Run Migrations & Create Superuser
bash

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

CREATED BY SHEN LEE OSIALAI
FOLLOW MY GITHUB ❤
