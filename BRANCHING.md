# Branching Strategy for BigSupport AI

To ensure the stability of the `main` branch, we follow a strict branching strategy.

## Branch Types

1. **main**: The production-ready branch. Only stable and tested code should be merged here.
2. **feature/*: For new features and enhancements.
3. **bugfix/*: For bug fixes.
4. **docs/*: For documentation updates.

## Workflow

1. Create a new branch from `main` (e.g., `feature/react-migration`).
2. Make your changes in the new branch.
3. Run all tests and verify frontend changes.
4. Open a Pull Request (PR) to merge into `main`.
5. Once reviewed and approved, merge the PR.

## GitHub Pages Deployment

The `docs/` folder contains the production build of the React frontend. It is automatically deployed to GitHub Pages when changes are pushed to `main`.
Do not edit files in `docs/` directly. Instead, make changes in `marketplace-frontend/src` and run `npm run build` from the `marketplace-frontend` directory.
