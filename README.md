# Assessment Project

A Django-based assessment application with PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd assessment-project
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at http://localhost:8000

## Development

### Running in Detached Mode
To run the application in the background:
```bash
docker-compose up -d
```

### Viewing Logs
To view the application logs:
```bash
docker-compose logs -f
```

### Stopping the Application
To stop the containers:
```bash
docker-compose down
```

## Database Management

### Creating a Superuser
To create an admin user:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Running Management Commands
To run any Django management command:
```bash
docker-compose exec web python manage.py <command>
```

### Accessing the Database
To access the PostgreSQL database directly:
```bash
docker-compose exec db psql -U postgres -d assessment_db
```

## Project Structure

```
assessment_project/
├── assessment/          # Main application directory
├── static/             # Static files
├── templates/          # HTML templates
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── requirements.txt   # Python dependencies
```

## Environment Variables

The following environment variables are configured in docker-compose.yml:

- `DEBUG`: Set to True for development
- `SECRET_KEY`: Django secret key
- `POSTGRES_DATABASE`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port

## Dependencies

Main dependencies include:
- Django 4.2.0
- PostgreSQL 13
- Gunicorn
- WhiteNoise
- psycopg2-binary
- python-dotenv

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request


