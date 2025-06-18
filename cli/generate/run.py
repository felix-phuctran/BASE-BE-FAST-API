#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from pybars import Compiler

# Suppose you import utils/string_case.py like below
# (Adjust the import path according to your project)
from utils.string_case import singularize, to_camel, to_snake_case


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python files from Handlebars templates."
    )
    parser.add_argument(
        "module_name", help="Module name in snake_case (e.g. membership_package)"
    )
    args = parser.parse_args()

    generate_files(args.module_name)


def generate_files(module_name: str):
    """
    Main function to:
      - Build context (name_sing, model, names, databases).
      - Compile .hbs templates.
      - Write out the corresponding .py files.
    """

    # Get the base path to the "generate" folder (where run.py is located)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # The template directory is the same folder "cli/generate"
    templates_dir = base_dir

    # Get the project's root directory "global-api"
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))

    # Process context
    # 1) Convert module_name to snake_case
    snake_name = to_snake_case(module_name)  # e.g. "membership_package"
    # 2) Singularize
    name_sing = singularize(
        snake_name
    )  # e.g. "membership_package" (if it was "membership_packages" => "membership_package")
    # 3) Create PascalCase
    model = to_camel(name_sing)  # e.g. "MembershipPackage"
    # 4) Create a plural form
    names = f"{name_sing}s"  # e.g. "membership_packages"
    databases = to_camel(names)  # e.g. "MembershipPackages"

    context = {
        "name": snake_name,  # "membership_package"
        "name_sing": name_sing,  # "membership_package"
        "model": model,  # "MembershipPackage"
        "names": names,  # "membership_packages"
        "databases": databases,  # "MembershipPackages"
    }

    # Define a list of templates and destination files
    # Note: template files are placed under `templates_dir` (== `base_dir`),
    # while output files are generated under `project_root`.
    template_output_map = [
        (
            "schema/base/{{name_sing}}_base_schema.hbs",
            "schema/base/{{name_sing}}_base_schema.py",
        ),
        (
            "schema/builder/{{name_sing}}_builder_schema.hbs",
            "schema/builder/{{name_sing}}_builder_schema.py",
        ),
        (
            "schema/request/{{name_sing}}_request_schema.hbs",
            "schema/request/{{name_sing}}_request_schema.py",
        ),
        (
            "schema/response/{{name_sing}}_response_schema.hbs",
            "schema/response/{{name_sing}}_response_schema.py",
        ),
        (
            "services/abstract/{{name_sing}}_service.hbs",
            "services/abstract/{{name_sing}}_service.py",
        ),
        (
            "services/implement/{{name_sing}}_service_impl.hbs",
            "services/implement/{{name_sing}}_service_impl.py",
        ),
        (
            "repositories/orm/orm_crud_{{name_sing}}.hbs",
            "repositories/orm/orm_crud_{{name_sing}}.py",
        ),
        ("api/v1/endpoints/{{name_sing}}.hbs", "api/v1/endpoints/{{name_sing}}.py"),
    ]

    compiler = Compiler()

    for template_rel_path, output_rel_path in template_output_map:
        # Build the full path for the template file
        template_path = os.path.join(templates_dir, template_rel_path)
        if not os.path.exists(template_path):
            print(f"❌ Template does not exist: {template_path}")
            continue

        # Read template content
        with open(template_path, "r", encoding="utf-8") as f:
            template_str = f.read()

        # Compile the template
        template_compiled = compiler.compile(template_str)

        # Render using context
        rendered_str = template_compiled(context)

        # Build output path. Replace {{name_sing}} in the path
        output_file_rel = template_rel_path_to_output(output_rel_path, name_sing)
        output_file_abs = os.path.join(project_root, output_file_rel)

        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(output_file_abs), exist_ok=True)

        # Write the file
        with open(output_file_abs, "w", encoding="utf-8") as out_f:
            out_f.write(rendered_str)

        print(f"✔ Generated: {output_file_abs}")


def template_rel_path_to_output(path_pattern: str, name_sing: str) -> str:
    """
    Replace {{name_sing}} in path_pattern
    """
    return path_pattern.replace("{{name_sing}}", name_sing)


if __name__ == "__main__":
    main()
