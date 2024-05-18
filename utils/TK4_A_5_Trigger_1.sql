CREATE OR REPLACE FUNCTION putih_pengecekan_email()
RETURNS trigger AS
$$
	BEGIN
	IF((SELECT COUNT(*) FROM akun as a WHERE a.EMAIL = NEW.EMAIL) >= 1 OR
	   (SELECT COUNT(*) FROM label as l WHERE l.EMAIL = NEW.EMAIL) >= 1)
	THEN 
	RAISE EXCEPTION 'Sudah ada akun yang menggunakan email ini, silahkan coba gunakan email lain';
	END IF;
	RETURN NEW;
	END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER putih_akun_pengecekan_email_trigger
BEFORE INSERT ON akun 
FOR EACH ROW EXECUTE FUNCTION putih_pengecekan_email();

CREATE TRIGGER putih_label_pengecekan_email_trigger
BEFORE INSERT ON label
FOR EACH ROW EXECUTE FUNCTION putih_pengecekan_email();

CREATE OR REPLACE FUNCTION putih_pendaftaran_pengguna_baru()
RETURNS trigger AS
$$
	BEGIN
	INSERT INTO nonpremium (email) VALUES (NEW.email)
	RETURN NEW;
	END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER  putih_pendaftaran_pengguna_baru_trigger
AFTER INSERT ON akun
FOR EACH ROW EXECUTE FUNCTION putih_pendaftaran_pengguna_baru();

CREATE FUNCTION putih_cekStatusLangganan(email_param VARCHAR(50)) RETURNS INT AS
$$

    DECLARE yaampun_status_code INT;
BEGIN
    IF EXISTS (SELECT 1 FROM PREMIUM as p WHERE p.email = email_param) THEN
        IF EXISTS (SELECT 1 FROM TRANSACTION as t WHERE t.email = email_param AND timestamp_berakhir > NOW()) THEN
            yaampun_status_code := 0; 
        ELSE
            yaampun_status_code := 1; 
        END IF;
    ELSE
        yaampun_status_code := -1; 
    END IF;
    
    RETURN yaampun_status_code;

END;
$$ LANGUAGE plpgsql;