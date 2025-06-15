#!/usr/bin/env python3
"""
MetaChat Application

This is the main entry point for the MetaChat application,
which demonstrates a meta-level framework for enhancing AI conversations.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("metachat")

def setup_environment():
    """Set up the application environment."""
    # Create data directory if it doesn't exist
    data_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Check for OpenAI API key
    if "OPENAI_API_KEY" not in os.environ:
        logger.warning("OPENAI_API_KEY environment variable is not set. You'll need to provide it in the application.")

def run_streamlit():
    """Run the Streamlit application."""
    import subprocess
    import shutil
    
    streamlit_path = Path(os.path.dirname(os.path.abspath(__file__))) / "ui" / "streamlit_app.py"
    
    if not streamlit_path.exists():
        logger.error(f"Streamlit application not found at {streamlit_path}")
        sys.exit(1)
    
    logger.info(f"Starting Streamlit application from {streamlit_path}")
    
    # Try to find streamlit executable
    streamlit_cmd = shutil.which("streamlit")
    
    if streamlit_cmd:
        # Use the found streamlit command
        try:
            subprocess.run([streamlit_cmd, "run", str(streamlit_path)], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running Streamlit: {e}")
            sys.exit(1)
    else:
        # Fallback: Try to run streamlit via python module
        logger.info("Streamlit command not found in PATH, trying to run via python -m streamlit")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", str(streamlit_path)], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running Streamlit via python module: {e}")
            logger.error("Please ensure Streamlit is installed by running: pip install streamlit")
            logger.info("Alternatively, you can run the application directly with: streamlit run ui/streamlit_app.py")
            sys.exit(1)
        except FileNotFoundError:
            logger.error("Failed to launch Streamlit. Please ensure it's installed with: pip install streamlit")
            logger.info("Then run directly with: streamlit run ui/streamlit_app.py")
            sys.exit(1)

def run_cli():
    """Run the command-line interface."""
    logger.info("CLI mode is not implemented yet. Please use the Streamlit UI.")
    sys.exit(0)

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="MetaChat - A meta-level framework for enhancing AI conversations")
    parser.add_argument("--ui", choices=["streamlit", "cli"], default="streamlit", help="User interface to use")
    args = parser.parse_args()
    
    setup_environment()
    
    if args.ui == "streamlit":
        run_streamlit()
    elif args.ui == "cli":
        run_cli()
    else:
        logger.error(f"Unknown UI option: {args.ui}")
        sys.exit(1)

if __name__ == "__main__":
    main()