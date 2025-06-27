## 🛠️ Instalación y despliegue local

### 1. Clona el repositorio

```bash
git clone https://github.com/Arisen32/InnovaTube.git
cd innovatube

## Crear el entorno virtual 
# En Windows
python -m venv venv

##Ejecuta el entorno virtual
.venv\Scripts\activate


##Instalar las dependencias
pip install -r requirements.txt

##Aplicar Migraciones
python manage.py migrate

##Ejecuta el servidor local 
python manage.py runserver
