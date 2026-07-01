import os, re
tpl_dir = r"d:\Internship\internproject\smartcollege\staff\student\templates"
files = [
    "take_attendance.html", "assignment.html", "view_submission.html", 
    "view_staff_announcements.html", "study_materials.html", "notifications.html", 
    "view_attendance.html", "view_timetable.html", "view_student_timetable.html", 
    "view_feedback.html", "view_student.html", "attendance.html"
]

for f in files:
    p = os.path.join(tpl_dir, f)
    if not os.path.exists(p): continue
    with open(p, "r", encoding="utf-8") as file:
        content = file.read()
    
    if "class=\"main-content\"" not in content and "class='main-content'" not in content:
        content = re.sub(r'({%\s*include\s+[\'"][^\'"]+_menu\.html[\'"]\s*%})', r'\1\n<div class="main-content">', content)
        content = content.replace("</body>", "</div>\n</body>")
        with open(p, "w", encoding="utf-8") as file:
            file.write(content)

print("Wrapped missing main-contents!")
