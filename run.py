"""
Script untuk menjalankan Smart Reporting API
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Server will run on http://0.0.0.0:{settings.port}")
    print(f"Debug mode: {settings.debug}")
    print(f"API Documentation: http://localhost:{settings.port}/docs")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
