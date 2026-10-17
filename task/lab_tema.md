**Projekto „Vaizdo įrašų katalogai" aprašymas**

T120B165 Saityno taikomųjų programų projektavimas. Projekto uždavinys

Turinys

[1. Sprendžiamo uždavinio aprašymas
[3](#sprendžiamo-uždavinio-aprašymas)](#sprendžiamo-uždavinio-aprašymas)

[1.1. Sistemos paskirtis [3](#sistemos-paskirtis)](#sistemos-paskirtis)

[1.2. Funkciniai reikalavimai
[3](#funkciniai-reikalavimai)](#funkciniai-reikalavimai)

[2. Sistemos architektūra
[4](#sistemos-architektūra)](#sistemos-architektūra)

# Sprendžiamo uždavinio aprašymas

## Sistemos paskirtis

Sistemos tikslas -- palengvinti vaizdo įrašų pakartotinį peržiūrėjimą ir
informacijos paiešką „YouTube" platformoje.

## Funkciniai reikalavimai

Svečias naudotojas galės:

1.  Peržiūrėti svetainės pagrindinį puslapį

2.  Užsiregistruoti prie svetainės

3.  Prisijungti prie svetainės

Narys naudotojas galės:

1.  Sukurti vaizdo įrašų katalogą

2.  Pridėti vaizdo įrašą į pasirinktą katalogą

3.  Pridėti anotaciją vaizdo įrašui tam tikram laiko intervale

4.  Peržiūrėti vaizdo įrašą įterptame „YouTube" lange

5.  Peržiūrėti vaizdo įrašo stenogramą

6.  Atlikti semantinę tekstinę paiešką katalogo lygmenyje pagal
    anotacijos ir stenogramas

7.  Nustatyti katalogo viešumą

8.  Atsijungti

Administratorius

1.  Peržiūrėti naudotojų sukurtus katalogus, video ir anotacijas

2.  Pašalinti naudotojų sukurtus katalogus, video ar anotacijas

# Sistemos architektūra

Kliento pusės kūrimui bus naudojamas Vue su TypeScript.

Severio pusė -- Python FastAPI ir SQLAlchemy (ORM). Kodas vykdomas
naudojant GCP Cloud Run. Tekstinei paieškai bus naudojami Vertex AI Text
Embedding ir pgvector įskiepis. Duomenys bus saugomi Neon (serverless
PostgresSQL) duomenų bazėje
