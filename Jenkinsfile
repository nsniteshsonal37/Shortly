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
		docker-compose down || true
                docker-compose up -d --build
		'''
            }
        }
    }
}
