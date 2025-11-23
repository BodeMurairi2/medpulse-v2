# MedPulse

![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

MedPulse is a secure, cloud-based platform designed to centralize and streamline patient medical records for hospitals, doctors, and patients in Eastern Africa.  
In a region where many health facilities still rely on paper-based records, MedPulse addresses inefficiencies, delays, and fragmented care caused by lost or inaccessible patient information.

The system comprises three interconnected portals:

- **Hospital Portal:** Manage staff accounts, departments, and patient registrations.  
- **Doctor Portal:** Access and update medical records, track consultations, prescriptions, and lab results.  
- **Patient Portal:** Securely view records, schedule appointments, and share information across facilities using a unique QR-coded ID, ensuring continuity of care.

---

## Table of Contents

- [Technical Overview](#technical-overview)
- [Docker Deployment](#docker-deployment)
  - [Quick Deployment (One Command)](#quick-deployment-one-command)
  - [Local Build from Source](#local-build-from-source)
- [Check Logs](#check-logs)
- [Stop Services](#stop-services)
- [Access the Application](#access-the-application)
- [Notes](#notes)
- [Author](#author)

---

## Technical Overview

- **Backend:** FastAPI RESTful API with JWT-based authentication, password hashing, and access controls.  
- **Database:** PostgreSQL using SQLAlchemy ORM for secure and structured data management.  
- **Frontend:** Responsive interface built with HTML, CSS, and JavaScript.  
- **Additional Features:** PDF generation, QR code integration for patient ID and records sharing.  
- **Development Methodology:** Agile, with iterative testing, continuous feedback, and collaborative improvement.  

Challenges such as backend–frontend communication, database synchronization, and secure authentication were addressed using middleware, ORM relationships, transaction management, and rigorous testing.  

MedPulse improves efficiency, data security, and continuity of care, enabling healthcare providers to make informed decisions while empowering patients with control over their health information. It demonstrates a scalable, user-centered solution to modernize healthcare record management in resource-limited settings.

---

## Docker Deployment

MedPulse can be deployed using **Docker Compose**. There are two workflows:

1. **Quick setup:** Pull prebuilt Docker images from Docker Hub  
2. **Build locally:** Build Docker images from the source code

---

### Quick Deployment (One Command)

If you want to deploy **without building**, you can use the following commands:

```bash
# Pull the latest images
docker-compose pull

# Start all services in detached mode
docker-compose up -d
````

This will:

* Pull the latest **backend** and **frontend** images
* Start PostgreSQL on **host port 5433**
* Start FastAPI backend on **host port 8080**
* Start NGINX frontend on **host port 8000**

---

### Local Build from Source

If you want to **build the images locally** (for development or custom changes), use `build:` in `docker-compose.yml`:

```yaml
backend:
  build:
    context: ./api
    dockerfile: Dockerfile
  container_name: medpulse_backend
  restart: always
  env_file:
    - ./api/.env
  environment:
    POSTGRES_USER: medpulse_user
    POSTGRES_PASSWORD: bodemurairi2
    POSTGRES_DB: medpulse_db
    DATABASE_URL: postgresql+psycopg2://medpulse_user:bodemurairi2@db/medpulse_db
  ports:
    - "8080:8080"
  depends_on:
    - db

frontend:
  build:
    context: ./Frontend-summative-MedPulse-main
    dockerfile: Dockerfile
  container_name: medpulse_frontend
  restart: always
  ports:
    - "8000:80"
  depends_on:
    - backend
```

#### **Step 1 — Build Images**

```bash
docker-compose build --no-cache
```

#### **Step 2 — Start Services**

```bash
docker-compose up -d
```

---

### Check Logs

Follow logs for all services:

```bash
docker-compose logs -f
```

Logs for a specific service (e.g., backend):

```bash
docker-compose logs -f backend
```

---

### Stop Services

Stop all running containers:

```bash
docker-compose down
```

Remove containers **and volumes**:

```bash
docker-compose down -v
```

---

### Access the Application

* **Frontend:** [http://localhost:8000](http://localhost:8000)
* **Backend API docs:** [http://localhost:8080/docs](http://localhost:8080/docs)

---

### Notes

* Ensure your `.env` file exists in `api/` if using environment variables.
* For development, modify code in `api/` or `Frontend-summative-MedPulse-main/` and rebuild locally.
* The system is designed for **secure, cloud-based operation**, centralizing patient records and ensuring continuity of care with QR code integration.

---

### Author

**Louis Pascal Nsigo <p.nsigo@alustudent.com>**
**Faith Irakoze <f.irakoze2@alustudent.com>**
**Bode Murairi <b.murairi@alustudent.com>**
**Laura Kwizera <l.kwizera1@alustudent.com>**
**Maurice Nshimyumukiza <m.nshimyumu@alustudent.com**
**Vanessa Umwari <v.umwari@alustudent.com>**

```
