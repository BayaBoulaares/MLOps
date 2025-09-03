pipeline {
  agent any

  environment {
    APP_NAME = "mlops-flask-app"
    DOCKERHUB_USER = credentials('dockerhub-username')   // Jenkins Credential ID
    DOCKERHUB_PASS = credentials('dockerhub-password')   // Jenkins Credential ID
    DOCKER_IMAGE = "${DOCKERHUB_USER_USR}/${APP_NAME}:latest"
  }

  triggers {
    githubPush()
  }

  options {
    timestamps()
    wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm'])
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
          if [ -f tests/requirements.txt ]; then pip install -r tests/requirements.txt; fi
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
          echo "${DOCKERHUB_PASS_PSW}" | docker login -u "${DOCKERHUB_PASS_USR}" --password-stdin
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
          # scp -r * user@server:/opt/app
          # ssh user@server "cd /opt/app && docker compose pull && docker compose up -d --force-recreate"
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'model/*.pkl', fingerprint: true
      junit 'reports/**/*.xml'
      cleanWs()
    }
  }
}
