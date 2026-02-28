# Insights Visualization

A professional Django website for publishing, documenting, and gathering feedback on data visualizations rendered from Jupyter notebooks.

**Live site:** [insightsvisualization.pythonanywhere.com](https://insightsvisualization.pythonanywhere.com)

## Features

- **Notebook Visualizations** — Upload Jupyter `.ipynb` files and render them as interactive HTML pages
- **Articles** — In-depth technical articles about data visualization techniques
- **Blog** — Shorter posts with tips, updates, and insights
- **Comments & Feedback** — Authenticated users can leave comments on visualizations
- **User Authentication** — Sign up, sign in, password change
- **Admin Dashboard** — Full Django admin for content management
- **Tag System** — Organize content with reusable tags
- **Responsive Design** — Professional Bootstrap 5 UI with custom styling
- **Git-based Deployment** — Deploy to PythonAnywhere via `git push`

## Local Development

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd insightsvisualization

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate      # bash/zsh
source .venv/bin/activate.fish  # fish

# Run migrations
cd src/insightsvisualization
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/admin/>

## Deploying to PythonAnywhere

### First-time Setup

1. **Create a PythonAnywhere account** at pythonanywhere.com (free tier works)

2. **Open a Bash console** on PythonAnywhere and clone your repo:

   ```bash
   git clone <your-repo-url> ~/insightsvisualization
   ```

3. **Run the deployment script:**

   ```bash
   cd ~/insightsvisualization
   bash deploy.sh
   ```

4. **Configure the Web App** on PythonAnywhere dashboard:
   - **Source code:** `/home/insightsvisualization/insightsvisualization`
   - **Working directory:** `/home/insightsvisualization/insightsvisualization/src`
   - **Virtualenv:** `/home/insightsvisualization/.virtualenvs/insightsvisualization`
   - **WSGI file:** Copy contents of `pythonanywhere_wsgi.py` into PythonAnywhere's WSGI config
   - **Static files:**
     - URL: `/static/` → Directory: `/home/insightsvisualization/insightsvisualization/staticfiles`
     - URL: `/media/` → Directory: `/home/insightsvisualization/insightsvisualization/src/insightsvisualization/media`

5. **Create a superuser:**

   ```bash
   cd ~/insightsvisualization/src/insightsvisualization
   python manage.py createsuperuser --settings=insightsvisualization.website.settings
   ```

6. **Reload** the web app from the dashboard.

### Updating (after git push)

```bash
cd ~/insightsvisualization
bash deploy.sh update
```

## Project Structure

```
insightsvisualization/
├── pyproject.toml                # Project metadata & dependencies
├── requirements.txt              # Pip requirements (for PythonAnywhere)
├── deploy.sh                     # PythonAnywhere deployment script
├── pythonanywhere_wsgi.py        # WSGI config for PythonAnywhere
└── src/insightsvisualization/
    ├── manage.py                 # Django management
    ├── website/                  # Django project settings
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── core/                     # Home page, about page
    ├── blog/                     # Blog posts
    ├── articles/                 # In-depth articles
    ├── notebooks/                # Jupyter notebook visualizations + comments
    ├── accounts/                 # User authentication
    ├── templates/                # HTML templates
    └── static/                   # CSS, JS, images
```

## Adding Content

1. Sign in at `/admin/` with your superuser account
2. Add **Tags** to categorize content
3. Create **Notebook Visualizations** by uploading `.ipynb` files
4. Write **Articles** and **Blog Posts** using the admin editor
5. Set status to "Published" to make content visible

## Tech Stack

- **Django 5.2** — Web framework
- **SQLite** — Database (upgradeable)
- **Bootstrap 5** — Responsive UI
- **nbconvert** — Jupyter notebook rendering
- **PythonAnywhere** — Hosting (free tier)
