pipeline {
    agent any

    environment {
        APP_NAME = "mlops-flask-app"
        // Credential Docker Hub : un seul ID suffit
        DOCKERHUB = credentials('baya-dockerhub')
        DOCKER_IMAGE = "${DOCKERHUB_USR}/${APP_NAME}:latest"
        VENV_DIR = ".venv"
    }

    triggers {
        githubPush() // déclenche le pipeline à chaque push GitHub
    }

    options {
        timestamps()
        ansiColor('xterm') // colorisation des logs
        skipDefaultCheckout() // on fera checkout manuellement
    }

    stages {
        // ------------------------------
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        // ------------------------------
        stage('Setup Python & Install Dependencies') {
            steps {
                sh '''
                    # Création de l'environnement virtuel
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    # Installer requirements pour tests si présents
                    if [ -f tests/requirements.txt ]; then
                        pip install -r tests/requirements.txt
                    fi
                '''
            }
        }

        // ------------------------------
        stage('Run Unit Tests') {
            steps {
                sh '''
                    if [ -d tests ]; then
                        . $VENV_DIR/bin/activate
                        pytest -q --tb=short --disable-warnings || true
                    fi
                '''
            }
        }

        // ------------------------------
        stage('Train Model & Log with MLflow') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python3 model_training.py
                '''
            }
        }

        // ------------------------------
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $APP_NAME .
                '''
            }
        }

        // ------------------------------
        stage('Push Docker Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin
                    docker tag $APP_NAME $DOCKER_IMAGE
                    docker push $DOCKER_IMAGE
                    docker logout
                '''
            }
        }

        // ------------------------------
        stage('Deploy (Docker Compose)') {
            when { expression { return fileExists('docker-compose.yml') } }
            steps {
                sh '''
                    echo "Deploying via Docker Compose..."
                    docker compose pull
                    docker compose up -d --force-recreate
                '''
            }
        }
    }

    // ------------------------------
    post {
        always {
            script {
                // Sauvegarder les modèles et rapports
                archiveArtifacts artifacts: 'model/*.pkl', fingerprint: true
                junit 'reports/**/*.xml'
                cleanWs() // nettoyer le workspace après le build
            }
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
