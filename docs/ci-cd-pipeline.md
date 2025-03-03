# CI/CD Pipeline Documentation

This document provides detailed information about the Continuous Integration and Continuous Deployment (CI/CD) pipeline implemented for the MicroEcom project using GitHub Actions.

## Overview

The CI/CD pipeline automates the process of code integration, testing, building, and deployment. It ensures that code changes are automatically validated, tested, and deployed to the appropriate environments.

## Workflow Files

The pipeline is defined in three main workflow files located in the `.github/workflows/` directory:

### 1. ci-cd.yml

The main workflow file that handles linting, testing, building Docker images, and deployment.

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **Lint**: Checks code quality using flake8, black, and isort
- **Test**: Runs unit and integration tests with pytest
- **Build**: Builds Docker images and pushes them to GitHub Container Registry
- **Deploy**: Deploys to staging or production environments based on the branch

### 2. security-scan.yml

Handles security scanning for dependencies, code, and container images.

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Weekly schedule (Sunday at midnight)

**Jobs:**
- **Dependency Check**: Scans Python dependencies for vulnerabilities using safety
- **Code Scanning**: Analyzes code for security issues using Bandit
- **Container Scan**: Scans Docker images for vulnerabilities using Trivy

### 3. infra-validation.yml

Validates infrastructure configuration files.

**Triggers:**
- Push to `main` or `develop` branches when Docker-related files change
- Pull requests to `main` or `develop` branches when Docker-related files change

**Jobs:**
- **Validate Docker Compose**: Checks docker-compose.yml for errors
- **Validate Dockerfiles**: Lints Dockerfiles using Hadolint
- **Test Docker Build**: Ensures Docker images can be built successfully

## Pipeline Stages

### 1. Lint

Code quality checks are performed using:
- **flake8**: For Python syntax and style errors
- **black**: For code formatting
- **isort**: For import sorting

Each microservice is linted separately to ensure code quality across the entire project.

### 2. Test

Tests are run using pytest with coverage reporting:
- Unit tests for individual components
- Integration tests for API endpoints
- Database tests with PostgreSQL test instances

Test environments are set up with:
- PostgreSQL database for data storage
- Redis for caching and message queuing

### 3. Build

Docker images are built and pushed to GitHub Container Registry:
- Each microservice gets its own image
- Images are tagged with branch name and commit SHA
- Build caching is used to speed up the process

### 4. Security Scan

Security scanning is performed at multiple levels:
- **Dependencies**: Checks for known vulnerabilities in Python packages
- **Code**: Static analysis to find potential security issues
- **Containers**: Scans Docker images for vulnerabilities

Results are uploaded to GitHub Security tab for easy tracking and remediation.

### 5. Deploy

Deployment is handled based on the branch:
- **develop**: Deploys to staging environment
- **main**: Deploys to production environment

The deployment process is currently simulated but can be extended to use:
- Kubernetes (kubectl)
- AWS ECS/EKS
- Azure Container Apps
- Other cloud platforms

## Environment Configuration

The pipeline uses GitHub Environments for deployment:
- **Staging**: For testing changes before production
- **Production**: For live application

Environment-specific variables and secrets can be configured in GitHub repository settings.

## Required Secrets

The following secrets should be configured in your GitHub repository:
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- Additional secrets for cloud provider authentication (if needed)

## Status Badges

Status badges are available for each workflow:
- CI/CD Pipeline: ![CI/CD Pipeline](https://github.com/yourusername/MicroEcom/actions/workflows/ci-cd.yml/badge.svg)
- Security Scan: ![Security Scan](https://github.com/yourusername/MicroEcom/actions/workflows/security-scan.yml/badge.svg)
- Infrastructure Validation: ![Infrastructure Validation](https://github.com/yourusername/MicroEcom/actions/workflows/infra-validation.yml/badge.svg)

## Best Practices for Developers

1. **Branch Strategy**:
   - Create feature branches from `develop`
   - Use descriptive branch names (e.g., `feature/user-authentication`)
   - Keep branches short-lived and focused on specific features or fixes

2. **Commit Messages**:
   - Write clear, concise commit messages
   - Reference issue numbers when applicable (e.g., "Fix #123: User login issue")

3. **Pull Requests**:
   - Create pull requests to `develop` for feature integration
   - Ensure all CI checks pass before requesting review
   - Address review comments promptly

4. **Testing**:
   - Write tests for new features and bug fixes
   - Aim for high test coverage
   - Run tests locally before pushing

5. **Security**:
   - Address security issues identified by the security scan
   - Regularly update dependencies to fix vulnerabilities
   - Follow secure coding practices

## Troubleshooting

### Common Issues

1. **Lint Failures**:
   - Run linting tools locally to fix issues before pushing
   - Use pre-commit hooks to automate linting

2. **Test Failures**:
   - Check test logs in GitHub Actions for details
   - Reproduce the issue locally using the same environment variables

3. **Build Failures**:
   - Ensure Dockerfiles are valid and follow best practices
   - Check for missing dependencies or configuration issues

4. **Deployment Failures**:
   - Verify environment variables and secrets are correctly set
   - Check for connectivity issues with deployment targets

### Getting Help

If you encounter issues with the CI/CD pipeline:
1. Check the workflow run logs in GitHub Actions
2. Review this documentation for guidance
3. Contact the DevOps team for assistance

## Future Improvements

Planned enhancements for the CI/CD pipeline:
- Integration with infrastructure as code (Terraform/Pulumi)
- Automated database migrations
- Performance testing integration
- Canary deployments
- Blue/green deployment strategy 