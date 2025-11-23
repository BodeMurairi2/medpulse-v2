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

- [Demo Video Orientation] (#demo-video)
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

## Demo Video

git clone https://github.com/BodeMurairi2/medpulse-v2.git
Inside the repository, find demo.mp4
medpulse-v2/demo.mp4

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

## Run the application
To run the application, pull the docker images
docker pull bodemurairi2/postgres:15
docker pull bodemurairi2/medpulse-v2_backend:latest
docker pull bodemurairi2/medpulse-v2_frontend:latest


# Start all services in detached mode
inside mepulse-v2/
docker-compose up
docker-compose up -d
````

This will:

* Pull the latest **backend** and **frontend** images
* Start PostgreSQL on **host port 5433**
* Start FastAPI backend on **host port 8080**
* Start NGINX frontend on **host port 8000**

---


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

## Author  

### Name & Email

- Backend Team:

* **Louis Pascal Nsigo <p.nsigo@alustudent.com>**
* **Faith Irakoze <f.irakoze2@alustudent.com>**
* **Bode Murairi <b.murairi@alustudent.com>**

- Frontend Team:

* **Laura Kwizera <l.kwizera1@alustudent.com>**
* **Maurice Nshimyumukiza <m.nshimyumu@alustudent.com**
* **Vanessa Umwari <v.umwari@alustudent.com>**

```
