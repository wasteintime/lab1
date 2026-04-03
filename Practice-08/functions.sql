-- Поиск
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_search TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.phone FROM phonebook c
    WHERE c.first_name ILIKE '%' || p_search || '%' OR c.phone ILIKE '%' || p_search || '%';
END;
$$ LANGUAGE plpgsql;

-- Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT * FROM phonebook ORDER BY id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Массовая вставка с валидацией
CREATE OR REPLACE FUNCTION insert_many_contacts(p_names VARCHAR[], p_phones VARCHAR[])
RETURNS TABLE(failed_name VARCHAR, failed_phone VARCHAR, reason TEXT) AS $$
DECLARE i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{10,15}$' THEN
            INSERT INTO phonebook (first_name, phone) VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone) DO UPDATE SET first_name = EXCLUDED.first_name;
        ELSE
            failed_name := p_names[i]; failed_phone := p_phones[i];
            reason := 'Некорректный формат телефона';
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;