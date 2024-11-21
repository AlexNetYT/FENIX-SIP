import sqlite3, os,shutil
from rich import *
os.system("title URFF Fenix Pather")
# Connect to the SQLite database
print("[white][bold]Default path[/white] [green]C:\\ProgramData\\Fenix\\Navdata\\nd.db3[/green]")
inp = input("Input path to nb.db3, if default left blank: ")
path = 'C:\\ProgramData\\Fenix\\Navdata\\nd.db3' if inp == '' else inp
if os.path.isfile(path) and path.endswith('.db3'):
    print(f"[green][bold]DB file found: [/green][white]{path}[/white][green] Connecting[/bold][/green]")
else:
    print(f"[red][bold]DB file not found: [/red][white]{path}[/white]")
    exit()
    
try:
    conn = sqlite3.connect(path)
except Exception as e:
    print("[red][bold] Error connecting to DB, error: " + str(e))
    exit()
    
shutil.copyfile(path, path+".old")

# Create a cursor objec
cursor = conn.cursor()
try:
    cursor.execute('SELECT * FROM config')
except sqlite3.OperationalError as e:
    print("[red][bold]Error reading DB: " + str(e))
    exit()
for info_tuo in cursor.fetchall():
    info = list(info_tuo)
    print(f"[bold][yellow]{info[0]}[/yellow]:   [green]{info[1]}[/green]")
print("Continue? [[green]y[/green]/[red]n[/red]]:      ")
if input() == 'n':
    print("[blue][bold]Exiting...[/blue][/bold]")
    exit()
    
cursor.execute('SELECT * FROM Airports ORDER BY id DESC LIMIT 1')
for last_airport_tup in cursor.fetchall():
    l_ap_list = list(last_airport_tup)
    if l_ap_list[2] == 'URFF':
        print("[green][bold]Already in Database[/green][/bold]")
        os.system('pause')
    else: 
        cursor.execute('SELECT * FROM Runways ORDER BY id DESC LIMIT 1')
        for last_runway_tup in cursor.fetchall():
            l_rwy_list = list(last_runway_tup)
        print("[yellow][bold]NOT IN DATABASE[/bold][/yellow]\n[green]Creating...[/green]")
        latest_ap_id = l_ap_list[0]
        latest_rwy_id = l_rwy_list[0]
        print(f"[blue][bold]LOG: [/blue] Latest Airports id is {latest_ap_id}")
        print(f"[blue][bold]LOG: [/blue] Latest Runways id is {latest_rwy_id}")
        print(f"""[blue][bold]LOG: [/blue] Executing:
            INSERT INTO Airports ("ID", "Name", "ICAO", "PrimaryID", "Latitude", "Longtitude", "Elevation", "TransitionAltitude", "TransitionLevel", "SpeedLimit", "SpeedLimitAltitude") VALUES ('{latest_ap_id+1}', 'SIMFEROPOL', 'URFF', NULL, '45.0522', '33.9751', '639', '3050', '10000', '250', '10000'); 
            INSERT INTO Runways ("ID", "AirportID", "Ident", "TrueHeading", "Length", "Width", "Surface", "Latitude", "Longtitude", "Elevation") VALUES ('{latest_rwy_id+1}', '{latest_rwy_id+1}', '01', '7.0', '3701', '60', 'ASP', '45.035853', '33.9751', '610');
            INSERT INTO Runways ("ID", "AirportID", "Ident", "TrueHeading", "Length", "Width", "Surface", "Latitude", "Longtitude", "Elevation") VALUES ('{latest_rwy_id+2}', '{latest_rwy_id+2}', '19', '187.0', '3701', '60', 'ASP', '45.06516894', '33.97708886', '600');

              """) 
        
        cursor.execute(f""" INSERT INTO Airports ("ID", "Name", "ICAO", "PrimaryID", "Latitude", "Longtitude", "Elevation", "TransitionAltitude", "TransitionLevel", "SpeedLimit", "SpeedLimitAltitude") VALUES ('{latest_ap_id+1}', 'SIMFEROPOL', 'URFF', NULL, '45.0522', '33.9751', '639', '3050', '10000', '250', '10000');""")
        cursor.execute(f""" INSERT INTO Runways ("ID", "AirportID", "Ident", "TrueHeading", "Length", "Width", "Surface", "Latitude", "Longtitude", "Elevation") VALUES ('{latest_rwy_id+1}', '{latest_ap_id+1}', '01', '7.0', '3701', '60', 'ASP', '45.035853', '33.9751', '610');""")
        cursor.execute(f""" INSERT INTO Runways ("ID", "AirportID", "Ident", "TrueHeading", "Length", "Width", "Surface", "Latitude", "Longtitude", "Elevation") VALUES ('{latest_rwy_id+2}', '{latest_ap_id+1}', '19', '187.0', '3701', '60', 'ASP', '45.06516894', '33.97708886', '600');""")
        
        conn.commit()
        print("[green][bold]Success.[/bold] Database was updated successfully.\n[/green][white][bold]Old DB saved with .old extension[/bold]\n[dark_orange]If you will have any issues just delete current [/dark_orange][yellow][bold]nb.db3[/bold][/yellow] [dark_orange]and rename[/dark_orange] [yellow][bold]nd.db3.old[/yellow] -> [green]nb.db3[/green][/bold]\n[blue][bold]:airplane: Have a good flights!:airplane:\n[/blue][white] Made by AlexNet. [link https://github.com/AlexNetYT]GitHub")
        os.system("pause")