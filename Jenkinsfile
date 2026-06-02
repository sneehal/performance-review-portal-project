pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\mahin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

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
                bat 'cd fastapi-backend && "%PYTHON_EXE%" -m pip install -r requirements.txt'
                bat 'cd flask-ai-service && "%PYTHON_EXE%" -m pip install -r requirements.txt'
                bat 'cd frontend && npm install'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'cd fastapi-backend && "%PYTHON_EXE%" test_all_apis.py'
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