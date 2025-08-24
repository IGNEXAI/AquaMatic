import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from src.services.models import Report

# Set up Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(template_dir))


def generate_report(report: Report, template_name='default') -> bytes:
    """
    Generates a PDF report from a Report object and returns it as bytes.

    :param report: A Report object containing the data for the report.
    :param template_name: The name of the template directory to use.
    :return: The generated PDF as a bytes object.
    """
    try:
        # Load the template and stylesheet
        template = env.get_template(f'{template_name}/report.html')
        css_path = os.path.join(template_dir, template_name, 'style.css')

        # Prepare data context for the template, adapting the model to the template's expectations
        # report_dict = report.model_dump()
        context_data = {
            'current_date': report.report_date.isoformat(),
            'is_valid': report.overall_valid,
            'issues': report.issues,
            'parameters': [],
            # These would typically come from a config file
            'logo_url': 'https://example.com/aqualimelabs_logo.png',
            'company_name': 'AquaLimeLabs'
        }

        # Adapt each parameter to match the template's variable names
        for param in report.parameters:
            context_data['parameters'].append({
                'name': param.name,
                'value': f"{param.value} {param.unit}",
                'range': f"{param.min_accepted_val} - {param.max_accepted_val} {param.unit}",
                'is_valid': param.is_acceptable,
                'comment': param.comment
            })

        # Render the HTML with the prepared data
        html_string = template.render(context_data)

        # Create a WeasyPrint HTML object
        html = HTML(string=html_string)

        # Create a WeasyPrint CSS object
        font_config = FontConfiguration()
        css = CSS(filename=css_path, font_config=font_config)

        # Write the PDF to a bytes object in memory
        pdf_bytes = html.write_pdf(stylesheets=[css], font_config=font_config)

        print("Report generated successfully in memory.")
        return pdf_bytes

    except Exception as e:
        print(f"Error generating report: {e}")
        return None


if __name__ == '__main__':
    # This block will be updated in the next step to show the full workflow
    pass
