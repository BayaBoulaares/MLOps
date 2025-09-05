pipeline {
    agent any

    environment {
        APP_NAME = "mlops-flask-app"
        DOCKERHUB_CRED = credentials('baya-dockerhub') // Jenkins Credential ID contenant user/password
        DOCKER_IMAGE = "${DOCKERHUB_CRED_USR}/${APP_NAME}:latest"
    }

    triggers {
        githubPush()
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    # Installer requirements pour tests si présent
                    if [ -f tests/requirements.txt ]; then pip install -r tests/requirements.txt; fi
                    # Lancer tests si le dossier tests existe
                    if [ -d tests ]; then pytest -q || true; fi
                '''
            }
        }

        stage('Train & Log (MLflow)') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 model_training.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                // Vérifier que le Dockerfile existe avant build
                sh '''
                    if [ ! -f Dockerfile ]; then
                        echo "ERROR: Dockerfile not found!"
                        exit 1
                    fi
                    docker build -t ${APP_NAME} .
                '''
            }
        }

        stage('Login & Push Docker Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CRED_PSW" | docker login -u "$DOCKERHUB_CRED_USR" --password-stdin
                    docker tag ${APP_NAME} ${DOCKER_IMAGE}
                    docker push ${DOCKER_IMAGE}
                    docker logout
                '''
            }
        }

        stage('Deploy (Docker Compose)') {
            when { expression { return fileExists('docker-compose.yml') } }
            steps {
                sh '''
                    echo "Skipping real remote deploy, sample only."
                    # Exemple de commande si serveur distant :
                    # scp -r * user@server:/opt/app
                    # ssh user@server "cd /opt/app && docker compose pull && docker compose up -d --force-recreate"
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'model/*.pkl', fingerprint: true
            junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
            cleanWs()
        }
    }
}
