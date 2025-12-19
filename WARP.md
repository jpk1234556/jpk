# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository overview

Property Management System with:
- **Backend**: Django 4 + Django REST Framework in `backend/property_management`
- **Frontend**: Static HTML/CSS/JS in `frontend/` organized by user role (`admin-module/`, `property-owner-module/`, `public/`)
- **Database**: PostgreSQL, schema reference in `backend/database-schema.sql`
- **Deployment/ops**: Windows-focused `.bat` scripts in `deployment/`

Key documentation:
- `README.md` – project structure, core setup
- `backend/property_management/README.md` – backend APIs and setup
- `BACKEND_ORGANIZATION.md` – mapping between Django apps and role-based modules
- `MODULES.md` – high-level module concept (historic Node.js structure)
- `INTEGRATION_GUIDE.md` – how the HTML frontend talks to the Django API
- `SYSTEM_ARCHITECTURE_COMPARISON.md` – Node.js → Django migration overview

## Commands and workflows

All commands assume PowerShell or `cmd` on Windows unless noted.

### Backend setup and virtualenv

From the repo root:

1. Navigate to the Django project:
   - `cd backend/property_management`
2. (First time) Create and activate a virtualenv, then install deps:
   - `python -m venv venv`
   - PowerShell: `venv\Scripts\Activate.ps1`
   - cmd: `venv\Scripts\activate.bat`
   - `pip install -r requirements.txt`

There is also a helper script for Windows:
- `cd backend/property_management`
- `setup.bat` – creates `venv`, installs dependencies, and runs `python manage.py migrate`.

### Running the development server

From `backend/property_management` with the virtualenv active and a PostgreSQL instance configured (see `config/settings.py` and `.env`):

- Apply migrations (initial or after model changes):
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Create an admin superuser (for `/admin/` and default test credentials if desired):
  - `python manage.py createsuperuser`
- Start the dev server:
  - `python manage.py runserver`

The API will be available at `http://127.0.0.1:8000/`.

### Tests

#### Django test suite

From `backend/property_management` with the virtualenv active:

- Run all Django tests (including app test modules under `apps/*`):
  - `python manage.py test`
- Run tests for a specific app/module (example):
  - `python manage.py test apps.users.tests`

> Note: many higher-level tests in this repo are standalone scripts rather than Django `TestCase`s; see below.

#### API and integration test scripts

These scripts live at the **repo root** or under `backend/property_management` and exercise the running API. They expect the Django server to already be running on `http://127.0.0.1:8000` and specific users (e.g. `admin/admin`) to exist.

From the **repo root** (virtualenv active and `python manage.py runserver` running separately):

- Backend API sanity checks:
  - `python test_backend_apis.py`
- Frontend–backend integration smoke test (login + core APIs):
  - `python test_frontend_backend_integration.py`
- End-to-end workflow test (admin + owner flows, CRUD for properties/units/tenants/payments, dashboards, reports):
  - `python test_comprehensive.py`
- Additional scenario tests:
  - `python test_admin_workflow.py`
  - `python test_property_owner_workflow.py`
  - `python test_registration.py`
  - `python test_security.py`
  - `python test_performance.py`

From `backend/property_management`:

- Simple connectivity checks against the API:
  - `python test_api.py`
  - `python test_modules.py`

These scripts use `requests` and direct HTTP calls rather than Django's test runner.

### Management commands (scheduled/ops tasks)

Django management commands for notifications live under `apps/tenants/management/commands/` and rely on email configuration in `config/settings.py` / `.env`.

From `backend/property_management`:

- General notification runner (rent due, lease expiry, maintenance):
  - `python manage.py send_notifications --notification-type all`
  - Or narrower scopes, e.g.: `python manage.py send_notifications --notification-type rent_due --days-before-due 5`
- Focused rent-due notification job:
  - `python manage.py send_rent_notifications --days-before-due 5`

These commands use `EmailNotificationService` in `utils/email_utils.py` and templates in `templates/emails/`.

### Deployment-related scripts (Windows)

Production-oriented scripts in `deployment/` assume a Windows server layout and may need path customization before use:

- `deployment/deploy.bat` – pulls latest code into `C:\inetpub\wwwroot\property-management`, sets up/activates a venv, installs `requirements.txt`, runs `makemigrations`, `migrate`, `collectstatic`, `python manage.py test`, and restarts services (IIS restart is commented).
- `deployment/backup_db.bat` – runs `pg_dump` for the `property_management` database and compresses the dump.
- `deployment/monitor.bat` – simple health check script (process presence, disk/memory health, DB connectivity via `psql`, and basic log inspection).

Refer to `deployment/DEPLOYMENT_CHECKLIST.md` for a full manual deployment checklist.

## High-level architecture

### Backend layers

The Django backend in `backend/property_management` is organized into several layers:

1. **Project configuration** (`config/`)
   - `settings.py` – environment-driven configuration via `python-decouple` (`SECRET_KEY`, `DEBUG`, DB, email, CORS, security settings). Uses PostgreSQL as the default DB (`django.db.backends.postgresql`).
   - `urls.py` – top-level URL router, wiring core REST endpoints and role-based modules:
     - `/api/users/` → `apps.users.urls`
     - `/api/properties/` → `apps.properties.urls`
     - `/api/units/` → `apps.units.urls`
     - `/api/tenants/` → `apps.tenants.urls`
     - `/api/maintenance/` → `apps.maintenance.urls`
     - `/api/payments/` → `apps.payments.urls`
     - `/api/admin-module/` → `modules.admin.urls`
     - `/api/property-owner-module/` → `modules.property_owner.urls`
   - Logging configuration is delegated to `config/logging_config.py` and imported as `LOGGING`.

2. **Domain apps** (`apps/`)
   - Each core concept has its own Django app with `models.py`, `serializers.py`, `views.py`, `urls.py`, and `signals.py`:
     - `apps.users` – custom `User` model extending `AbstractUser` with `role` (`admin` / `property_owner`), `is_approved`, and timestamps.
     - `apps.properties` – `Property` model linking to `User` as `owner` with type (`hostel`, `apartment`, `hotel`, `rental`) and address.
     - `apps.units`, `apps.tenants`, `apps.maintenance`, `apps.payments` – units/rooms, tenant leases, maintenance requests, and payments, each with their own serializers and REST views.
   - These apps represent the data and business rules and are reused by the higher-level role-based modules.

3. **Role-based modules** (`modules/`)
   - Described in `BACKEND_ORGANIZATION.md` and `backend/property_management/modules/README.md`.
   - Organizes views/serializers and URLs by **user role**, mirroring the frontend folder structure:
     - `modules/admin/` – admin-only API surface:
       - `views/dashboard_views.py` (e.g., `AdminDashboardStatsView`) aggregates system-wide metrics such as total property owners, pending approvals, total properties, and (for now) mock active tenant counts.
       - `views/reports_views.py`, `views/settings_views.py` – report and settings endpoints used by admin dashboards.
       - `urls.py` – exposes endpoints like `/api/admin-module/dashboard-stats/`, `/api/admin-module/reports/`, `/api/admin-module/settings/`.
     - `modules/property_owner/` – property-owner-specific API surface:
       - `views/dashboard_views.py` (e.g., `PropertyOwnerDashboardStatsView`) computes stats filtered to `request.user`’s properties (property count, units, pending requests – some fields are still marked as TODO/mocked).
       - `views/reports_views.py` – owner-focused reporting endpoints.
       - `urls.py` – exposes `/api/property-owner-module/dashboard-stats/` and `/api/property-owner-module/reports/`.
   - The modules do **not** define models; they orchestrate between domain apps and present module-specific JSON structures aligned with frontend needs.

4. **Utilities and cross-cutting concerns**
   - `utils/email_utils.py` – `EmailNotificationService` encapsulates all outgoing email flows:
     - New user registration → notifies admin with an approval link.
     - User approval → notifies the user with a login URL.
     - Rent due notifications → sent to tenants.
     - Maintenance request notifications → sent to a property manager address.
     - Payment received notifications → sent to tenants.
   - Email templates live under `templates/emails/` and are rendered via `render_to_string` before sending.
   - Email and frontend URLs are configured via environment (`EMAIL_*`, `DEFAULT_FROM_EMAIL`, `ADMIN_EMAIL`, `FRONTEND_BASE_URL`).

5. **Background / scheduled tasks**
   - `apps.tenants.management.commands.send_notifications` – multi-purpose command that:
     - Sends rent-due notifications based on lease dates.
     - Logs upcoming lease expirations.
     - Sends notifications for recent pending maintenance requests.
   - `apps.tenants.management.commands.send_rent_notifications` – narrower rent-due notifier assuming a monthly rent cadence.
   - These commands use `EmailNotificationService` and tenant/maintenance models and are intended to be wired into a scheduler (e.g., Windows Task Scheduler, cron under Linux) on production systems.

### Frontend–backend mapping

The frontend is organized purely as HTML pages in `frontend/`:

- `frontend/admin-module/` – admin dashboard and related views.
- `frontend/property-owner-module/` – property-owner workflows (properties, tenants, maintenance, payments, reports).
- `frontend/public/` – unauthenticated views such as `landing.html`, `login.html`, and `register.html`.

`INTEGRATION_GUIDE.md` captures how these pages integrate with the `/api/...` endpoints:

- `login.html` posts credentials to `/api/users/login/` and stores the returned token in `localStorage`.
- Subsequent API calls include `Authorization: Token <token>` in headers.
- Users are redirected by role:
  - Admins → `frontend/admin-module/dashboard.html`
  - Property owners → `frontend/property-owner-module/dashboard.html`
- Dashboard pages call the module endpoints described above (`/api/admin-module/dashboard-stats/`, `/api/property-owner-module/dashboard-stats/`, and associated report endpoints), as well as the core CRUD endpoints (`/api/properties/`, `/api/units/`, `/api/tenants/`, `/api/maintenance/`, `/api/payments/`).

### Authentication and authorization model

- Custom `User` model (`apps.users.models.User`) adds a `role` field (`admin`, `property_owner`) and an `is_approved` flag.
- Django REST Framework is configured in `config/settings.py` with:
  - Token and session authentication.
  - `IsAuthenticated` as the default permission class (anonymous access is opt-in per view if needed).
- Role-based authorization is enforced in multiple layers:
  - Per-view checks like `if request.user.role == 'admin'` in module dashboards.
  - Queryset filtering in app-level views/serializers (e.g., owners only see their own properties, tenants, payments).
- Login endpoint (`/api/users/login/`) returns both `token` and a serialized `user` object; most tests and frontend flows rely on this structure.

### Legacy context and migration

The repository originally had a Node.js/Express backend with a similar two-module concept; this is documented (for reference) in:

- `MODULES.md` – describes the earlier Express-based module layout and API paths.
- `SYSTEM_ARCHITECTURE_COMPARISON.md` – maps prior Express routes to the current Django endpoints and compares behavior across layers (auth, DB, deployment, security).

The Django implementation preserves the same conceptual modules and URLs where possible, so older frontend expectations and documentation remain largely valid.
