CREATE OR REPLACE FUNCTION merah_update_podcast_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE konten
        SET durasi = durasi + NEW.durasi
        WHERE id = NEW.id_konten_podcast;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE konten
        SET durasi = durasi - OLD.durasi
        WHERE id = OLD.id_konten_podcast;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER merah_update_podcast_duration_trigger
AFTER INSERT OR DELETE ON episode
FOR EACH ROW
EXECUTE FUNCTION merah_update_podcast_duration();

CREATE OR REPLACE FUNCTION merah_1_update_album()
RETURNS TRIGGER AS $$

DECLARE
durasi_baru integer;

BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT durasi from konten
        WHERE id = NEW.id_konten into durasi_baru;

        BEGIN
        UPDATE album
        SET total_durasi = total_durasi + durasi_baru,
        jumlah_lagu = jumlah_lagu + 1
        WHERE id = NEW.id_album;
        END;
    ELSIF TG_OP = 'DELETE' THEN
        SELECT durasi from konten
        WHERE id = old.id_konten into durasi_baru;

        BEGIN
        UPDATE album
        SET total_durasi = total_durasi - durasi_baru,
        jumlah_lagu = jumlah_lagu - 1
        WHERE id = OLD.id_album;
        END;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER merah_1_update_album_trigger
AFTER INSERT OR DELETE ON SONG
FOR EACH ROW
EXECUTE FUNCTION merah_1_update_album();