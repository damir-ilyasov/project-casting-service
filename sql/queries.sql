-- 1. Все проекты по алфавиту
SELECT id, name FROM projects ORDER BY name;

-- 2. Поиск проектов по части названия (параметр :query)
SELECT id, name FROM projects WHERE name LIKE '%' || :query || '%' ORDER BY name;

-- 3. Роли конкретного проекта (параметр :project_id)
SELECT id, name FROM roles WHERE project_id = :project_id ORDER BY id;

-- 4. Заявки со статусом (параметр :status)
SELECT id, project_id, role_id, candidate_id, status
FROM applications WHERE status = :status ORDER BY id DESC;

-- 5. JOIN: заявки с именами кандидатов, проектов и ролей
SELECT a.id, c.name AS candidate_name, p.name AS project_name,
       r.name AS role_name, a.status
FROM applications a
JOIN candidates c ON c.id = a.candidate_id
JOIN projects p ON p.id = a.project_id
JOIN roles r ON r.project_id = a.project_id AND r.id = a.role_id
ORDER BY a.id;

-- 6. Количество ролей в каждом проекте (GROUP BY)
SELECT p.id, p.name, COUNT(r.id) AS role_count
FROM projects p LEFT JOIN roles r ON r.project_id = p.id
GROUP BY p.id, p.name ORDER BY role_count DESC, p.name;

-- 7. Проекты, в которых не менее двух ролей (HAVING)
SELECT p.id, p.name, COUNT(r.id) AS role_count
FROM projects p JOIN roles r ON r.project_id = p.id
GROUP BY p.id, p.name HAVING COUNT(r.id) >= 2;

-- 8. Количество заявок по каждому статусу
SELECT status, COUNT(*) AS application_count
FROM applications GROUP BY status ORDER BY application_count DESC;

-- 9. Кандидаты с количеством их заявок
SELECT c.id, c.name, COUNT(a.id) AS application_count
FROM candidates c LEFT JOIN applications a ON a.candidate_id = c.id
GROUP BY c.id, c.name ORDER BY application_count DESC, c.name;

-- 10. Последние пять заявок
SELECT id, project_id, role_id, candidate_id, status
FROM applications ORDER BY id DESC LIMIT 5;

-- 11. Заявки проекта (параметр :project_id), от новых к старым
SELECT id, project_id, role_id, candidate_id, status
FROM applications WHERE project_id = :project_id ORDER BY id DESC;

-- 12. Свободные роли: нет принятой заявки
SELECT r.project_id, r.id AS role_id, r.name AS role_name, p.name AS project_name
FROM roles r JOIN projects p ON p.id = r.project_id
WHERE NOT EXISTS (
    SELECT 1 FROM applications a
    WHERE a.project_id = r.project_id AND a.role_id = r.id AND a.status = 'accepted'
)
ORDER BY p.name, r.id;
