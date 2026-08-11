# Vercel Hosting Plan for Uninet Backend

## Branch
- Branch created: `vercel-backend-hosting-test`

## Goal
Deploy the Flask backend in `uninet-backend` to Vercel as a Python runtime deployment for testing.

## What is already configured
- `pyproject.toml` now includes a Vercel entrypoint:
  - `tool.vercel.entrypoint = "src.uninet.main:app"`
- `src/uninet/main.py` now exposes a top-level `app` instance for Vercel.
- `.python-version` is set to `3.14`, which is supported by Vercel.

## Required environment variables
The backend requires these variables in Vercel settings:

1. `DATABASE_URL`
   - Example: `postgresql://user:pass@host:port/dbname?sslmode=require`
   - Required for PostgreSQL/Neon access.
2. `MONGODB_URL` or `MONGODB__URL`
   - Required if the app uses MongoDB for auth storage.
   - Use the same URI format as MongoDB Atlas.
3. `SECRET_KEY`
   - Flask secret key used by the app.
4. `JWT_SECRET_KEY`
   - Used by `flask-jwt-extended` to sign tokens.

Optional / recommended:
- `CORS_ORIGINS`
  - Example: `https://your-frontend-domain.com`
  - If used by the app, it should match allowed frontend origins.

## Local `.env` setup
1. Copy the example file to create a local environment file:
   ```bash
   cd /home/janidu/workbench/Hackelite/uninet-backend
   cp .env.example .env
   ```
2. Replace placeholder values with real settings.
3. Do not commit `.env` to Git. `.gitignore` already excludes `.env`.

## Vercel project setup
### Option 1: Deploy via Vercel Dashboard
1. Sign in to Vercel and click `New Project`.
2. Import the repository containing `uninet-backend`.
3. Set the project root to `uninet-backend`.
4. Ensure the framework is detected as Python/Flask.
5. Add environment variables under `Settings > Environment Variables`:
   - `DATABASE_URL`
   - `MONGODB_URL` or `MONGODB__URL`
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
6. Optionally set the build command if Vercel does not auto-detect it.
   - For this repository, no custom build command should be required.
7. Deploy.

### Option 2: Deploy via Vercel CLI
1. Install Vercel CLI if not already installed:
   ```bash
   npm install -g vercel
   ```
2. From the backend root:
   ```bash
   cd /home/janidu/workbench/Hackelite/uninet-backend
   vercel login
   vercel link
   vercel env pull .env.local
   ```
3. Add environment variables using CLI or dashboard.
4. Deploy preview:
   ```bash
   vercel --confirm
   ```
5. Deploy production when ready:
   ```bash
   vercel --prod --confirm
   ```

## Testing the deployed backend
After deployment, verify the health endpoint:
- `https://<your-deployment-url>/health`

Verify API routes:
- `https://<your-deployment-url>/api/v1/auth/...`
- `https://<your-deployment-url>/api/v1/profile/...`

## Notes for a monorepo
If this repo contains both frontend and backend folders, keep the backend on its own Vercel project with root set to `uninet-backend`.

## Recommended next changes (if needed)
- Add a `vercel.json` file for custom function settings if you later need:
  - custom `maxDuration`
  - custom `memory`
  - specific route rewrites
- Keep secrets only in Vercel environment variables.
- Use `DATABASE_URL` and `MONGODB_URL` values from secured services.

## Summary
1. Use branch `vercel-backend-hosting-test`.
2. Confirm `tool.vercel.entrypoint` and top-level `app` are present.
3. Create local `.env` from `.env.example` for testing.
4. Configure Vercel environment vars.
5. Deploy from `uninet-backend` root.
6. Test `/health` and backend API routes.
