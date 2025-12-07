#!/bin/bash
# Quick start script for authentication-services using Nox
# This script helps you set up and run the service in different environments

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if nox is installed
check_nox() {
    if ! command -v nox &> /dev/null; then
        print_error "Nox is not installed. Installing nox..."
        pip install nox
        print_success "Nox installed successfully!"
    else
        print_success "Nox is already installed"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [ENVIRONMENT]"
    echo ""
    echo "Environments:"
    echo "  dev       - Development environment (default)"
    echo "  uat       - User Acceptance Testing environment"
    echo "  prod      - Production environment"
    echo ""
    echo "Examples:"
    echo "  $0          # Setup and run development environment"
    echo "  $0 dev      # Setup and run development environment"
    echo "  $0 uat      # Setup and run UAT environment"
    echo "  $0 prod     # Setup and run production environment"
    echo ""
}

# Function to setup environment
setup_environment() {
    local env=$1
    
    print_info "Setting up ${env} environment..."
    
    # Copy environment file if .env doesn't exist
    if [ ! -f .env ]; then
        print_info "Copying .env.${env} to .env"
        cp ".env.${env}" .env
        print_success "Environment file created"
        print_warning "Please review and update .env with your configuration"
    else
        print_warning ".env file already exists. Skipping copy."
    fi
    
    # Install dependencies
    print_info "Installing dependencies..."
    nox -s "${env}-install"
    
    # Create superuser for dev environment
    if [ "$env" = "dev" ]; then
        print_info "You can create a superuser by running:"
        echo "    nox -s dev-createsuperuser"
    fi
    
    print_success "${env} environment setup complete!"
}

# Function to run server
run_server() {
    local env=$1
    
    print_info "Starting ${env} server..."
    print_info "Press Ctrl+C to stop the server"
    echo ""
    
    nox -s "${env}-server"
}

# Main script
main() {
    local env="${1:-dev}"
    
    # Show usage if help is requested
    if [ "$env" = "-h" ] || [ "$env" = "--help" ]; then
        show_usage
        exit 0
    fi
    
    # Validate environment
    if [ "$env" != "dev" ] && [ "$env" != "uat" ] && [ "$env" != "prod" ]; then
        print_error "Invalid environment: $env"
        show_usage
        exit 1
    fi
    
    print_info "Authentication Services - Quick Start"
    print_info "Environment: ${env}"
    echo ""
    
    # Check if nox is installed
    check_nox
    
    # Setup environment
    setup_environment "$env"
    
    # Ask if user wants to start the server
    echo ""
    read -p "Do you want to start the ${env} server now? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_server "$env"
    else
        print_info "You can start the server later by running:"
        echo "    nox -s ${env}-server"
    fi
}

# Run main function
main "$@"
