# Vaizdo įrašų katalogai (Video Catalogues)

Saityno taikomųjų programų projektavimo (T120B165) laboratorinių darbų projektas.

## Apie projektą

Projekto tikslas - sukurti sistemą, palengvinančią vaizdo įrašų pakartotinį peržiūrėjimą, organizavimą bei informacijos paiešką „YouTube“ platformoje.

Sistemoje realizuojamas hierarchinis duomenų sąryšis (vienas su daug):
- **Katalogas** (`Catalogue`) -> **Vaizdo įrašas** (`Video`) -> **Anotacija** (`Annotation`)

## Funkciniai reikalavimai

Svečias naudotojas galės:

1. Peržiūrėti svetainės pagrindinį puslapį
2. Užsiregistruoti prie svetainės
3. Prisijungti prie svetainės

Narys naudotojas galės:

1. Sukurti vaizdo įrašų katalogą
2. Pridėti vaizdo įrašą į pasirinktą katalogą
3. Pridėti anotaciją vaizdo įrašui tam tikram laiko intervale
4. Peržiūrėti vaizdo įrašą įterptame „YouTube" lange
5. Peržiūrėti vaizdo įrašo stenogramą
6. Atlikti semantinę tekstinę paiešką katalogo lygmenyje pagal anotacijos ir stenogramas
7. Nustatyti katalogo viešumą
8. Atsijungti

Administratorius

1. Peržiūrėti naudotojų sukurtus katalogus, video ir anotacijas
2. Pašalinti naudotojų sukurtus katalogus, video ar anotacijas

## Sistemos architektūra

Kliento pusės kūrimui bus naudojamas Vue su TypeScript.

Severio pusė - Python FastAPI ir SQLAlchemy (ORM). Kodas vykdomas naudojant GCP Cloud Run. Tekstinei paieškai bus naudojami Vertex AI Text Embedding ir pgvector įskiepis. Duomenys bus saugomi Neon (serverless PostgresSQL) duomenų bazėje

---

## Projekto struktūra

- `backend/` - API serveris, realizuotas naudojant **Python** ir **FastAPI**. Paketų valdymui naudojamas `uv`.

---

## Backend paleidimas

### Reikalavimai
- [Python](https://www.python.org/) (>=3.12)
- [uv](https://docs.astral.sh/uv/)

### Žingsniai

   ```bash
   cd backend
   uv sync
   uv run fastapi dev
   ```

Serveris pasiekamas ties: `http://127.0.0.1:8000`

---

## API dokumentacija ir patikra

API specifikacija ir metodų išbandymas:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
