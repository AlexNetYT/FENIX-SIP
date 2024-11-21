import sqlite3, os, shutil, glob
from rich import print

# Set terminal title
os.system("title URFF Fenix PMDG Updater")

# Define default Fenix DB path
fenix_db_path = 'C:\\ProgramData\\Fenix\\Navdata\\nd.db3'
input_fenix_path = input(f"Input path to Fenix nb.db3 (leave blank for default path: {fenix_db_path}): ")
fenix_db_path = input_fenix_path if input_fenix_path else fenix_db_path

# Define single PMDG DB file for consolidated updates
single_pmdg_db_path = 'e_dfd_PMDG.s3db'
input_single_pmdg_path = input(f"Input path for consolidated PMDG database (leave blank for default path: {single_pmdg_db_path}): ")
single_pmdg_db_path = input_single_pmdg_path if input_single_pmdg_path else single_pmdg_db_path

# Backup function
def create_backup(db_path):
    backup_path = db_path + ".old"
    shutil.copyfile(db_path, backup_path)
    print(f"[green]✔ Backup created at: {backup_path}[/green]")

# Search for PMDG databases in Community folder
def find_pmdg_databases(community_path):
    pmdg_databases = []
    search_patterns = ['pmdg-aircraft-738', 'pmdg-aircraft-739', 'pmdg-aircraft-737', 'pmdg-aircraft-736','pmdg-aircraft-77w']
    
    for pattern in search_patterns:
        aircraft_path = os.path.join(community_path, pattern, 'Config', 'NavData', 'e_dfd_PMDG.s3db')
        print("[blue][bold] LOG:[/blue] [white] Aircraft path: %s" %aircraft_path)
        if os.path.isfile(aircraft_path):
            pmdg_databases.append(aircraft_path)
            print(f"[cyan]Found PMDG DB at: {aircraft_path}[/cyan] :airplane:")
        else:
            print(f"[yellow]Warning: No database found for {pattern}[/yellow]")
    
    return pmdg_databases

# Check Fenix database path and connect
if os.path.isfile(fenix_db_path):
    print(f"[cyan]Fenix DB file located at: {fenix_db_path}[/cyan] :link:")
    try:
        conn_fenix = sqlite3.connect(fenix_db_path)
        print("[green]Successfully connected to Fenix database![/green]")
        create_backup(fenix_db_path)
    except Exception as e:
        print(f"[red]⚠ Error connecting to Fenix database: {e}[/red]")
        exit()
else:
    print(f"[red]⚠ Fenix DB file not found at: {fenix_db_path}[/red]")
    exit()

# Check consolidated PMDG database path and connect
if os.path.isfile(single_pmdg_db_path):
    print(f"[cyan]Using single PMDG DB file for updates at: {single_pmdg_db_path}[/cyan]")
    try:
        conn_pmdg = sqlite3.connect(single_pmdg_db_path)
        print("[green]Successfully connected to single PMDG database![/green]")
        create_backup(single_pmdg_db_path)
    except Exception as e:
        print(f"[red]⚠ Error connecting to PMDG database: {e}[/red]")
        exit()
else:
    print(f"[red]⚠ Single PMDG DB file not found at: {single_pmdg_db_path}[/red]")
    exit()

# Prompt user to input Community folder path for PMDG aircraft
community_path = input("Input path to Community folder for PMDG DB search: ")
pmdg_databases = find_pmdg_databases(community_path)

# Function to insert data for Simferopol (URFF) in Fenix database
def insert_fenix_urff(cursor):
    cursor.execute('SELECT * FROM Airports ORDER BY id DESC LIMIT 1')
    last_airport = cursor.fetchone()
    latest_ap_id = last_airport[0] if last_airport else 0
    
    cursor.execute(f"""
        INSERT INTO Airports ("ID", "Name", "ICAO", "PrimaryID", "Latitude", "Longtitude", "Elevation", 
                              "TransitionAltitude", "TransitionLevel", "SpeedLimit", "SpeedLimitAltitude")
        VALUES ('{latest_ap_id+1}', 'SIMFEROPOL', 'URFF', NULL, '45.0522', '33.9751', '639', '3050', 
                '10000', '250', '10000');
    """)

# Function to insert data for Simferopol (URFF) in PMDG database
def insert_pmdg_urff(cursor):
    cursor.execute("""
        INSERT INTO tbl_airports (area_code, icao_code, airport_identifier, airport_name, 
                                  airport_ref_latitude, airport_ref_longitude, ifr_capability, 
                                  longest_runway_surface_code, elevation, transition_altitude, 
                                  transition_level, speed_limit, speed_limit_altitude)
        VALUES ('EEU', 'UR', 'URFF', 'SIMFEROPOL', '45.0522', '33.9751', 'Y', 'H', '639', 
                '3050', '10000', '250', '10000');
    """)
    cursor.execute("""
        INSERT INTO tbl_runways (area_code, icao_code, airport_identifier, runway_identifier, 
                                 runway_latitude, runway_longitude, runway_magnetic_bearing, 
                                 runway_true_bearing, landing_threshold_elevation, 
                                 runway_length, runway_width, surface_code)
        VALUES 
            ('EEU', 'UR', 'URFF', 'RW01', '45.035853', '33.9751', '7.0', '7.0', '610', '3701', '60', 'ASP'),
            ('EEU', 'UR', 'URFF', 'RW19', '45.06516894', '33.97708886', '187.0', '187.0', '600', '3701', '60', 'ASP');
    """)

# Insert data for URFF in Fenix database
fenix_cursor = conn_fenix.cursor()
insert_fenix_urff(fenix_cursor)
conn_fenix.commit()
print("[green]Fenix database successfully updated with URFF data![/green]")

# Insert data for URFF in single PMDG database
pmdg_cursor = conn_pmdg.cursor()
insert_pmdg_urff(pmdg_cursor)
conn_pmdg.commit()
print("[green]Single PMDG database successfully updated with URFF data![/green]")

# Copy single PMDG DB to each PMDG database found in Community folder
for db_path in pmdg_databases:
    shutil.copyfile(single_pmdg_db_path, db_path)
    print(f"[cyan]Updated {db_path} with new URFF data[/cyan]")

print("\n[blue][bold]:airplane: Update complete! Your PMDG and Fenix databases now include Simferopol (URFF) data. Enjoy your flights! :airplane:[/bold][/blue]")
