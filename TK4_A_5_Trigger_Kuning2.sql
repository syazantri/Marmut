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