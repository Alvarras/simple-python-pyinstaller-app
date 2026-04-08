# Simple Python CI/CD Pipeline

CI/CD pipeline menggunakan Jenkins dan Docker untuk build, test, dan deliver aplikasi Python dengan PyInstaller.

## Struktur Proyek

```
simple-python-pyinstaller-app/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile.jenkins          # Custom Jenkins image dengan Docker CLI
├── .env                        # Auto-generated (host Docker GID)
├── Jenkinsfile                 # Pipeline definition
├── nginx/
│   └── default.conf            # NGINX reverse proxy
└── sources/
    ├── add2vals.py             # Main application
    ├── calc.py                 # Calc library
    └── test_calc.py            # Unit tests
```

## Prerequisites

- Docker & Docker Compose
- Git

## Menjalankan

### 1. Setup Environment

```bash
# Generate .env dengan Docker GID dari host
echo "DOCKER_GID=$(getent group docker | cut -d: -f3)" > .env
```

### 2. Build & Start Containers

```bash
docker compose build --no-cache
docker compose up -d
```

### 3. Setup Jenkins

```bash
# Dapatkan admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Akses Jenkins:
- **Via NGINX**: http://localhost:9000
- **Direct**: http://localhost:49000

1. Install suggested plugins
2. Buat admin user
3. Buat akun `dicoding` (Setup → Security → Allow users to sign up)

### 4. Buat Pipeline

1. Login sebagai `dicoding`
2. **New Item** → Pipeline → **Pipeline script from SCM**
3. SCM: **Git**, repo URL Anda, branch `*/master`
4. Script Path: `Jenkinsfile`
5. Build Triggers: **Poll SCM** → `H/2 * * * *`
6. Install plugin **Blue Ocean** (opsional)

## Pipeline Stages

1. **Build** — Build aplikasi dengan PyInstaller di dalam container `python:3.9-slim`
2. **Test** — Jalankan pytest pada `sources/test_calc.py`
3. **Deliver** — Archive artifacts (log.txt dan dist/*)
