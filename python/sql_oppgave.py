import psycopg2

user = 'name'
pwd = 'password'

connection = \
    "dbname='" + user + "' " +  \
    "user='" + user + "_priv' " + \
    "port='5432' " +  \
    "host='dbpg-ifi-kurs03.uio.no' " + \
    "password='" + pwd + "'"

def huffsa():
    conn = psycopg2.connect(connection)

    ch = 0
    while (ch != 3):
        print("--[ HUFFSA ]--")
        print("Vennligst velg et alternativ:\n 1. Søk etter planet\n 2. Legg inn forsøksresultat\n 3. Avslutt")
        ch = int(input("Valg: "))

        if (ch == 1):
            planet_sok(conn)
        elif (ch == 2):
            legg_inn_resultat(conn)

def planet_sok(conn):
    
    print(" -- [Søk etter planet] -- ")
    mole1 = input("Skriv inn molekyl1: ")
    mole2 = input("Skriv inn molekyl2: ")
    cur = conn.cursor()

    if mole2 != "":
        q = "SELECT p.navn, p.masse, s.masse, s.avstand, p.liv " + \
            "FROM planet AS p INNER JOIN materie as m ON (p.navn = m.planet)" \
            + " INNER JOIN materie AS m2 ON (p.navn = m2.planet) INNER JOIN stjerne AS s ON (s.navn = p.stjerne)" + \
            " WHERE m.planet = m2.planet AND m.molekyl = %(mole1)s " \
            + "AND m2.molekyl = %(mole2)s ORDER BY s.avstand ASC;"
        cur.execute(q, {'mole1': mole1, 'mole2': mole2})

    if mole2 == "":
        q = "SELECT p.navn, p.masse, s.masse, s.avstand, p.liv " + \
                "FROM planet AS p INNER JOIN stjerne AS s ON (p.stjerne = s.navn) INNER JOIN materie AS m ON (p.navn = m.planet)" + \
                "WHERE m.molekyl = %(mole1)s ORDER BY s.avstand ASC;"

        cur.execute(q, {'mole1': mole1})


    rows = cur.fetchall()

    if (rows == []):
        print("-- [Ingen planeter samsvarer med molekyl(ene)] -- ")
        return

    print("\n -- RESULTATER --\n")
    x = len(rows)
    n = 1
    for row in rows:
        print(f"Navn: {row[0]}")
        print(f"Planet-masse: {row[1]}")
        print(f"Stjerne-masse: {row[2]}")
        print(f"Stjerne-distanse: {row[3]}")
        if row[4] == False:
            liv = "Nei"
        elif row[4] == True:
            liv = "Ja"
        print(f" Bekreftet liv: {liv}")

        print(f" -- [Planet {n} av {x}] -- \n")
        n += 1
    return


def legg_inn_resultat(conn):
    cur = conn.cursor()

    print(" -- [Legg inn resultater] -- ")
    planet = input("Planet: ")
    skummel = input("Skummel (j/n): ")
    if skummel == "n":
        skummel = False
    elif skummel == "j":
        skummel = True
    intel = input("Intelligent (j/n): ")
    if intel == "n":
        intel = False
    elif intel == "j":
        intel = True
    beskr = input("Beskrivelse: ")
    if beskr == None:
        beskr = ""
    liv = True

    cur.execute("UPDATE planet SET liv = %s, skummel = %s, intelligent = %s, beskrivelse = %s WHERE navn = %s;", (liv, skummel, intel, beskr, planet))
    conn.commit()

    print(" -- [Dine forskningsresulater er lagt inn!] -- \n")
    return


if __name__ == "__main__":
    huffsa()
