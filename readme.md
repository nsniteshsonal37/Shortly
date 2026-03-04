# Shortly --- Microservices URL Shortener with DevOps Observability Stack

Frontend: https://shortlyfrontend.vercel.app

Frontend Repository:

https://github.com/PawanKumar2001/Short.ly_front_end

Shortly is a **production-style microservices URL shortener** designed
to demonstrate modern **DevOps practices, observability, CI/CD
automation, and distributed system architecture**.

The platform consists of two backend services, a full monitoring stack,
centralized logging, and automated deployments.

------------------------------------------------------------------------

# Frontend

The frontend for Shortly is maintained in a separate repository.

Frontend repository:

https://github.com/PawanKumar2001/Short.ly_front_end

Live frontend deployment:

https://shortlyfrontend.vercel.app

The frontend is deployed using **Vercel** and communicates with the
backend API exposed by the Shortly services.

------------------------------------------------------------------------

# Live Deployment

The backend services are exposed using a **Cloudflare Tunnel**.

This allows the system to be publicly accessible without requiring a
dedicated cloud server or static IP.

Because the project uses the **free Cloudflare tunnel tier**, the API
may take **a few seconds to respond on the first request while the
tunnel initializes**.

Subsequent requests respond normally once the tunnel is active.

------------------------------------------------------------------------

# Architecture Overview

The system is built using a **microservices architecture**.

Client → URL Service → Auth Service → PostgreSQL

Each service has its own database and communicates via internal APIs.

Core components:

-   URL Service --- manages shortened links
-   Auth Service --- handles authentication and token verification
-   PostgreSQL --- separate databases per service
-   Prometheus --- metrics collection
-   Grafana --- dashboards and alerts
-   Loki --- centralized logging
-   Promtail --- log ingestion
-   Node Exporter --- infrastructure monitoring
-   Jenkins --- CI/CD automation
-   Docker Compose --- container orchestration

------------------------------------------------------------------------

# System Architecture

                     ┌─────────────┐
                     │   Client    │
                     └──────┬──────┘
                            │
                            ▼
                   ┌────────────────┐
                   │   URL Service   │
                   │ (FastAPI)       │
                   └──────┬─────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Auth Service   │
                  │ (FastAPI)      │
                  └──────┬────────┘
                         │
              ┌──────────┴───────────┐
              ▼                      ▼
         PostgreSQL             PostgreSQL
          (url-db)               (auth-db)

------------------------------------------------------------------------

# Observability Stack

Shortly includes a full **monitoring and logging pipeline**.

    Services
       │
       ▼
    Prometheus ───► Grafana (dashboards + alerts)
       │
       ▼
    Node Exporter (host metrics)

    Docker logs
       │
       ▼
    Promtail ───► Loki ───► Grafana Logs

Features:

-   Request rate monitoring
-   Error rate monitoring
-   p95 latency tracking
-   Container resource monitoring
-   Centralized log aggregation
-   Email alert notifications

------------------------------------------------------------------------

# DevOps Features

This project demonstrates multiple DevOps practices.

## CI/CD

Jenkins pipeline automatically:

-   checks out code
-   injects secrets via credentials
-   generates service `.env` files
-   rebuilds containers
-   deploys via Docker Compose
-   runs health checks
-   sends failure notifications

------------------------------------------------------------------------

## Automated Database Migrations

Each service runs migrations on startup:

    alembic upgrade head

This ensures schema compatibility during deployments.

------------------------------------------------------------------------

## Containerized Microservices

Services are isolated using Docker:

-   auth-service
-   url-service
-   auth-db
-   url-db

Each service owns its data.

------------------------------------------------------------------------

## Observability

Metrics:

-   Prometheus scraping `/metrics` endpoints

Logging:

-   Promtail collects Docker logs
-   Loki stores indexed logs
-   Grafana provides query dashboards

Infrastructure monitoring:

-   Node Exporter collects host CPU/memory/disk metrics

------------------------------------------------------------------------

## Operational Runbooks

Operational runbooks exist for:

-   service outages
-   high latency
-   elevated error rates

These guide incident diagnosis and recovery.

------------------------------------------------------------------------

# Authentication Flow

Authentication uses **JWT tokens**.

    Client
       │
       ▼
    POST /login
       │
       ▼
    Auth Service
       │
       ▼
    JWT issued
       │
       ▼
    Client request with Bearer token
       │
       ▼
    URL Service verifies token via Auth Service

The URL service delegates token validation to the auth service.

------------------------------------------------------------------------

# API Overview

## Auth Service

Register user

    POST /register

Login

    POST /login

Verify token (internal service endpoint)

    POST /verify

------------------------------------------------------------------------

## URL Service

Create short link

    POST /links

List user links

    GET /links

Delete link

    DELETE /links/{id}

Redirect

    GET /{short_code}

------------------------------------------------------------------------

# Database Design

Each microservice has its own database.

### Auth Database

users

-   id
-   email
-   username
-   hashed_password
-   is_active

------------------------------------------------------------------------

### URL Database

links

-   id
-   original_url
-   short_code
-   owner_id
-   clicks
-   created_at

Indexes enable fast redirect lookups.

------------------------------------------------------------------------

# Running the Project

Start the entire stack:

    docker compose up -d --build

Services will be available at:

URL service

    http://localhost:8001

Auth service

    http://localhost:8000

Grafana

    http://localhost:3000

Prometheus

    http://localhost:9091

------------------------------------------------------------------------

# Monitoring

Grafana dashboards include:

-   request throughput
-   p95 latency
-   error rate
-   system CPU/memory
-   container logs

Alerts trigger email notifications for:

-   service outages
-   high latency
-   elevated error rates

------------------------------------------------------------------------

# Technology Stack

Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   Alembic

Infrastructure

-   Docker
-   Docker Compose

CI/CD

-   Jenkins

Observability

-   Prometheus
-   Grafana
-   Loki
-   Promtail
-   Node Exporter

Authentication

-   JWT
-   bcrypt

------------------------------------------------------------------------

# DevOps Concepts Demonstrated

This project demonstrates:

-   microservices architecture
-   container orchestration
-   CI/CD pipelines
-   centralized logging
-   metrics-based monitoring
-   incident response runbooks
-   migration-driven deployments
-   service-to-service authentication
-   rate limiting and API protection

------------------------------------------------------------------------

# Purpose

This project was built to demonstrate **real-world DevOps workflows and
production-style backend architecture** in a small but complete system.

