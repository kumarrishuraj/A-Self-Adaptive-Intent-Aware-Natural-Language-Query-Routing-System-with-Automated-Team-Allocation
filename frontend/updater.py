import os
import re
DEPARTMENTS = [
    ("Academics", "academics_dashboard.html", "📚", "Academics"),
    ("Admissions", "admissions_dashboard.html", "🎓", "Admissions"),
    ("Examination", "examination_dashboard.html", "📝", "Examination"),
    ("Fees_and_Account", "fees_and_account_dashboard.html", "💰", "Fees and Account"),
    ("International_Affair", "international_affair_dashboard.html", "🌍", "International affair"),
    ("IT", "it_dashboard.html", "💻", "IT"),
    ("Residential_Services", "residential_services_dashboard.html", "🏠", "Residential services"),
    ("Security_and_Safety", "security_and_safety_dashboard.html", "🛡️", "Security and safety"),
    ("Placements", "placements_dashboard.html", "💼", "Placements"),
    ("Division_of_Research_and_Development", "division_of_research_and_development_dashboard.html", "🔬", "Division of Research and Development"),
    ("Library", "library_dashboard.html", "📖", "Library"),
    ("HOD_ML", "hod_ml_dashboard.html", "🤖", "HOD ML"),
    ("HOD_MATH", "hod_math_dashboard.html", "📐", "HOD MATH"),
    ("EDU_REV", "edu_rev_dashboard.html", "📊", "EDU-REV")
]
SIDEBAR_HTML = """        <div class="sidebar-section">Student</div>
        <ul class="sidebar-nav">
            <li><a href="student_page.html"><span class="nav-icon">📝</span> Student Portal</a></li>
        </ul>

        <div class="sidebar-section">Dashboards</div>
        <ul class="sidebar-nav" style="max-height: 50vh; overflow-y: auto;">\n"""

for dept_id, file_name, icon, display_name in DEPARTMENTS:
    SIDEBAR_HTML += f'            <li><a href="{file_name}"><span class="nav-icon">{icon}</span> {display_name}</a></li>\n'
SIDEBAR_HTML += '        </ul>'

def update_sidebar(html_content, active_file):
    # Regex to find the whole sidebar from "Student" section to end of dashboards section
    pattern = re.compile(r'<div class="sidebar-section">Student</div>.*?(<div class="sidebar-footer">)', re.DOTALL)
    # Mark the active file
    new_sidebar = SIDEBAR_HTML
    if active_file:
        new_sidebar = SIDEBAR_HTML.replace(f'href="{active_file}"', f'href="{active_file}" class="active"')
    return pattern.sub(new_sidebar + r'\n        \1', html_content)

if __name__ == '__main__':
    BASE = os.path.dirname(os.path.abspath(__file__))
    # Read academics_dashboard.html as template
    with open(os.path.join(BASE, 'academics_dashboard.html'), 'r', encoding='utf-8') as f:
        template = f.read()
    # Generate and write all 14 dashboards
    for dept_id, file_name, icon, display_name in DEPARTMENTS:
        new_html = template
        # Replace the visual title
        new_html = new_html.replace('📚 <span class="gradient-text">Academics</span>', f'{icon} <span class="gradient-text">{display_name}</span>')
        # Replace the logic constant
        new_html = re.sub(r"const DEPT = 'Academics';", f"const DEPT = '{dept_id}';", new_html)
        # Replace the title tag
        new_html = re.sub(r"<title>Academics Dashboard — TicketFlow</title>", f"<title>{display_name} Dashboard — TicketFlow</title>", new_html)
        # Inject sidebar
        new_html = update_sidebar(new_html, file_name)
        
        with open(os.path.join(BASE, file_name), 'w', encoding='utf-8') as f:
            f.write(new_html)

    print("Dashboards generated.")

    # Update student_page.html sidebar
    student_path = os.path.join(BASE, 'student_page.html')
    if os.path.exists(student_path):
        with open(student_path, 'r', encoding='utf-8') as f:
            student_html = f.read()

        student_html = update_sidebar(student_html, "student_page.html")

        # Rewrite student page
        with open(student_path, 'w', encoding='utf-8') as f:
            f.write(student_html)
        print("student_page.html sidebar updated.")