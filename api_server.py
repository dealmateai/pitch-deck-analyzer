"""
Main API server entry point.
Runs the FastAPI application.
"""

import sys
import uvicorn
from utils.logger import log, setup_logger
from config import API_CONFIG

# Setup logging
setup_logger()

def main():
    """Start the API server."""
    try:
        log.info("Starting Pitch Deck Analyzer API...")
        log.info(f"Server will run on {API_CONFIG['host']}:{API_CONFIG['port']}")
        log.info(f"API Documentation: http://localhost:{API_CONFIG['port']}/docs")
        
        # Start server
        uvicorn.run(
            "api.app:app",
            host=API_CONFIG["host"],
            port=API_CONFIG["port"],
            reload=not API_CONFIG["debug"],
            log_level="info",
        )
    
    except Exception as e:
        log.error(f"Failed to start API server: {str(e)}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())