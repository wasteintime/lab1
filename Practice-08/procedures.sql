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