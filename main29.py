import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import folium
from folium.plugins import HeatMap
import csv

# Definisci la variabile UPLOAD_FOLDER per una cartella temporanea
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_upload')

# Crea un'applicazione Flask
app = Flask(__name__, static_folder='static2')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'S3gret0'  # Imposta la chiave segreta

# Dati sui casi di crimine a Roma
initial_crimes = [
        ("Via Appia Nuova", 41.8736, 12.4834, "Furto"),
        ("Via Cavour", 41.8933, 12.4911, "Omicidio"),
        ("Via del Corso", 41.9022, 12.4809, "Aggressione"),
        ("Via Veneto", 41.9073, 12.4885, "Furto"),
        ("Via Nazionale", 41.9024, 12.4964, "Furto"),
        ("Via dei Fori Imperiali", 41.8919, 12.4874, "Aggressione"),
        ("Via Ostiense", 41.8692, 12.4849, "Furto"),
        ("Viale Trastevere", 41.8861, 12.4674, "Omicidio"),
        ("Via Tiburtina", 41.9105, 12.5345, "Furto"),
        ("Via Salaria", 41.9136, 12.4993, "Omicidio"),
        ("Via Flaminia", 41.9271, 12.4834, "Furto"),
        ("Via Appia Antica", 41.8519, 12.4973, "Aggressione"),
        ("Viale delle Milizie", 41.9093, 12.4662, "Furto"),
        ("Viale Regina Margherita", 41.9138, 12.5161, "Furto"),
        ("Viale Guglielmo Marconi", 41.8525, 12.4671, "Omicidio"),
        ("Viale Palmiro Togliatti", 41.8989, 12.5458, "Furto"),
        ("Via Cristoforo Colombo", 41.8496, 12.4788, "Aggressione"),
        ("Viale dei Romagnoli", 41.8602, 12.4769, "Furto"),
        ("Via della Conciliazione", 41.9023, 12.4545, "Omicidio"),
        ("Via del Tritone", 41.9007, 12.4881, "Furto"),
        ("Via Giulia", 41.8959, 12.4686, "Omicidio"),
        ("Via Margutta", 41.9067, 12.4815, "Furto"),
        ("Via del Babuino", 41.9061, 12.4801, "Aggressione"),
        ("Via della Lungara", 41.8963, 12.4657, "Furto"),
        ("Via del Governo Vecchio", 41.8998, 12.4709, "Furto"),
        ("Vicolo della Campanella", 41.8933, 12.4722, "Omicidio"),
        ("Via dei Giubbonari", 41.8944, 12.4718, "Furto"),
        ("Piazza del Popolo", 41.9105, 12.4768, "Furto"),
        ("Via del Corso", 41.9021, 12.4833, "Aggressione"),
        ("Via Nazionale", 41.9002, 12.4961, "Furto"),
        ("Via Appia Nuova", 41.8843, 12.5012, "Omicidio"),
        ("Via Tuscolana", 41.8762, 12.5234, "Furto"),
        ("Piazza Navona", 41.8992, 12.4735, "Aggressione"),
        ("Piazza Venezia", 41.8956, 12.4822, "Furto"),
        ("Piazza di Spagna", 41.9059, 12.4828, "Furto"),
        ("Viale Trastevere", 41.8796, 12.4671, "Omicidio"),
        ("Viale dei Castani", 41.9012, 12.4597, "Furto"),
        ("Viale Parioli", 41.9243, 12.4918, "Aggressione"),
        ("Viale Regina Elena", 41.9097, 12.5102, "Furto"),
        ("Via dei Fori Imperiali", 41.8911, 12.4883, "Omicidio"),
        ("Via della Conciliazione", 41.9021, 12.4549, "Furto"),
        ("Via della Lungara", 41.8948, 12.4643, "Furto"),
        ("Via del Babuino", 41.9076, 12.4799, "Aggressione"),
        ("Via dei Coronari", 41.8987, 12.4708, "Furto"),
        ("Via del Corso", 41.9008, 12.4845, "Omicidio"),
        ("Via Nazionale", 41.8992, 12.4968, "Furto"),
        ("Via Appia Nuova", 41.8862, 12.5034, "Furto"),
        ("Via Aurelia", 41.8984, 12.4261, "Aggressione"),
        ("Via Cassia", 41.9712, 12.4195, "Furto"),
        ("Via del Tritone", 41.9002, 12.4885, "Omicidio"),
        ("Via Veneto", 41.9063, 12.4873, "Furto"),
        ("Via dei Condotti", 41.9062, 12.4829, "Furto"),
        ("Via Margutta", 41.9078, 12.4819, "Aggressione"),
        ("Via della Croce", 41.9065, 12.4802, "Furto"),
        ("Via del Babuino", 41.9071, 12.4806, "Omicidio"),
        ("Via Giulia", 41.8969, 12.4681, "Furto"),
        ("Vicolo della Campanella", 41.8936, 12.4729, "Furto"),
        ("Vicolo dei Bovari", 41.8917, 12.4742, "Aggressione"),
        ("Vicolo delle Vacche", 41.8919, 12.4768, "Furto"),
        ("Vicolo del Cinque", 41.8944, 12.4785, "Furto"),
        ("Piazza Farnese", 41.8956, 12.4698, "Omicidio"),
        ("Piazza della Rotonda", 41.8993, 12.4767, "Furto"),
        ("Piazza della Minerva", 41.8987, 12.4778, "Aggressione"),
        ("Piazza Navona", 41.8982, 12.4739, "Furto"),
        ("Piazza di Pietra", 41.8996, 12.4795, "Omicidio"),
        ("Piazza Colonna", 41.9011, 12.4802, "Furto"),
        ("Piazza Venezia", 41.8962, 12.4833, "Furto"),
        ("Piazza del Popolo", 41.9108, 12.4764, "Aggressione"),
        ("Piazza di Spagna", 41.9056, 12.4829, "Furto"),
        ("Piazza della Repubblica", 41.9017, 12.4958, "Omicidio"),
        ("Piazza Barberini", 41.9036, 12.4886, "Furto"),
        ("Piazza Venezia", 41.8959, 12.4827, "Furto"),
        ("Piazza della Rotonda", 41.8998, 12.4765, "Aggressione"),
        ("Piazza Navona", 41.8981, 12.4736, "Furto"),
        ("Piazza di Spagna", 41.9061, 12.4825, "Omicidio"),
        ("Piazza del Popolo", 41.9103, 12.4761, "Furto"),
        ("Piazza Farnese", 41.8962, 12.4711, "Furto"),
        ("Piazza Colonna", 41.9009, 12.4804, "Aggressione"),
        ("Piazza di Pietra", 41.8995, 12.4799, "Furto"),
        ("Piazza Venezia", 41.8958, 12.4829, "Furto"),
        ("Piazza della Repubblica", 41.9021, 12.4956, "Aggressione"),
        ("Piazza Barberini", 41.9037, 12.4884, "Furto"),
        ("Piazza del Campidoglio", 41.8922, 12.4826, "Omicidio"),
        ("Piazza della Minerva", 41.8988, 12.4775, "Furto"),
        ("Piazza Navona", 41.8983, 12.4741, "Aggressione"),
        ("Piazza di Spagna", 41.9063, 12.4831, "Furto"),
        ("Piazza del Popolo", 41.9106, 12.4763, "Furto"),
        ("Piazza Farnese", 41.8961, 12.4715, "Omicidio"),
        ("Piazza Colonna", 41.9010, 12.4800, "Furto"),
        ("Piazza di Pietra", 41.8997, 12.4803, "Aggressione"),
        ("Piazza Venezia", 41.8957, 12.4828, "Furto"),
        ("Piazza della Repubblica", 41.9022, 12.4957, "Furto"),
        ("Piazza Barberini", 41.9038, 12.4882, "Aggressione"),
        ("Piazza del Campidoglio", 41.8923, 12.4827, "Furto"),
        ("Piazza della Minerva", 41.8987, 12.4774, "Furto"),
        ("Piazza Navona", 41.8984, 12.4740, "Omicidio"),
        ("Piazza di Spagna", 41.9064, 12.4830, "Furto"),
        ("Piazza del Popolo", 41.9105, 12.4762, "Aggressione"),
        ("Piazza Farnese", 41.8960, 12.4716, "Furto"),
        ("Piazza Colonna", 41.9009, 12.4801, "Furto"),
        ("Piazza di Pietra", 41.8996, 12.4804, "Aggressione"),
        ("Piazza Venezia", 41.8956, 12.4827, "Furto"),
        ("Piazza della Repubblica", 41.9021, 12.4955, "Omicidio"),
        ("Piazza Barberini", 41.9037, 12.4883, "Furto"),
        ("Piazza del Campidoglio", 41.8921, 12.4825, "Aggressione"),
        ("Piazza della Minerva", 41.8986, 12.4776, "Furto"),
        ("Piazza Navona", 41.8985, 12.4742, "Furto"),
        ("Piazza di Spagna", 41.9062, 12.4829, "Omicidio"),
        ("Piazza del Popolo", 41.9104, 12.4764, "Furto"),
        ("Piazza Farnese", 41.8962, 12.4714, "Furto"),
        ("Piazza Colonna", 41.9008, 12.4803, "Aggressione"),
        ("Piazza di Pietra", 41.8994, 12.4805, "Furto"),
        ("Piazza Venezia", 41.8955, 12.4828, "Furto"),
        ("Piazza della Repubblica", 41.9020, 12.4954, "Aggressione"),
        ("Piazza Barberini", 41.9036, 12.4885, "Furto"),
        ("Piazza del Campidoglio", 41.8924, 12.4828, "Omicidio"),
        ("Piazza della Minerva", 41.8989, 12.4773, "Furto"),
        ("Piazza Navona", 41.8982, 12.4743, "Aggressione"),
        ("Piazza di Spagna", 41.9061, 12.4831, "Furto"),
        ("Piazza del Popolo", 41.9103, 12.4765, "Furto"),
        ("Piazza Farnese", 41.8963, 12.4713, "Omicidio"),
        ("Piazza Colonna", 41.9007, 12.4802, "Furto"),
        ("Piazza di Pietra", 41.8993, 12.4806, "Aggressione"),
        ("Piazza Venezia", 41.8954, 12.4829, "Furto"),
        ("Piazza della Repubblica", 41.9019, 12.4953, "Furto"),
        ("Piazza Barberini", 41.9035, 12.4884, "Aggressione"),
        ("Piazza del Campidoglio", 41.8925, 12.4829, "Furto"),
        ("Piazza della Minerva", 41.8990, 12.4772, "Furto"),
        ("Piazza Navona", 41.8983, 12.4744, "Omicidio"),
        ("Piazza di Spagna", 41.9060, 12.4832, "Furto"),
        ("Piazza del Popolo", 41.9102, 12.4766, "Aggressione"),
        ("Piazza Farnese", 41.8964, 12.4712, "Furto"),
        ("Piazza Colonna", 41.9006, 12.4801, "Furto"),
        ("Piazza di Pietra", 41.8992, 12.4807, "Aggressione"),
        ("Piazza Venezia", 41.8953, 12.4829, "Furto"),
        ("Piazza della Repubblica", 41.9018, 12.4952, "Omicidio"),
        ("Piazza Barberini", 41.9034, 12.4883, "Furto"),
        ("Piazza del Campidoglio", 41.8926, 12.4830, "Aggressione"),
        ("Piazza della Minerva", 41.8991, 12.4771, "Furto"),
        ("Piazza Navona", 41.8984, 12.4745, "Furto"),
        ("Piazza di Spagna", 41.9059, 12.4833, "Omicidio"),
        ("Piazza del Popolo", 41.9101, 12.4767, "Furto"),
        ("Piazza Farnese", 41.8965, 12.4711, "Furto"),
        ("Piazza Colonna", 41.9005, 12.4800, "Aggressione"),
        ("Piazza di Pietra", 41.8991, 12.4808, "Furto"),
        ("Piazza Venezia", 41.8952, 12.4829, "Furto"),
        ("Piazza della Repubblica", 41.9017, 12.4951, "Aggressione"),
        ("Piazza Barberini", 41.9033, 12.4882, "Furto"),
        ("Piazza del Campidoglio", 41.8927, 12.4831, "Omicidio"),
        ("Piazza della Minerva", 41.8992, 12.4770, "Furto"),
        ("Piazza Navona", 41.8985, 12.4746, "Aggressione"),
        ("Piazza di Spagna", 41.9058, 12.4834, "Furto"),
    ]

def create_map():
    # Definisci la mappa di Folium
    m = folium.Map(location=[41.9028, 12.4964], zoom_start=12, tiles='OpenStreetMap')

    # Aggiungi HeatMapLayer limitata ai casi di Roma
    crime_coordinates = [[crime[1], crime[2]] for crime in initial_crimes]
    HeatMap(crime_coordinates, radius=50).add_to(m)

    # Aggiunta dei pin sulla mappa di Folium
    for address, lat, lon, crime_type in initial_crimes:
        folium.Marker([lat, lon], popup=f"{address} - {crime_type}").add_to(m)

    # Salva la mappa di Folium come HTML
    m.save('static2/map.html')

    # Restituisci l'oggetto mappa
    return m

def update_map():
    # Inizializza la mappa
    m = create_map()

    # Se esiste un file CSV caricato, aggiorna la mappa con i nuovi dati
    csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_points.csv')
    print("Percorso del file CSV:", csv_file_path)  # Stampare il percorso del file CSV per debug
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_data = list(csv_reader)  # Leggi i dati dal file CSV e memorizzali in una lista

            # Aggiungi l'heatmap solo se ci sono nuovi dati
            if csv_data:
                # Aggiungi i nuovi punti sulla mappa
                for row in csv_data:
                    lat = float(row['Latitudine'])
                    lon = float(row['Longitudine'])
                    address = row['Indirizzo']
                    crime_type = row['Tipo Crimine']
                    folium.Marker([lat, lon], popup=f"{address} - {crime_type}").add_to(m)

                # Aggiungi l'heatmap con i nuovi dati
                HeatMap([[float(row['Latitudine']), float(row['Longitudine'])] for row in csv_data], radius=50).add_to(m)

    # Salva la mappa di Folium aggiornata come HTML
    m.save('static2/map.html')

@app.route('/')
def home():
    update_map()
    # Rendi la mappa disponibile nella pagina HTML
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_map():
    # Cancella il file CSV e aggiorna la mappa
    csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_points.csv')
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    update_map()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Controlla se il file è stato inviato
        if 'file' not in request.files:
            flash('Nessun file selezionato')
            return redirect(request.url)
        file = request.files['file']
        # Controlla se il nome del file è vuoto
        if file.filename == '':
            flash('Nessun file selezionato')
            return redirect(request.url)
        # Se il file è stato inviato e ha un nome, leggilo e aggiungi i nuovi punti alla mappa
        if file:
            filename = secure_filename(file.filename)
            # Salva il file nella cartella temporanea
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_points.csv')
            file.save(file_path)
            print("File CSV caricato con successo:", file_path)  # Stampare il percorso del file CSV caricato per debug
            flash('File caricato con successo')
            update_map()  # Aggiorna la mappa con i nuovi punti e l'heatmap
            return redirect(url_for('home'))  # Reindirizza alla visualizzazione principale
    return render_template('upload.html')

if __name__ == '__main__':
    create_map()  # Creazione della mappa iniziale all'avvio dell'applicazione
    app.run(debug=True)
