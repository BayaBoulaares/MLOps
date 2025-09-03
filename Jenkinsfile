pipeline {
    agent any

    environment {
        APP_NAME = "mlops-flask-app"
        // Credential Docker Hub : un seul ID suffit
        DOCKERHUB = credentials('baya-dockerhub')
        DOCKER_IMAGE = "${DOCKERHUB_USR}/${APP_NAME}:latest"
    }

    triggers {
        githubPush()
    }

    options {
        timestamps()
        // ansiColor nécessite le plugin "AnsiColor" installé dans Jenkins
        // si non installé, commentez la ligne suivante
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
                sh 'docker build -t ${APP_NAME} .'
            }
        }

        stage('Login & Push Docker Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin
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
            script {
                archiveArtifacts artifacts: 'model/*.pkl', fingerprint: true
                junit 'reports/**/*.xml' // si vous avez des rapports de tests JUnit
                cleanWs()
            }
        }
    }
}
