CREATE TRIGGER IF NOT EXISTS after_admin_insert
            AFTER INSERT ON admin
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.id, NULL, 3, ip, active);
            END;
/

CREATE TRIGGER IF NOT EXISTS after_proff_insert
            AFTER INSERT ON proff
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.p_id, NULL, 2, ip, active);
            END;
/

CREATE TRIGGER IF NOT EXISTS after_student_insert
            AFTER INSERT ON student
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.s_id, NULL, 1, ip, active);
            END;