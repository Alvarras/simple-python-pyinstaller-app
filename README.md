# Submission CI/CD dengan Docker

Proyek ini berisi implementasi CI/CD pipeline menggunakan Jenkins dan Docker Compose sesuai submission criteria.

## Struktur Proyek

```
simple-python-pyinstaller-app/
├── docker-compose.yml          # Docker Compose configuration
├── nginx/
│   └── default.conf            # NGINX reverse proxy configuration
├── jenkins/
│   └── Jenkinsfile             # Scripted Pipeline configuration
├── sources/
│   ├── add2vals.py             # Main application
│   ├── calc.py                 # Calc library
│   └── test_calc.py            # Unit tests
└── README.md
```

## Arsitektur

```
Docker Compose:
├── Jenkins (port 49000 → 8080 internal)
├── NGINX reverse proxy (port 9000 → Jenkins:8080)
└── Jenkins Agent (port 50000)
```

## Cara Menjalankan

### Prerequisites
- Docker dan Docker Compose terinstall
- Git terinstall

### Step 1: Clone dan Jalankan Docker Compose

```bash
cd "submission-cicd"
docker compose up -d
```

### Step 2: Dapatkan Initial Admin Password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 3: Akses Jenkins

- **Via NGINX**: http://localhost:9000
- **Direct**: http://localhost:49000

### Step 4: Setup Jenkins

1. Masukkan `initialAdminPassword`
2. Pilih **"Install suggested plugins"**
3. Buat admin user
4. Selesaikan wizard

### Step 5: Aktifkan Signup

1. **Manage Jenkins → Security → Security Realm**
2. Pilih **"Jenkins' own user database"**
3. Centang **"Allow users to sign up"**
4. Klik **Save**

### Step 6: Buat Akun `dicoding`

1. Logout dari admin
2. Klik **"Create an account"**
3. Isi:
   - Username: `dicoding`
   - Password: (bebas)
   - Full name: `Dicoding Indonesia`
   - Email: (email Anda)

### Step 7: Buat Pipeline

1. Login sebagai `dicoding`
2. **New Item** → Nama: `submission-cicd-pipeline-<username>`
3. Pilih **Pipeline** → OK
4. **Build Triggers**: Centang **Poll SCM**
5. Jadwal: `H/2 * * * *`
6. **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: URL repository Anda
   - Branch: `*/master`
   - Script Path: `jenkins/Jenkinsfile`
7. **Save**

### Step 8: Install Blue Ocean

1. **Manage Jenkins → Plugins → Available plugins**
2. Cari **Blue Ocean** → Install
3. Restart Jenkins

## Pipeline Stages

Pipeline terdiri dari 3 stage:

1. **Build**: Install PyInstaller dan build aplikasi
2. **Test**: Jalankan pytest pada `sources/test_calc.py`
3. **Deliver**: Archive artifacts (log.txt dan dist/*)
