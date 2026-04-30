-- === ТВОИ ОРИГИНАЛЬНЫЕ ПРОЦЕДУРЫ (БЕЗ ИЗМЕНЕНИЙ) ===

-- Процедура Upsert
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phonebook (first_name, phone) 
    VALUES (p_name, p_phone)
    ON CONFLICT (phone) DO UPDATE SET first_name = EXCLUDED.first_name;
END;
$$;

-- Процедура Delete
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE first_name = p_identifier OR phone = p_identifier;
END;
$$;


-- === НОВЫЕ ПРОЦЕДУРЫ ДЛЯ TSIS 1 (ДОБАВЛЕНО) ===

-- Добавление телефона
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE first_name = p_contact_name LIMIT 1;
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE EXCEPTION 'Контакт % не найден', p_contact_name;
    END IF;
END;
$$;

-- Перемещение в группу
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- Ищем группу, если нет - создаем
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF NOT FOUND THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    -- Обновляем контакт
    UPDATE phonebook SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$;