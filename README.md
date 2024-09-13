## Prerequisites

- Python 3.8+
- Django 3.2+
- Celery 5.0+
- Redis
- Stability AI API Key

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nagar2817/ChaotixTask.git
   cd ChaotixTask
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Starting the Workers

1. **Start the Celery Worker:**
   ```bash
   celery -A django_project worker --loglevel=info
   ```

2. **Start the Django Development Server:**
   ```bash
   python manage.py runserver
   ```

## Running a Sample `curl` Command

Use the following `curl` command to generate images with multiple prompts:

```bash
curl -X POST http://127.0.0.1:8000/api/generate-images/ -H "Content-Type: application/json" -d '{"prompts": ["A red flying dog", "A piano ninja", "A footballer kid", "A futuristic cityscape"]}'
```

## API Endpoint

- **Endpoint**: `/api/generate-images/`
- **Method**: POST
- **Payload**:
  ```json
  {
    "prompts": ["A red flying dog", "A piano ninja", "A footballer kid", "A futuristic cityscape"]
  }
  ```

## Response

The API will return a JSON response with the task IDs for the generated images:

```json
{
  "task_ids": ["task_id_1", "task_id_2", "task_id_3", "task_id_4"]
}
```
