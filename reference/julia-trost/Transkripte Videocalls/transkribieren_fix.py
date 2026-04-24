import subprocess
import os
import sys
import json
import tempfile
from openai import OpenAI

API_KEY = "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"
client = OpenAI(api_key=API_KEY)

# Alle 221 Videos aus Batch 2 - das Skript prueft automatisch welche noch fehlen
URLS = [
    "https://player.vimeo.com/video/1000037620",
    "https://player.vimeo.com/video/1003946602",
    "https://player.vimeo.com/video/1007690812",
    "https://player.vimeo.com/video/1009236254",
    "https://player.vimeo.com/video/1014261125",
    "https://player.vimeo.com/video/1014296103",
    "https://player.vimeo.com/video/1014686992",
    "https://player.vimeo.com/video/1014871130",
    "https://player.vimeo.com/video/1017503919",
    "https://player.vimeo.com/video/1017513794",
    "https://player.vimeo.com/video/1017545889",
    "https://player.vimeo.com/video/1020912491",
    "https://player.vimeo.com/video/1022107265",
    "https://player.vimeo.com/video/1022848669",
    "https://player.vimeo.com/video/1025914789",
    "https://player.vimeo.com/video/1026036728",
    "https://player.vimeo.com/video/1026117646",
    "https://player.vimeo.com/video/1026178104",
    "https://player.vimeo.com/video/1026536681",
    "https://player.vimeo.com/video/1026546372",
    "https://player.vimeo.com/video/1026573258",
    "https://player.vimeo.com/video/1027157203",
    "https://player.vimeo.com/video/1027715035",
    "https://player.vimeo.com/video/1027902640",
    "https://player.vimeo.com/video/1028287161",
    "https://player.vimeo.com/video/1035903876",
    "https://player.vimeo.com/video/1043881886",
    "https://player.vimeo.com/video/1044587828",
    "https://player.vimeo.com/video/1053318032",
    "https://player.vimeo.com/video/1053347219",
    "https://player.vimeo.com/video/1053443336",
    "https://player.vimeo.com/video/1054045040",
    "https://player.vimeo.com/video/1054120643",
    "https://player.vimeo.com/video/1055861975",
    "https://player.vimeo.com/video/1055876670",
    "https://player.vimeo.com/video/1055889779",
    "https://player.vimeo.com/video/1060027096",
    "https://player.vimeo.com/video/1065031335",
    "https://player.vimeo.com/video/1066498610",
    "https://player.vimeo.com/video/1066521914",
    "https://player.vimeo.com/video/1066665837",
    "https://player.vimeo.com/video/1066736133",
    "https://player.vimeo.com/video/1066982978",
    "https://player.vimeo.com/video/1069192815",
    "https://player.vimeo.com/video/1069197080",
    "https://player.vimeo.com/video/1069201165",
    "https://player.vimeo.com/video/1072034532",
    "https://player.vimeo.com/video/1074239216",
    "https://player.vimeo.com/video/1096736223",
    "https://player.vimeo.com/video/1098005543",
    "https://player.vimeo.com/video/1098431332",
    "https://player.vimeo.com/video/1107338188",
    "https://player.vimeo.com/video/1115299032",
    "https://player.vimeo.com/video/1126565296",
    "https://player.vimeo.com/video/1126594233",
    "https://player.vimeo.com/video/1135255761",
    "https://player.vimeo.com/video/1136433073",
    "https://player.vimeo.com/video/1136433103",
    "https://player.vimeo.com/video/1136433149",
    "https://player.vimeo.com/video/1136433211",
    "https://player.vimeo.com/video/1136433246",
    "https://player.vimeo.com/video/1136433303",
    "https://player.vimeo.com/video/1136435821",
    "https://player.vimeo.com/video/1136445276",
    "https://player.vimeo.com/video/1136452733",
    "https://player.vimeo.com/video/1136461685",
    "https://player.vimeo.com/video/1136462281",
    "https://player.vimeo.com/video/1136462341",
    "https://player.vimeo.com/video/1143329299",
    "https://player.vimeo.com/video/1143329339",
    "https://player.vimeo.com/video/1143329383",
    "https://player.vimeo.com/video/1143366264",
    "https://player.vimeo.com/video/1143377587",
    "https://player.vimeo.com/video/1143383868",
    "https://player.vimeo.com/video/1143384981",
    "https://player.vimeo.com/video/1143388646",
    "https://player.vimeo.com/video/1143429790",
    "https://player.vimeo.com/video/1144823795",
    "https://player.vimeo.com/video/1154488914",
    "https://player.vimeo.com/video/1169872897",
    "https://player.vimeo.com/video/1169935849",
    "https://player.vimeo.com/video/1169954499",
    "https://player.vimeo.com/video/1170232181",
    "https://player.vimeo.com/video/1170232222",
    "https://player.vimeo.com/video/1170232261",
    "https://player.vimeo.com/video/1170232380",
    "https://player.vimeo.com/video/1170232419",
    "https://player.vimeo.com/video/1170232446",
    "https://player.vimeo.com/video/1170232478",
    "https://player.vimeo.com/video/1170232496",
    "https://player.vimeo.com/video/1170232559",
    "https://player.vimeo.com/video/1170232580",
    "https://player.vimeo.com/video/1170266970",
    "https://player.vimeo.com/video/1170267001",
    "https://player.vimeo.com/video/1170270002",
    "https://player.vimeo.com/video/1170271840",
    "https://player.vimeo.com/video/1170273262",
    "https://player.vimeo.com/video/841903915",
    "https://player.vimeo.com/video/844368914",
    "https://player.vimeo.com/video/844380959",
    "https://player.vimeo.com/video/844382023",
    "https://player.vimeo.com/video/844392125",
    "https://player.vimeo.com/video/844624345",
    "https://player.vimeo.com/video/844656610",
    "https://player.vimeo.com/video/844662340",
    "https://player.vimeo.com/video/844718172",
    "https://player.vimeo.com/video/844953495",
    "https://player.vimeo.com/video/844956039",
    "https://player.vimeo.com/video/849214877",
    "https://player.vimeo.com/video/849889673",
    "https://player.vimeo.com/video/849891724",
    "https://player.vimeo.com/video/849948822",
    "https://player.vimeo.com/video/849959535",
    "https://player.vimeo.com/video/852442453",
    "https://player.vimeo.com/video/852774447",
    "https://player.vimeo.com/video/853366088",
    "https://player.vimeo.com/video/853388909",
    "https://player.vimeo.com/video/853389464",
    "https://player.vimeo.com/video/854121752",
    "https://player.vimeo.com/video/854609454",
    "https://player.vimeo.com/video/854655129",
    "https://player.vimeo.com/video/854674681",
    "https://player.vimeo.com/video/854694919",
    "https://player.vimeo.com/video/854775472",
    "https://player.vimeo.com/video/855678717",
    "https://player.vimeo.com/video/863930830",
    "https://player.vimeo.com/video/863931657",
    "https://player.vimeo.com/video/863933474",
    "https://player.vimeo.com/video/863934434",
    "https://player.vimeo.com/video/863935946",
    "https://player.vimeo.com/video/864843168",
    "https://player.vimeo.com/video/864852770",
    "https://player.vimeo.com/video/871122952",
    "https://player.vimeo.com/video/871124084",
    "https://player.vimeo.com/video/871510068",
    "https://player.vimeo.com/video/871580937",
    "https://player.vimeo.com/video/872184068",
    "https://player.vimeo.com/video/872597804",
    "https://player.vimeo.com/video/872602710",
    "https://player.vimeo.com/video/872608338",
    "https://player.vimeo.com/video/875635484",
    "https://player.vimeo.com/video/884490289",
    "https://player.vimeo.com/video/886966360",
    "https://player.vimeo.com/video/892608849",
    "https://player.vimeo.com/video/893673801",
    "https://player.vimeo.com/video/901099611",
    "https://player.vimeo.com/video/904720700",
    "https://player.vimeo.com/video/915550520",
    "https://player.vimeo.com/video/916652420",
    "https://player.vimeo.com/video/920175841",
    "https://player.vimeo.com/video/921939269",
    "https://player.vimeo.com/video/929059738",
    "https://player.vimeo.com/video/929066537",
    "https://player.vimeo.com/video/929070213",
    "https://player.vimeo.com/video/929071473",
    "https://player.vimeo.com/video/929538402",
    "https://player.vimeo.com/video/932520468",
    "https://player.vimeo.com/video/934805003",
    "https://player.vimeo.com/video/945764918",
    "https://player.vimeo.com/video/952276873",
    "https://player.vimeo.com/video/952277147",
    "https://player.vimeo.com/video/952277321",
    "https://player.vimeo.com/video/953120178",
    "https://player.vimeo.com/video/953141030",
    "https://player.vimeo.com/video/953143920",
    "https://player.vimeo.com/video/959526060",
    "https://player.vimeo.com/video/959536182",
    "https://player.vimeo.com/video/965174200",
    "https://player.vimeo.com/video/965180105",
    "https://player.vimeo.com/video/979850986",
    "https://player.vimeo.com/video/979875142",
    "https://player.vimeo.com/video/979940034",
    "https://player.vimeo.com/video/979976552",
    "https://player.vimeo.com/video/980025035",
    "https://player.vimeo.com/video/980041698",
    "https://player.vimeo.com/video/980049838",
    "https://player.vimeo.com/video/981085783",
    "https://player.vimeo.com/video/981099932",
    "https://player.vimeo.com/video/981855276",
    "https://player.vimeo.com/video/981942673",
    "https://player.vimeo.com/video/983503447",
    "https://player.vimeo.com/video/983822315",
    "https://player.vimeo.com/video/983822834",
    "https://player.vimeo.com/video/983840955",
    "https://player.vimeo.com/video/984218050",
    "https://player.vimeo.com/video/984340642",
    "https://player.vimeo.com/video/984341618",
    "https://player.vimeo.com/video/984347802",
    "https://player.vimeo.com/video/984361976",
    "https://player.vimeo.com/video/984369720",
    "https://player.vimeo.com/video/984455824",
    "https://player.vimeo.com/video/984777808",
    "https://player.vimeo.com/video/984778671",
    "https://player.vimeo.com/video/984796697",
    "https://player.vimeo.com/video/984809103",
    "https://player.vimeo.com/video/985588898",
    "https://player.vimeo.com/video/985626305",
    "https://player.vimeo.com/video/985631251",
    "https://player.vimeo.com/video/985635046",
    "https://player.vimeo.com/video/985639064",
    "https://player.vimeo.com/video/985642860",
    "https://player.vimeo.com/video/985646680",
    "https://player.vimeo.com/video/986325219",
    "https://player.vimeo.com/video/986326264",
    "https://player.vimeo.com/video/986335263",
    "https://player.vimeo.com/video/986395522",
    "https://player.vimeo.com/video/986989597",
    "https://player.vimeo.com/video/987282091",
    "https://player.vimeo.com/video/987290548",
    "https://player.vimeo.com/video/987292172",
    "https://player.vimeo.com/video/987300720",
    "https://player.vimeo.com/video/987543168",
    "https://player.vimeo.com/video/987581694",
    "https://player.vimeo.com/video/987582368",
    "https://player.vimeo.com/video/992728618",
    "https://player.vimeo.com/video/993012147",
    "https://player.vimeo.com/video/995697979",
    "https://player.vimeo.com/video/996982384",
    "https://player.vimeo.com/video/998337269",
    "https://player.vimeo.com/video/998563028",
    "https://player.vimeo.com/video/999801391",
]

AUSGABE = os.path.dirname(os.path.abspath(__file__))
FERTIG_DATEI = os.path.join(AUSGABE, "_fertig.txt")
MAX_SIZE = 24 * 1024 * 1024  # 24MB - sicher unter dem 25MB Limit

def lade_fertige():
    if not os.path.exists(FERTIG_DATEI):
        return set()
    with open(FERTIG_DATEI, "r") as f:
        return set(line.strip() for line in f if line.strip())

def speichere_fertig(url):
    with open(FERTIG_DATEI, "a") as f:
        f.write(url + "\n")

def download_audio(url, ausgabe_pfad):
    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "-x", "--audio-format", "mp3",
        "--audio-quality", "5",
        "-o", ausgabe_pfad,
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FEHLER Download: {result.stderr[:200]}")
        return False
    return True

def finde_audio_datei(ausgabe_pfad, video_id):
    """Findet die tatsaechliche Audio-Datei (yt-dlp benennt manchmal um)"""
    if os.path.exists(ausgabe_pfad):
        return ausgabe_pfad
    if os.path.exists(ausgabe_pfad + ".mp3"):
        return ausgabe_pfad + ".mp3"
    verzeichnis = os.path.dirname(ausgabe_pfad)
    for f in os.listdir(verzeichnis):
        if f.startswith(f"temp_{video_id}") and (f.endswith(".mp3") or f.endswith(".m4a") or f.endswith(".opus")):
            return os.path.join(verzeichnis, f)
    return None

def split_audio(audio_pfad, video_id):
    """Splittet Audio in Chunks unter 24MB mit ffmpeg"""
    dateig = os.path.getsize(audio_pfad)
    if dateig <= MAX_SIZE:
        return [audio_pfad]

    # Berechne wie viele Teile wir brauchen
    anzahl_teile = (dateig // MAX_SIZE) + 1

    # Hole Gesamtdauer mit ffprobe
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", audio_pfad]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback: schaetze Dauer basierend auf Dateigroesse (~128kbps)
        dauer = dateig / (128 * 1024 / 8)
    else:
        dauer = float(result.stdout.strip())

    teil_dauer = dauer / anzahl_teile

    print(f"  Datei zu gross ({dateig/1024/1024:.1f}MB) - splitte in {anzahl_teile} Teile...")

    teile = []
    for i in range(anzahl_teile):
        start = i * teil_dauer
        teil_pfad = os.path.join(AUSGABE, f"temp_{video_id}_teil{i+1}.mp3")
        cmd = [
            "ffmpeg", "-y", "-i", audio_pfad,
            "-ss", str(start), "-t", str(teil_dauer),
            "-acodec", "libmp3lame", "-ab", "64k",
            teil_pfad
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists(teil_pfad):
            teile.append(teil_pfad)
        else:
            print(f"  FEHLER beim Splitten von Teil {i+1}")

    return teile

def transkribiere_whisper_api(audio_pfad, video_id):
    """Transkribiert eine einzelne Datei oder splittet sie bei Bedarf"""
    try:
        dateig = os.path.getsize(audio_pfad)

        if dateig > MAX_SIZE:
            # Datei zu gross - splitten
            teile = split_audio(audio_pfad, video_id)
            if not teile:
                print(f"  FEHLER: Konnte Audio nicht splitten")
                return False

            gesamt_text = []
            alle_segmente = []
            zeit_offset = 0

            for i, teil in enumerate(teile):
                print(f"  Transkribiere Teil {i+1}/{len(teile)}...")
                with open(teil, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"
                    )

                gesamt_text.append(transcript.text)

                for seg in transcript.segments:
                    alle_segmente.append({
                        "start": seg.start + zeit_offset,
                        "end": seg.end + zeit_offset,
                        "text": seg.text
                    })

                # Offset fuer naechsten Teil
                if transcript.segments:
                    zeit_offset += transcript.segments[-1].end

                # Cleanup Teil
                try:
                    os.remove(teil)
                except:
                    pass

            # Speichere kombiniertes Ergebnis
            basis = os.path.join(AUSGABE, video_id)

            with open(basis + ".txt", "w", encoding="utf-8") as f:
                f.write(" ".join(gesamt_text))

            with open(basis + ".json", "w", encoding="utf-8") as f:
                json.dump({"text": " ".join(gesamt_text), "segments": alle_segmente}, f, ensure_ascii=False, indent=2)

            with open(basis + ".srt", "w", encoding="utf-8") as f:
                for i, seg in enumerate(alle_segmente, 1):
                    start = format_time_srt(seg["start"])
                    end = format_time_srt(seg["end"])
                    f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")

            with open(basis + ".vtt", "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                for i, seg in enumerate(alle_segmente, 1):
                    start = format_time_vtt(seg["start"])
                    end = format_time_vtt(seg["end"])
                    f.write(f"{start} --> {end}\n{seg['text'].strip()}\n\n")

            with open(basis + ".tsv", "w", encoding="utf-8") as f:
                f.write("start\tend\ttext\n")
                for seg in alle_segmente:
                    f.write(f"{int(seg['start']*1000)}\t{int(seg['end']*1000)}\t{seg['text'].strip()}\n")

            return True

        else:
            # Datei klein genug - normal transkribieren
            with open(audio_pfad, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )

            basis = os.path.join(AUSGABE, video_id)

            with open(basis + ".txt", "w", encoding="utf-8") as f:
                f.write(transcript.text)

            with open(basis + ".json", "w", encoding="utf-8") as f:
                json.dump({"text": transcript.text, "segments": [{"start": s.start, "end": s.end, "text": s.text} for s in transcript.segments]}, f, ensure_ascii=False, indent=2)

            with open(basis + ".srt", "w", encoding="utf-8") as f:
                for i, seg in enumerate(transcript.segments, 1):
                    start = format_time_srt(seg.start)
                    end = format_time_srt(seg.end)
                    f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")

            with open(basis + ".vtt", "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                for i, seg in enumerate(transcript.segments, 1):
                    start = format_time_vtt(seg.start)
                    end = format_time_vtt(seg.end)
                    f.write(f"{start} --> {end}\n{seg.text.strip()}\n\n")

            with open(basis + ".tsv", "w", encoding="utf-8") as f:
                f.write("start\tend\ttext\n")
                for seg in transcript.segments:
                    f.write(f"{int(seg.start*1000)}\t{int(seg.end*1000)}\t{seg.text.strip()}\n")

            return True

    except Exception as e:
        print(f"  FEHLER Transkription: {e}")
        return False

def format_time_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_time_vtt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

if __name__ == "__main__":
    fertige = lade_fertige()
    gesamt = len(URLS)
    uebersprungen = 0
    neu_fertig = 0
    fehler = 0

    print(f"=== Julia Trost Transkription (Fix-Runde - mit Splitting) ===")
    print(f"Gesamt: {gesamt} Videos")
    print(f"Bereits fertig: {len(fertige)}")
    print(f"Zu große Dateien werden automatisch gesplittet!\n")

    for i, url in enumerate(URLS, 1):
        video_id = url.split("/")[-1]

        if url in fertige:
            uebersprungen += 1
            continue

        print(f"[{i}/{gesamt}] Video {video_id}...")

        audio_pfad = os.path.join(AUSGABE, f"temp_{video_id}.mp3")

        # Download
        print(f"  Downloade...")
        if not download_audio(url, audio_pfad):
            fehler += 1
            continue

        # Finde die tatsaechliche Datei
        actual_file = finde_audio_datei(audio_pfad, video_id)

        if not actual_file:
            print(f"  FEHLER: Audio-Datei nicht gefunden")
            fehler += 1
            continue

        # Transkribiere (mit automatischem Splitting bei Bedarf)
        print(f"  Transkribiere mit Whisper API...")
        if transkribiere_whisper_api(actual_file, video_id):
            neu_fertig += 1
            speichere_fertig(url)
            print(f"  FERTIG!")
        else:
            fehler += 1

        # Cleanup
        try:
            os.remove(actual_file)
        except:
            pass

    print(f"\n=== ERGEBNIS ===")
    print(f"Übersprungen (bereits fertig): {uebersprungen}")
    print(f"Neu transkribiert: {neu_fertig}")
    print(f"Fehler: {fehler}")
    print(f"Gesamt fertig: {uebersprungen + neu_fertig}/{gesamt}")
