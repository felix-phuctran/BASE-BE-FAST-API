import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from utils.logger import setup_logger


class EmailTemplateManager:
    """
    Manager for email templates using Jinja2.
    """
    def __init__(self):
        self._logger = setup_logger()
        
        # Try multiple possible template locations
        possible_paths = [
            # Standard path resolution
            Path(__file__).resolve().parent.parent / "templates",
            # Current working directory
            Path.cwd() / "templates",
            # Go up one directory (for different module structures)
            Path.cwd().parent / "templates"
        ]
        
        template_dir = None
        
        # Find the first valid template directory
        for path in possible_paths:
            if path.exists() and path.is_dir():
                template_dir = path
                self._logger.info(f"Found template directory at: {template_dir}")
                break
        
        if not template_dir:
            self._logger.error("No template directory found in any of the expected locations")
            # Last resort: just use "templates" and let Jinja handle errors
            template_dir = Path("templates")
        
        # Create Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
        # List available templates for debugging
        try:
            available_templates = self.env.list_templates()
            self._logger.info(f"Available templates: {available_templates}")
        except Exception as e:
            self._logger.error(f"Could not list available templates: {str(e)}")

    def render_template(self, template_name: str, **context: Any) -> str:
        """
        Render a template with given context.
        
        Args:
            template_name: The name of the template file (relative to templates directory)
            **context: Variables to pass to the template
            
        Returns:
            str: The rendered HTML template
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            self._logger.error(f"Error rendering template '{template_name}': {str(e)}")
            raise

# Create a singleton instance
template_manager = EmailTemplateManager()