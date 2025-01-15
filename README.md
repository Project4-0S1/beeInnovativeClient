# Bee Innovative Client App
This application is the client that runs the AI detections and connects to the server.

The client app is stored in /opt/beeInnovativeCLient
Run the client app by running the following command:
```python3 /opt/beeInnovativeClient/app.py```

# Branching Strategy for Web App, API Development and Client

## Overview
We will adopt a feature-based branching strategy to streamline the development of our web app and API. This ensures organized collaboration, efficient testing, and easy integration.

## Main Branches
- **main**: The stable branch containing production-ready code. Only thoroughly tested changes are merged here.
- **develop**: The integration branch for ongoing development. All feature branches are merged here after review.

## Feature Branch Workflow
1. **Branch Naming**: Use clear and consistent names, e.g., `<initials>-<short-description>`.
2. **Creation**: Branch from `develop` for each new feature.
3. **Development**: Implement the feature in isolation.
4. **Testing**: Ensure thorough testing within the feature branch.
5. **Merging**: Create a pull request to merge the feature branch into `develop`.

## Merging Guidelines

### Feature to Develop
- Open a Pull Request when the feature is complete.
- Ensure all tests pass and the code is reviewed.
- Merge with a **squash commit** to keep history clean.

### Develop to Main
- Merge into `main` only after rigorous testing on `develop`.
- Use a **merge commit** to retain the context of changes.
- Tag releases for versioning.

### Conflict Resolution
- Resolve conflicts locally before pushing to the branch.
- Always ensure the branch is up-to-date with its base before merging.
