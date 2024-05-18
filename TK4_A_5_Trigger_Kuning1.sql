CREATE OR REPLACE FUNCTION manage_premium_subscription()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM TRANSACTION
        WHERE email = NEW.email
        AND timestamp_berakhir > NOW()
    ) THEN
        RAISE EXCEPTION 'Pengguna telah berstatus premium.';
    ELSE

        IF NOT EXISTS (
            SELECT 1 FROM PREMIUM WHERE email = NEW.email
        ) THEN
    
            INSERT INTO PREMIUM (email) VALUES (NEW.email);
        END IF;
        

        DELETE FROM NONPREMIUM WHERE email = NEW.email;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_manage_premium_before_insert
BEFORE INSERT ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION manage_premium_subscription();