# Railway Deployment Guide for SAMS Application

## Prerequisites Checklist ✓
- [x] requirements.txt created
- [x] Procfile created
- [x] runtime.txt created
- [x] railway.json created
- [x] .env.example created
- [x] settings.py updated for production
- [x] WhiteNoise configured for static files
- [x] PostgreSQL support added

## Step 1: Generate Production SECRET_KEY

Run this command locally to generate a secure secret key:

```bash
cd "F:\Desktop\WT\2025FA Web App Dev (CIDM-6325-70)\CIDM-Repo\CIDM6325\CIDM6325\sams_site"
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**IMPORTANT**: Copy the output - you'll need it for Railway environment variables.

## Step 2: Push Code to GitHub

```bash
cd "F:\Desktop\WT\2025FA Web App Dev (CIDM-6325-70)\CIDM-Repo\CIDM6325\CIDM6325"
git add .
git commit -m "feat: add Railway deployment configuration

- Add requirements.txt with production dependencies
- Add Procfile for gunicorn web server
- Add runtime.txt specifying Python 3.11.9
- Add railway.json with migration/collectstatic commands
- Update settings.py for production (env vars, PostgreSQL, WhiteNoise)
- Add .env.example template

Refs #[ISSUE_NUMBER]"

git push origin FALL2025
```

## Step 3: Set Up Railway

### 3.1 Create Railway Account
1. Go to https://railway.app
2. Click "Login" and sign in with your GitHub account
3. Authorize Railway to access your repositories

### 3.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `zanehill01/CIDM6325` repository
4. **CRITICAL**: Set root directory to `/CIDM6325/sams_site` (because of nested structure)

### 3.3 Add PostgreSQL Database
1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create the database and set `DATABASE_URL` environment variable

### 3.4 Configure Environment Variables
In Railway dashboard, go to your web service → Variables tab and add:

```
SECRET_KEY = [paste the generated secret key from Step 1]
DEBUG = False
ALLOWED_HOSTS = .railway.app
```

**Note**: `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

## Step 4: Deploy

Railway will automatically deploy when you push to GitHub. The deployment process:
1. Detects `runtime.txt` and installs Python 3.11.9
2. Installs dependencies from `requirements.txt`
3. Runs commands from `railway.json`:
   - `python manage.py migrate` (creates database tables)
   - `python manage.py collectstatic --noinput` (gathers static files)
   - `gunicorn sams_site.wsgi --log-file -` (starts web server)

## Step 5: Post-Deployment Setup

### 5.1 Create Superuser

Install Railway CLI (one-time):
```bash
# Windows PowerShell
iwr https://railway.app/install.ps1 | iex
```

Then create superuser:
```bash
railway login
railway link  # Select your project
railway run python manage.py createsuperuser
```

Follow prompts to create admin account.

### 5.2 Create 20 Students

Option A - Django Shell (recommended):
```bash
railway run python manage.py shell
```

Then paste this code:
```python
from sams.models import Student

students = [
    ("Michael Johnson", "S001"), ("Sarah Williams", "S002"),
    ("David Brown", "S003"), ("Emily Davis", "S004"),
    ("James Wilson", "S005"), ("Jessica Martinez", "S006"),
    ("Robert Anderson", "S007"), ("Jennifer Taylor", "S008"),
    ("Christopher Thomas", "S009"), ("Amanda Moore", "S010"),
    ("Matthew Jackson", "S011"), ("Ashley Martin", "S012"),
    ("Daniel Lee", "S013"), ("Brittany White", "S014"),
    ("Joshua Harris", "S015"), ("Stephanie Clark", "S016"),
    ("Andrew Lewis", "S017"), ("Nicole Robinson", "S018"),
    ("Ryan Walker", "S019"), ("Lauren Young", "S020")
]

for name, student_id in students:
    Student.objects.create(name=name, student_id=student_id)
    print(f"Created {name}")

print(f"\nTotal students: {Student.objects.count()}")
exit()
```

Option B - Create via Admin Interface:
1. Go to `https://your-app.railway.app/admin/`
2. Login with superuser credentials
3. Navigate to Students → Add student
4. Manually create all 20 students

## Step 6: Verify Deployment

1. Visit your Railway app URL (e.g., `https://sams-app-production.up.railway.app`)
2. Test login page loads
3. Login as admin and verify calendar displays
4. Test attendance feature with the orange button
5. Create a test student account and verify permission restrictions

## Troubleshooting

### Check Logs
```bash
railway logs
```

### Common Issues

**Static files not loading**:
- Verify `STATIC_ROOT` is set in settings.py
- Check Railway logs for collectstatic errors
- Ensure WhiteNoise middleware is enabled

**Database connection errors**:
- Verify PostgreSQL addon is attached
- Check `DATABASE_URL` environment variable exists
- Review migration logs in Railway dashboard

**500 Internal Server Error**:
- Set `DEBUG=True` temporarily to see error details
- Check Railway logs for Python tracebacks
- Verify all environment variables are set correctly

**Permission errors**:
- Ensure superuser was created successfully
- Check that student accounts exist in production database
- Verify is_staff flag is set correctly on admin accounts

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (generate fresh for production) | `django-insecure-abc123...` |
| `DEBUG` | Debug mode (MUST be False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `.railway.app` |
| `DATABASE_URL` | PostgreSQL connection (auto-set by Railway) | `postgresql://user:pass@host:5432/db` |

## Continuous Deployment

Railway automatically redeploys when you push to the `FALL2025` branch:
```bash
git add .
git commit -m "feat: <description> Refs #<issue>"
git push origin FALL2025
# Railway deploys automatically
```

## Rollback

To rollback to a previous deployment:
1. Go to Railway dashboard → Deployments tab
2. Find the working deployment
3. Click "Redeploy"

Or via Git:
```bash
git revert <commit-hash>
git push origin FALL2025
```

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Unique `SECRET_KEY` (never reuse dev key)
- [ ] `ALLOWED_HOSTS` restricted to Railway domain
- [ ] PostgreSQL database (not SQLite in production)
- [ ] WhiteNoise serving static files securely
- [ ] Admin account uses strong password
- [ ] Student accounts have limited permissions

## Support

- Railway Docs: https://docs.railway.app/
- Django Deployment Checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- Course Repository: https://github.com/zanehill01/CIDM6325
