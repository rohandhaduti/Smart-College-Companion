import os, re
tpl_dir = r'd:\\Internship\\internproject\\smartcollege\\staff\\student\\templates'
files = ['take_attendance.html', 'assignment.html', 'view_submission.html', 'view_staff_announcements.html', 'study_materials.html', 'notifications.html', 'view_attendance.html', 'view_timetable.html', 'view_student_timetable.html', 'view_feedback.html', 'view_student.html', 'admin_menu.html', 'staff_menu.html', 'student_menu.html']

for f in files:
    p = os.path.join(tpl_dir, f)
    if not os.path.exists(p): continue
    with open(p, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove <style>...</style> block
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    
    # Clean up old border=1 and align=center tags
    content = content.replace('border="1"', '')
    content = content.replace('border="2"', '')
    content = content.replace('align="center"', '')
    
    with open(p, 'w', encoding='utf-8') as file:
        file.write(content)
print("Done cleaning!")
