Modulio tikslas


Išmokti kurti programų sistemas paremtas saityno paslaugomis (web services)

Norint tai daryti reikės išmokti projektuoti į paslaugas orientuotos architektūros SOA (Service Oriented Architecture) sprendimus

3

Modulio temos

1

Įžanga

Pristatomas kurso turinys ir vertinimo sistema

2

(!) RESTfull paslaugų projektavimas

Detalus REST nagrinėjimas

REST projektavimo gerosios praktikos

3

(!) REST programavimas su .NET ir AI

Demo / Savarankiškas darbas

4

RESTfull principai

SOA architektūros

REST ir SOAP

RESTfull principai

4

Modulio temos

5

(!) Autentifikavimas ir autorizacija, OAuth2, JWT

Autorizacija ir autentifikacija.

Saityno ir tinklalapių programų autentifikacijos / autorizacijos skirtumai

OAuth2 autorizacijos „protokolas“.

OAuth2 realizacijos pavyzdys.

6

(!) JWT autorizacijos programavimas su .NET

Demo / Savarankiškas darbas

7

Saityno paslaugų realizavimas naudojant GraphQL

GraphQL idėjos.

GraphQL veikimas.

5

GraphQL derinimas.

GraphQL bibliotekos.

Modulio temos

8

Debesų kompiuterijos sprendimai saityno paslaugoms

Bendros tendencijos rinkoje, dabartinės galimybės, sprendžiamos problemos.

Pagrindinių modelių apžvalga: Infrastructure as Service (IaaS), Platform as a Service (PaaS), Software as a Service (SaaS).

9

Saityno saugumas

Nagrinėjamos dažniausiai paliekamos saugumo spragos.

Nagrinėjami saugumo spragų audito ir prevencijos įrankiai.

10

(!) Sukurtos sistemos diegimas kompiuterijos paslaugose

Demo / Savarankiškas darbas

11

Į paslaugas orientuota architektūra (SOA – Service Oriented Architecture)

Problemos, kurias sprendžia SOA.

SOA principai: contracts, coupling, abstraction, reusability, autonomy, statelessness, discoverability, composability.

Mikroservisai

6

Modulio temos

12

(!) Autorizacijos įgyvendinimas kliento pusėje

Demo / Savarankiškas darbas

13

Vue, Angular, React

Būsenos valdymas (angl. state management);

Virtualus DOM;

Reaktyvumas;

Karkasų sintaksė;

Testavimas;

Pavyzdys kaip sukurti projektą.

8

Laboratorinių vedimo forma

Laboratorinių darbų laikas skirtas konsultacijoms ir atsiskaitymams.

Atsiskaitymai vyks numatytais laikais laboratorijose.

Savaitė laiko korekcijoms.

Lab 0

Lab 1

Lab 2

Lab 3

Ataskaita

2 sav.

5 sav.

3 sav.

4 sav.

iki rugsėjo 20 d.

iki spalio 25 d.

iki lapkričio 15 d.

iki gruodžio 13 d.

iki gruodžio 23 d.

9

Modulio savarankiški darbai

Eiga:

1

Technologijų pasirinkimas

2

Projekto pasirinkimas ir aprašymas

Moodle sistemoje užfiksuosime jūsų pasirinkto projekto apimtį

3

Projekto realizacija ir pažingsninis atsiskaitymas

Projekto atskiros dalys bus užfiksuojamos kaip pirmas, antras ir trečias laboratoriniai

4

Ataskaita (internete)

10

Modulio laboratoriniai darbai



1

Serverio programinės įrangos sąsajos sukūrimas

Sąsaja turi būti suprojektuota remiantis REST principais ir gerosiomis praktikomis

2

Autentifikacijos ir autorizacijos mechanizmų realizacija ir diegimas

Turi būti realizuota autentifikacija ir autorizacija

3

Klientinės dalies („frontendo“) realizacija

Turi būti realizuota įvestis, API panaudojimas ir vaizdavimas

Programa turi būti įdiegta debesų kompiuterijos paslaugose

4

Ataskaita (internete)

Architektūrinis sprendimo pateikimas

API specifikacija (openAPI)

11

0 LAB: projekto aprašymas



Projekto pavadinimas

Sprendžiamo uždavinio aprašymas

Sistemos paskirtis

Funkciniai reikalavimai

Diegimo diagrama

Pasirinktų technologijų aprašymas

Projekto uždavinys turi būti patalpintas projektui sukurtame wiki arba projekto kodo Git saugykloje (.readme).

Svarbiausia: suderinti temą ir tris taikomosios srities objektus su dėstytoju.

Apimtis  1–3 psl.

12



Laboratorinių darbų

vertinimo kriterijai

Kiekvienas laboratorinis darbas ir ataskaita vertinami 10 balų

13

1 LAB: vertinimo kriterijai



Iš viso 10 balų

Egzistuoja bent 3 taikomosios srities objektai ir operacijos su jais

3 balai

Tie objektai susiję hierarchiniu sąryšiu

1 balas

Paruošta testavimo aplinka

1 balas

Duomenų bazė užpildyta prasmingais duomenimis

1 balas

Grąžinami teisingi kodai

2 balai

REST semantikos laikymasis ir pakankama apimtis

2 balai

14

1 LAB: kriterijų paaiškinimai (1 iš 2)



Bent 3 taikomosios srities objektai ir operacijos su jais

API metodai turi būti realizuoti bent 3 taikomosios srities objektams. Objektai turi būti prasmingi, sudaryti iš daugiau nei vieno lauko.

Sistemos naudotojas (naudotojų lentelė) nėra taikomosios srities objektas.

Kiekvienam objektui turi būti realizuotas CRUD (Create, Read, Update, Delete) ir LIST (sąrašo gavimas).

Turi būti realizuotas puslapiavimas ir filtravimas.

Turi būti realizuota hypermedia bent esminiams elementams.

Bent 1 panaudojimo atvejis (profilis, panelė ir pan.), kur grąžinamas resursas sukonstruojamas iš bent 2 esybių.

Objektų hierarchinis sąryšis

Objektai susiję „grandinėle“ ryšiu vienas-su-daug, pvz. Tema → Įrašas → Komentaras arba Testas → Klausimas → Atsakymas.

Hierarchijoje neturi būti naudotojų esybės ir neturi būti vienas-su-vienu ryšių.

Negalimi variantai: Klientas → Užsakymas → Adresas; Žemynas → Šalis → Sostinė; Automobilis → VIN → Registracija.

Kodėl to reikia: kad galėtume pasitreniruoti realizuoti apimties valdymą (scoping) naudojant URL.

15

1 LAB: kriterijų paaiškinimai (2 iš 2)



Paruošta testavimo aplinka

Aplinka, kurioje galima greitai išbandyti visus API prieigos taškus (endpoints). Rekomenduojamas Postman, tinka ir kitos priemonės.

Turi būti parengtas užklausų rinkinys, leidžiantis pratestuoti visus prieigos taškus.

Duomenų bazė užpildyta prasmingais duomenimis

Kiekviena su hierarchinio ryšio objektais susijusi lentelė turi turėti bent 5 įrašus.

Įrašai turi būti prasmingi: ne atsitiktiniai raidžių kratiniai ar tiesiog žodis string.

Grąžinami teisingi kodai

Kiekvienas prieigos taškas privalo grąžinti teisingą atsako kodą: 404, 201, 204 ir kitus.

Jokiais atvejais neturėtų būti grąžinamas 500.

REST semantikos laikymasis ir apimtis

URI kuriami laikantis REST principų: POST /products, o ne POST /createProduct ar POST /products/create.

GET /customers/3/orders/9, o ne GET /getOrder?id=9&amp;cid=5. Analogiškai ir su visais kitais metodais.

Bent vienas metodas privalo būti hierarchinis ir apimti visus 3 objektus, pvz. GET /customers/3/orders/9/items.

16

1 LAB: gynimo metu turite gebėti aptarti



REST principus ir kaip jie realizuoti arba nerealizuoti programoje (stateless, cachable, uniform interface). Ką suteikia vienas ar kitas principas.

Esminius status codes. Reikės demonstruoti išskirtinius atvejus — dėstytojai specialiai mėgins iššaukti neteisingą programos elgesį.

Savo programos architektūrą: kur aprašomi keliai, kur vykdomos su užklausa susijusios operacijos. Gebėti pridėti papildomą taikomosios srities objektą ir realizuoti jam CRUD operacijas.

Kodėl pasirinkta viena ar kita DB valdymo sistema ir kokios galimos alternatyvos.

Jei naudotas LLM — kaip buvo kuriama jo pagalba ir kaip LLM buvo valdomas. Gynimo metu LLM naudoti negalima.

17

2 LAB: vertinimo kriterijai



Iš viso 10 balų

Integruota autorizacija naudojant OAuth arba JWT technologinius sprendimus

3 balai

Pasirinkta tinkama tokenų atnaujinimo strategija

2 balai

Realizuoti register, login ir logout metodai

2 balai

Projekte realizuota autorizacija pagal naudotojo rolę ir ID, yra bent 3 rolės

3 balai

18

2 LAB: kriterijų paaiškinimai



Integruota autorizacija (OAuth arba JWT)

Atitinkami sistemos prieigos taškai turi būti pasiekiami tik prisijungusiems naudotojams.

Žetono (token) viduje turi būti saugoma naudotojo informacija — rolė ir ID.

Tokenų atnaujinimo strategija

Turi būti naudojama žetonų atnaujinimo strategija, tokia kaip refresh token.

Access tipo žetonai turi galioti trumpai, refresh — ilgiau. Naudotojui neturi reikėti nuolatos jungtis iš naujo.

Register, login ir logout metodai

Atsijungimo metodas turi panaikinti naudotojo žetonus arba pažymėti juos kaip nebegaliojančius.

Galima vietinė autentifikacija arba išorinis tiekėjas (Google, Facebook ar kt.), arba abu. Žetonai valdomi kūrėjo pusėje.

Už dviejų faktorių autorizaciją skiriamas papildomas balas kuriam nors laboratoriniam.

Autorizacija pagal rolę ir ID, bent 3 rolės

Naudotojai gali naudotis tik tam tikrais prieigos taškais — pavyzdžiui, skelbimų kategorijas kuria tik administratorius.

Įgyvendintos apsaugos ten, kur rolė neapsaugo nuo kenkėjiškų veiksmų: paprastas naudotojas neturi galėti ištrinti ar redaguoti kito naudotojo komentaro.

19

2 LAB: gynimo metu turite gebėti aptarti



Kokia yra žetono struktūra ir kokia realizuota konkrečiai. Kur programoje sukuriamas žetonas ir kokie claims į jį įeina, kodėl naudinga įtraukti rolę, kaip galima arba negalima nulaužti žetoną.

Ar programos sukuriamas žetonas yra pasirašomas: kurioje vietoje, kokiu algoritmu, kur laikomi slapti arba viešosios kriptografijos raktai.

Kokiu būdu perduodamas žetonas (header, cookie ar kt.). Jei cookie — parodyti secure ir http-only vėliavas. Abiejų būdų privalumai ir trūkumai.

Kaip programa apsaugota nuo pagrindinių grėsmių (injekcijų, teisių eskalacijos ir kt.) ir kurioje vietoje tai realizuota.

Su autorizacija susijusius statuso kodus — reikės pademonstruoti jų veikimą.

20

3 LAB: vertinimo kriterijai



Iš viso 10 balų

Sąsaja leidžia panaudoti visus realizuotus API metodus

2 balai

Paveiksliukai, vektorinės ikonėlės, header ir footer elementai, modaliniai langai

2 balai

Panaudotos animacijos

1 balas

Naudotojo sąsaja yra vientisa ir pagyvinta naudojant CSS

2 balai

Responsive layout

1 balas

Publikavimas

2 balai

21

3 LAB: kriterijų paaiškinimai (1 iš 2)



Sąsaja leidžia panaudoti visus realizuotus API metodus

Trims pasirinktiems dalykinės srities objektams turi būti galima atlikti CRUD veiksmus naudojant vartotojo sąsają.

Turi būti realizuota registracija, prisijungimas ir žetonų atnaujinimas.

Duomenų įvedimui panaudoti bent 4 skirtingi elementai (input, textarea, pasirinkimų mygtukai, dropdown ar list, date/time/color picker, spinner ir t. t.).

Duomenys turi būti grąžinami json formatu, ne html.

Paveiksliukai, ikonėlės, header ir footer, modaliniai langai

Naudojami paveiksliukai, kurių dydis kinta priklausomai nuo lango dydžio.

Meniu punktuose naudojamos papildomos ikonėlės.

Sukūrimo, redagavimo arba ištrynimo formoms panaudoti modaliniai langai.

Svetainė turi header ir footer elementus ten, kur jų reikia.

22

3 LAB: kriterijų paaiškinimai (2 iš 2)



Panaudotos animacijos

Animacijos gali būti rodomos duomenų grąžinimo metu arba užvedus pelę ant kai kurių elementų.

Vientisa ir CSS pagyvinta naudotojo sąsaja

Vientisa spalvų paletė ir stilistika; elementai išdėstyti logiška, naudotojui patogia seka.

Panaudotas nestandartinis šriftas.

Naudotojui teikiamas grįžtamasis ryšys apie jo veiksmus. Naršyklės alert langai tam neturi būti naudojami.

Responsive layout

Sąsaja prisitaiko prie skirtingų ekrano dydžių, panaudotas bent vienas lūžio taškas (breakpoint).

Realizuotas „hamburgeris“ mobiliai versijai.

Publikavimas

Projektas patalpintas ir pasiekiamas internetu. Tinka bet kuris tiekėjas — Azure, DigitalOcean, Render ar kiti.

Backend ir frontend talpinimui skiriama po balą.

23

3 LAB: gynimo metu turite gebėti aptarti



Kodėl pasirinktas vienas ar kitas klientinės dalies karkasas ir kokios galimos alternatyvos.

Kokią architektūrą naudoja karkasas ir kaip jame saugoma būsena.

Kaip įtraukiami nestandartiniai šriftai — kokiu būdu ir kur tai padaryta jūsų programoje.

Kaip CSS realizuota animacija ir kur yra konkrečios animacijos kodas.

Kokiomis CSS priemonėmis realizuotas breakpoint. Gebėti jį pakeisti.

Kodėl naudinga naudoti vektorinės grafikos elementus ir kur jie padėti (jų šaltinis).

24

Inžinerinis projektas: vertinimo kriterijai



Iš viso 10 balų

Ataskaitos struktūra, formatavimas ir turinys

3 balai

Diegimo diagrama

2 balai

Naudotojo sąsaja ir jos projektas

2 balai

OpenAPI specifikacija

2 balai

Išvados

1 balas

Ataskaitos ginti nereikia. Tačiau norint sužinoti jos trūkumus ir turėti galimybę pataisyti geresniam įvertinimui, ataskaitą reikia parodyti laboratorinio užsiėmimo metu dėstytojui.

25

Inžinerinis projektas: kriterijų paaiškinimai



Ataskaitos struktūra, formatavimas ir turinys

Ataskaita turi būti prieinama Github arba įkelta į Moodle.

Turi būti laikomasi pateiktos struktūros, aprašyti visi skyriai. Jokio DI šlamšto (AI slop).

Diegimo diagrama

Atitinka realų arba numatomą sistemos diegimo atvejį.

Diagrama taisyklinga, paruošta naudojant UML standartą. Jokio plantUML.

Naudotojo sąsaja ir jos projektas

Pateikiami sąsajos ekranvaizdžiai ir bent 3 wireframe, padaryti su Figma arba kitu įrankiu.

OpenAPI specifikacija

Specifikacija papildyta naudojimo pavyzdžiais ir galimais rezultatais.

Pateikta skaitomu formatu dokumente arba Github. Galite naudoti LLM.

Išvados

Išsamios ir sunumeruotos. Pasakoma ne tik, kas buvo padaryta, bet ir kas iš to. Jokio DI šlamšto.

26

Egzaminas



Laikomas klasėje prie kompiuterio (Moodle)

~25–30

4

testų klausimų

laisvos formos klausimai

(rankinis vertinimas)

Atsakymai įvertinami ir įvedami į akademinę sistemą.

33