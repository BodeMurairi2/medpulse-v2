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

- [Demo Video](#demo-video)
- [Technical Overview](#technical-overview)
- [Run the Application](#run-the-application)
  - [Pull Docker Images](#pull-docker-images)
  - [Start Services](#start-services)
  - [Stop Services](#stop-services)
- [Access the Application](#access-the-application)
- [Author](#author)

---

## Demo Video

Clone the repository:

```bash
git clone https://github.com/BodeMurairi2/medpulse-v2.git
````

Inside the repository, you will find:

```
medpulse-v2/demo.mp4
```

---

## Run the Application

### Pull Docker Images

```bash
docker pull bodemurairi2/postgres:15
docker pull bodemurairi2/medpulse-v2_backend:latest
docker pull bodemurairi2/medpulse-v2_frontend:latest
```

### Start Services

From inside the `medpulse-v2/` directory:

```bash
# Start all services in detached mode
docker-compose up -d
```

This will:

* Pull the latest **backend** and **frontend** images if needed
* Start PostgreSQL on **host port 5433**
* Start FastAPI backend on **host port 8080**
* Start NGINX frontend on **host port 8000**

---

### Stop Services

Stop all running containers:

```bash
docker-compose down
```

Stop and remove containers **and volumes**:

```bash
docker-compose down -v
```

---

### Access the Application

* **Frontend:** [http://localhost:8000](http://localhost:8000)
* **Backend API docs:** [http://localhost:8080/docs](http://localhost:8080/docs)

---

## Author

### Backend Team

* **Louis Pascal Nsigo** – [p.nsigo@alustudent.com](mailto:p.nsigo@alustudent.com)
* **Faith Irakoze** – [f.irakoze2@alustudent.com](mailto:f.irakoze2@alustudent.com)
* **Bode Murairi** – [b.murairi@alustudent.com](mailto:b.murairi@alustudent.com)

### Frontend Team

* **Laura Kwizera** – [l.kwizera1@alustudent.com](mailto:l.kwizera1@alustudent.com)
* **Maurice Nshimyumukiza** – [m.nshimyumu@alustudent.com](mailto:m.nshimyumu@alustudent.com)
* **Vanessa Umwari** – [v.umwari@alustudent.com](mailto:v.umwari@alustudent.com)

```

---
