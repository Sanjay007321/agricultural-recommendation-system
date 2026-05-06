import sys
import importlib

# Force reload modules
sys.modules.pop('app.api.analysis', None)
sys.modules.pop('app.services.climate_service', None)

from app.api.analysis import get_climate_dashboard
from app.services.climate_service import get_climate_dashboard_data
import inspect

print("API endpoint function:")
print(inspect.getsource(get_climate_dashboard))

print("\nClimate service function:")
print(inspect.getsource(get_climate_dashboard_data))