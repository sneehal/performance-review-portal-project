pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'cd fastapi-backend && pip install -r requirements.txt'
                bat 'cd flask-ai-service && pip install -r requirements.txt'
                bat 'cd frontend && npm install'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'cd fastapi-backend && python test_all_apis.py'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                bat 'docker build -t performance-review-portal-backend:latest ./fastapi-backend'
                bat 'docker build -t performance-review-portal-ai-service:latest ./flask-ai-service'
                bat 'docker build -t performance-review-portal-frontend:latest ./frontend'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                bat 'kubectl apply -f k8s/'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Performance Review Portal deployed successfully!'
        }
        failure {
            echo 'Build failed. Check Jenkins console output.'
        }
    }
}