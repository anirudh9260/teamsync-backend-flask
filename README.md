
# TeamSync Data Manager

Welcome to **TeamSync Data Manager**, a simple and efficient web application designed to streamline file sharing and data management within your team. Whether you're collaborating on projects, distributing resources, or organizing team assets, TeamSync provides an intuitive platform to keep everything in one place.


## Features

- **File Upload & Sharing**: Easily upload files and share them with your team members via links or direct access.
- **Organized Storage**: Categorize files into projects for quick retrieval and better organization.
- **Access Control**: Set permissions to control who can view, edit, or download files.
- **Conversion**: Convert files easily between different data formats (json-xml-csv).
- **Real-Time Collaboration**: Team members can access the latest versions of files instantly.
- **Search Functionality**: Quickly find files with a built-in search tool.
- **Cross-Platform**: Access TeamSync from any device with a web browser.

## Getting Started


### Installation
This project requires backend and front end setup seperately. To see how to setup frontend go to https://github.com/anirudh9260/teamsync-frontend-react.git
Follow these steps to set up TeamSync Backend locally:

1. Clone the repository:
```bash
git clone https://github.com/anirudh9260/teamsync-backend-flask.git

```

2. Create a virtual enviornment and install dependencies:
```bash
cd teamsync-backend-flask
python -m venv venv
```

3. activate the virtual enviornment and install dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

4. Create a .env file in the root directory(or rename the existing example env):
```bash
SECRET_KEY=<YOUR SECRET KEY>
CACHE_REDIS_HOST=<REDIS_HOST>
CACHE_REDIS_PORT=<REDIS_PORT>
CACHE_REDIS_DB=<REDIS_DB>
USERNAME=<DB_USERNAME>
PASSWORD=<DB_PASSWORD>
HOST=<DB_HOST>:<DB_PORT>
DB=<DB_NAME>
BASE_PATH=<BASE_NAME_FOR_API_URLS>
SERVER_PATH=<PATH_TO_STORE_UPLOADED_FILES>
```

4. Run the app:
```bash
flask run
```



## Support

If you encounter any issues or have questions:
- Contact your team admin.
- Email our support team at `anirudh.88@live.in`.

## License
This project is licensed under the MIT License - see the  file for details.

## Contact
For any queries, reach out to:
Email: anirudh.88@live.in


**Happy using TeamSync Data Manager!**