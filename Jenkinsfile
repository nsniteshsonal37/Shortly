pipeline {
    agent any

    environment {
        GRAFANA_SMTP_USER = credentials('grafana_smtp_user')
        GRAFANA_SMTP_PASSWORD = credentials('grafana_smtp_password')

        URL_DATABASE_URL = credentials('url_database_url')
        AUTH_SERVICE_URL = credentials('auth_service_url')

        AUTH_DATABASE_URL = credentials('auth_database_url')
        AUTH_SECRET_KEY = credentials('auth_secret_key')
        AUTH_ALGORITHM = credentials('auth_algorithm')
        AUTH_TOKEN_EXPIRE = credentials('auth_token_expire')
        BUILD_NOTIFY_EMAIL = credentials('build_notification_email')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Generate Env Files') {
            steps {
                sh '''
                # Root .env
                cat > .env <<EOF
GRAFANA_SMTP_USER=$GRAFANA_SMTP_USER
GRAFANA_SMTP_PASSWORD=$GRAFANA_SMTP_PASSWORD
EOF

                # URL Service .env
                cat > url-service/.env <<EOF
DATABASE_URL=$URL_DATABASE_URL
AUTH_SERVICE_URL=$AUTH_SERVICE_URL
EOF

                # Auth Service .env
                cat > auth-service/.env <<EOF
DATABASE_URL=$AUTH_DATABASE_URL
SECRET_KEY=$AUTH_SECRET_KEY
ALGORITHM=$AUTH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=$AUTH_TOKEN_EXPIRE
EOF
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                export DOCKER_API_VERSION=1.41
                export COMPOSE_PROJECT_NAME=shortly
                cd /opt/shortly
                docker-compose down --remove-orphans || true
                docker-compose up -d --build
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                set -e

                echo "Checking URL service..."
                for i in {1..10}; do
                  if curl -f http://localhost/health; then
                    echo "URL service healthy"
                    break
                  fi
                  if [ $i -eq 10 ]; then
                    echo "URL service failed health check"
                    exit 1
                  fi
                  echo "Retrying URL service..."
                  sleep 2
                done

                echo "Checking Auth service..."
                for i in {1..10}; do
                  if curl -f http://localhost/auth/health; then
                    echo "Auth service healthy"
                    break
                  fi
                  if [ $i -eq 10 ]; then
                    echo "Auth service failed health check"
                    exit 1
                  fi
                  echo "Retrying Auth service..."
                  sleep 2
                done

                echo "All health checks passed."
                '''
            }
        }
    }

    post {
        failure {
            emailext(
                subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build FAILED.

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}

Check logs immediately.
""",
                to: "${env.BUILD_NOTIFY_EMAIL}",
                attachLog: true
            )
        }

        unstable {
            emailext(
                subject: "⚠️ UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build is unstable.

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
""",
                to: "${env.BUILD_NOTIFY_EMAIL}"
            )
        }
    }
}
