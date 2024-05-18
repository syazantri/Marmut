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

_______________________________________________________________________________________

CREATE OR REPLACE FUNCTION log_song_plays()
RETURNS TRIGGER AS $$
DECLARE
    song_id uuid;
BEGIN
    
    FOR song_id IN
        SELECT song_id FROM playlist_song WHERE id_playlist = NEW.id_user_playlist
    LOOP
        
        INSERT INTO akun_play_song (email_pemain, id_song, waktu)
        VALUES (NEW.email_pemain, song_id, NEW.waktu);
    END LOOP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_user_playlist_play
AFTER INSERT ON akun_play_user_playlist
FOR EACH ROW
EXECUTE FUNCTION log_song_plays();