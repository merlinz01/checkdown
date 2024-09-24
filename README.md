# Checkdown

Checkdown is a simple task management application built with Django and Vue. It provides a user-friendly interface for managing projects and tasks, assigning tasks to team members, and tracking progress.

## Features

- Task Management: Create, update, and delete tasks with ease.
- User Collaboration: Assign tasks to team members and track their progress.
- Dark Theme: Enjoy a modern dark theme for a better user experience.
- Responsive Design: Access Checkdown on any device, including desktops, tablets, and smartphones.

## Technologies Used

- Vue.js: A progressive JavaScript framework for building user interfaces.
- Vuetify: A Material Design component framework for Vue.js.
- Django: A high-level Python web framework for rapid development.

## Local Installation

Checkdown is a Django project with a Vue.js frontend. To run the project locally, follow the steps below:

1. Clone the repository:

```bash
git clone https://github.com/merlinz01/checkdown.git
```

2. Navigate to the project directory:

```bash
cd checkdown
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

4. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

5. Install the Node.js dependencies:

```bash
cd tasks/frontend
yarn install
```

6. Run the Vue.js frontend development server:

```bash
yarn dev
```

7. In a new terminal, run the Django development server:

```bash
python3 manage.py runserver
```

8. Open your browser and navigate to `http://localhost:7000` to access the Checkdown application.

## Deployment

Checkdown is published as a Docker image on Docker Hub. To deploy the application using Docker Compose, follow the steps below:

1. Download the Docker Compose configuration file:

```bash
wget https://raw.githubusercontent.com/merlinz01/checkdown/main/docker-compose.yml
```

2. Create a `.env` file with the following environment variables:

```bash
CHECKDOWN_HOSTNAME=your.hostname.com
```

3. Create a `.secret_key` file with a random secret key:

```bash
openssl rand -base64 64 > .secret_key
```

4. Set the Django superuser password as an environment variable for the initial run:

```bash
read -s -p "Enter Django superuser password: " DJANGO_SUPERUSER_PASSWORD
```

5. Run Docker Compose to start the application:

```bash
docker-compose up
```

# License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
