@echo off
set ROOT=performance-review-portal

echo Creating project structure...

:: Root
mkdir %ROOT%

:: =========================
:: FASTAPI BACKEND
:: =========================
mkdir %ROOT%\fastapi-backend
mkdir %ROOT%\fastapi-backend\routes
mkdir %ROOT%\fastapi-backend\controllers
mkdir %ROOT%\fastapi-backend\services
mkdir %ROOT%\fastapi-backend\dao
mkdir %ROOT%\fastapi-backend\dto
mkdir %ROOT%\fastapi-backend\models
mkdir %ROOT%\fastapi-backend\utils

type nul > %ROOT%\fastapi-backend\main.py
type nul > %ROOT%\fastapi-backend\config.py
type nul > %ROOT%\fastapi-backend\db.py
type nul > %ROOT%\fastapi-backend\requirements.txt
type nul > %ROOT%\fastapi-backend\Dockerfile

:: routes
type nul > %ROOT%\fastapi-backend\routes\__init__.py
type nul > %ROOT%\fastapi-backend\routes\auth_routes.py
type nul > %ROOT%\fastapi-backend\routes\review_cycle_routes.py
type nul > %ROOT%\fastapi-backend\routes\goal_routes.py
type nul > %ROOT%\fastapi-backend\routes\review_routes.py
type nul > %ROOT%\fastapi-backend\routes\manager_routes.py
type nul > %ROOT%\fastapi-backend\routes\competency_routes.py
type nul > %ROOT%\fastapi-backend\routes\admin_routes.py

:: controllers
type nul > %ROOT%\fastapi-backend\controllers\__init__.py
type nul > %ROOT%\fastapi-backend\controllers\auth_controller.py
type nul > %ROOT%\fastapi-backend\controllers\review_cycle_controller.py
type nul > %ROOT%\fastapi-backend\controllers\goal_controller.py
type nul > %ROOT%\fastapi-backend\controllers\review_controller.py
type nul > %ROOT%\fastapi-backend\controllers\manager_controller.py
type nul > %ROOT%\fastapi-backend\controllers\competency_controller.py
type nul > %ROOT%\fastapi-backend\controllers\admin_controller.py

:: services
type nul > %ROOT%\fastapi-backend\services\__init__.py
type nul > %ROOT%\fastapi-backend\services\auth_service.py
type nul > %ROOT%\fastapi-backend\services\review_cycle_service.py
type nul > %ROOT%\fastapi-backend\services\goal_service.py
type nul > %ROOT%\fastapi-backend\services\review_service.py
type nul > %ROOT%\fastapi-backend\services\manager_service.py
type nul > %ROOT%\fastapi-backend\services\competency_service.py
type nul > %ROOT%\fastapi-backend\services\admin_service.py

:: dao
type nul > %ROOT%\fastapi-backend\dao\__init__.py
type nul > %ROOT%\fastapi-backend\dao\user_dao.py
type nul > %ROOT%\fastapi-backend\dao\review_cycle_dao.py
type nul > %ROOT%\fastapi-backend\dao\goal_dao.py
type nul > %ROOT%\fastapi-backend\dao\review_dao.py
type nul > %ROOT%\fastapi-backend\dao\manager_dao.py
type nul > %ROOT%\fastapi-backend\dao\competency_dao.py
type nul > %ROOT%\fastapi-backend\dao\admin_dao.py

:: dto
type nul > %ROOT%\fastapi-backend\dto\__init__.py
type nul > %ROOT%\fastapi-backend\dto\auth_dto.py
type nul > %ROOT%\fastapi-backend\dto\review_cycle_dto.py
type nul > %ROOT%\fastapi-backend\dto\goal_dto.py
type nul > %ROOT%\fastapi-backend\dto\review_dto.py
type nul > %ROOT%\fastapi-backend\dto\manager_dto.py
type nul > %ROOT%\fastapi-backend\dto\competency_dto.py
type nul > %ROOT%\fastapi-backend\dto\admin_dto.py

:: models
type nul > %ROOT%\fastapi-backend\models\__init__.py
type nul > %ROOT%\fastapi-backend\models\user_model.py
type nul > %ROOT%\fastapi-backend\models\review_cycle_model.py
type nul > %ROOT%\fastapi-backend\models\goal_model.py
type nul > %ROOT%\fastapi-backend\models\review_model.py
type nul > %ROOT%\fastapi-backend\models\competency_model.py

:: utils
type nul > %ROOT%\fastapi-backend\utils\__init__.py
type nul > %ROOT%\fastapi-backend\utils\jwt_utils.py
type nul > %ROOT%\fastapi-backend\utils\password_utils.py
type nul > %ROOT%\fastapi-backend\utils\response_utils.py
type nul > %ROOT%\fastapi-backend\utils\exceptions.py


:: =========================
:: FLASK AI SERVICE
:: =========================
mkdir %ROOT%\flask-ai-service
mkdir %ROOT%\flask-ai-service\routes
mkdir %ROOT%\flask-ai-service\controllers
mkdir %ROOT%\flask-ai-service\services
mkdir %ROOT%\flask-ai-service\dao
mkdir %ROOT%\flask-ai-service\dto
mkdir %ROOT%\flask-ai-service\utils

type nul > %ROOT%\flask-ai-service\app.py
type nul > %ROOT%\flask-ai-service\config.py
type nul > %ROOT%\flask-ai-service\db.py
type nul > %ROOT%\flask-ai-service\requirements.txt
type nul > %ROOT%\flask-ai-service\Dockerfile

type nul > %ROOT%\flask-ai-service\routes\__init__.py
type nul > %ROOT%\flask-ai-service\routes\chatbot_routes.py

type nul > %ROOT%\flask-ai-service\controllers\__init__.py
type nul > %ROOT%\flask-ai-service\controllers\chatbot_controller.py

type nul > %ROOT%\flask-ai-service\services\__init__.py
type nul > %ROOT%\flask-ai-service\services\chatbot_service.py
type nul > %ROOT%\flask-ai-service\services\llm_service.py

type nul > %ROOT%\flask-ai-service\dao\__init__.py
type nul > %ROOT%\flask-ai-service\dao\faq_dao.py

type nul > %ROOT%\flask-ai-service\dto\__init__.py
type nul > %ROOT%\flask-ai-service\dto\chatbot_dto.py

type nul > %ROOT%\flask-ai-service\utils\__init__.py
type nul > %ROOT%\flask-ai-service\utils\response_utils.py
type nul > %ROOT%\flask-ai-service\utils\exceptions.py


:: =========================
:: DATABASE
:: =========================
mkdir %ROOT%\database

type nul > %ROOT%\database\01_create_tables.sql
type nul > %ROOT%\database\02_create_sequences.sql
type nul > %ROOT%\database\03_seed_data.sql
type nul > %ROOT%\database\04_sample_test_users.sql


:: Root files
type nul > %ROOT%\docker-compose.yml
type nul > %ROOT%\README.md

echo.
echo Done! Folder structure created successfully.
pause