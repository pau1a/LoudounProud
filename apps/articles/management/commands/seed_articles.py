"""Seed the site with articles drawn from the local events research PDF."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.articles.models import Article, Author, Town


# fmt: off
ARTICLES = [
    # ── NEWS ────────────────────────────────────────────────────────────
    {
        "title": "Coalfield Communities project celebrates success as £6m landscape partnership nears completion",
        "deck": "East Ayrshire Council has hailed the Coalfield Communities Landscape Partnership as a model for rural regeneration, with peatland restoration, wildflower meadows and heritage work across the Doon Valley.",
        "category": "news",
        "towns": ["cumnock", "auchinleck"],
        "days_ago": 1,
        "is_featured": True,
        "body": (
            "The Coalfield Communities Landscape Partnership (CCLP) — a £6 million programme spanning 22 individual projects — "
            "has been celebrated by East Ayrshire Council as it enters its final phase.\n\n"
            "Over the past five years, the partnership has restored peatland, created wildflower meadows and hedgerows, improved "
            "public paths and carried out heritage restoration across the former coalfield communities of the Doon Valley.\n\n"
            "The project has now been extended to May 2026 to allow completion of the Doon Valley Railway heritage shed, one of "
            "the most ambitious elements of the programme.\n\n"
            "Council leader Douglas Reid said the CCLP demonstrated what was possible when communities, landowners and public "
            "bodies worked together. \"This landscape was shaped by industry. Now it's being shaped by the people who live here.\"\n\n"
            "The partnership was funded by the National Lottery Heritage Fund, with additional support from NatureScot, Forestry "
            "and Land Scotland, and East Ayrshire Council."
        ),
    },
    {
        "title": "Net-zero Wallace Court opens in Mauchline with 20 new homes built to Passivhaus standards",
        "deck": "A new assisted living development on Kilmarnock Road provides 17 flats and three accessible bungalows, all built to Passivhaus energy standards.",
        "category": "news",
        "towns": ["mauchline"],
        "days_ago": 6,
        "homepage_secondary": True,
        "secondary_priority": 2,
        "body": (
            "Wallace Court, a net-zero assisted living development on Kilmarnock Road in Mauchline, has officially opened "
            "its doors to residents.\n\n"
            "The development provides 17 flats and three fully accessible bungalows, all constructed to Passivhaus standards — "
            "a rigorous energy-efficiency benchmark that dramatically reduces heating costs and carbon emissions.\n\n"
            "The project was delivered by East Ayrshire Council in partnership with housing association partners, with construction "
            "completed on schedule despite supply chain pressures during the build phase.\n\n"
            "Residents began moving in during late January, with all properties expected to be occupied by the end of March.\n\n"
            "\"This is exactly the kind of housing our communities need,\" said Councillor Elena Collins, the council's housing "
            "convener. \"Energy-efficient, accessible, and designed for people to live independently with dignity.\"\n\n"
            "The development includes communal gardens, a residents' lounge, and is within walking distance of Mauchline's "
            "town centre shops and services."
        ),
    },
    {
        "title": "Former Kirkstyle Primary School to become Army Cadets headquarters",
        "deck": "East Ayrshire Council has agreed to sell the disused school to the Lowland Reserve Forces, creating a new HQ with community facilities.",
        "category": "news",
        "towns": ["kilmarnock"],
        "days_ago": 6,
        "body": (
            "The former Kirkstyle Primary School is set for a new chapter after East Ayrshire Council agreed to sell the "
            "building to the Lowland Reserve Forces and Cadets' Association.\n\n"
            "The site will be transformed into the West Lowland Battalion Army Cadets headquarters, providing "
            "state-of-the-art training facilities for young people across the region.\n\n"
            "Crucially, the redevelopment will also include community facilities that will be available for local groups "
            "and organisations to use outside cadet training hours.\n\n"
            "The school has stood empty since its closure several years ago, and the sale ends a period of uncertainty "
            "about the building's future. Planning applications are expected to be submitted in the coming months, "
            "with work anticipated to begin before the end of 2026."
        ),
    },
    {
        "title": "Supported housing completed at Barnweil Drive as council invests in complex care",
        "deck": "Four renovated properties in Hurlford now provide supported accommodation for adults with complex needs, funded through the council's Innovation Fund.",
        "category": "news",
        "towns": ["hurlford"],
        "days_ago": 39,
        "body": (
            "Four properties at Barnweil Drive in Hurlford have been renovated and converted into supported accommodation "
            "for adults with complex care needs.\n\n"
            "The project, funded through East Ayrshire Council's Innovation Fund, provides purpose-designed homes where "
            "residents can live with appropriate support while maintaining as much independence as possible.\n\n"
            "Each property has been adapted to meet specific accessibility requirements, with features including "
            "level-access showers, widened doorways and assistive technology.\n\n"
            "The scheme is part of the council's broader strategy to reduce reliance on residential care placements "
            "and provide more community-based alternatives."
        ),
    },
    {
        "title": "Demolition underway in Darvel as derelict factory makes way for community plans",
        "deck": "A disused fabric factory on Jamieson Road is being demolished due to asbestos, with the site earmarked for community redevelopment including a possible cycling track.",
        "category": "news",
        "towns": ["darvel"],
        "days_ago": 27,
        "body": (
            "Demolition work has begun on a derelict fabric factory on Jamieson Road in Darvel, bringing an end to years "
            "of concern about the deteriorating building.\n\n"
            "The factory, which has stood empty for over a decade, required specialist demolition due to the presence of "
            "asbestos materials throughout the structure.\n\n"
            "Once cleared, the site will be transferred to Darvel Community Trust for redevelopment. Early plans include "
            "a cycling track and community facilities, though detailed proposals are still being developed.\n\n"
            "\"This has been an eyesore and a worry for people living nearby for far too long,\" said trust chair "
            "Margaret Henderson. \"We're excited to finally have the chance to turn it into something positive for the town.\"\n\n"
            "The demolition is expected to take approximately eight weeks, with the site transfer anticipated by summer 2026."
        ),
    },
    {
        "title": "Roadworks begin near Crosshouse as Ayrshire Innovation Park takes shape",
        "deck": "Single-lane closures and temporary traffic lights will operate for around ten weeks near Crosshouse Hospital to support construction of the new innovation park.",
        "category": "news",
        "towns": ["kilmarnock"],
        "days_ago": 43,
        "body": (
            "Roadworks near Crosshouse Hospital began in January to support the construction of the Ayrshire Innovation Park, "
            "a major new business and technology hub.\n\n"
            "Drivers can expect single-lane closures and temporary traffic lights for approximately ten weeks as utility "
            "connections and access roads are put in place.\n\n"
            "The Innovation Park is a key element of the Ayrshire Growth Deal, a £250 million package of investment "
            "aimed at boosting the regional economy. The park will provide flexible workspace for technology companies, "
            "start-ups and research organisations.\n\n"
            "East Ayrshire Council has advised motorists to allow extra time for journeys in the Crosshouse area, "
            "particularly during peak hours."
        ),
    },
    # ── BUSINESS ────────────────────────────────────────────────────────
    {
        "title": "North and East Ayrshire councils agree shared economic development service",
        "deck": "A new joint service bringing together tourism, business support and digital functions will launch on 1 June 2026, led by a Regional Economic Director.",
        "category": "business",
        "towns": ["kilmarnock", "irvine"],
        "days_ago": 6,
        "homepage_secondary": True,
        "secondary_priority": 1,
        "section_lead": True,
        "body": (
            "North and East Ayrshire councils have formally approved the creation of a shared economic development service, "
            "in what leaders describe as an unprecedented step towards regional collaboration.\n\n"
            "The new service, which will launch on 1 June 2026, will bring together tourism promotion, business support, "
            "digital infrastructure and inward investment functions under a single Regional Economic Director.\n\n"
            "The move is designed to eliminate duplication, pool expertise and present a unified offer to businesses "
            "considering investing in the region.\n\n"
            "\"We compete with Edinburgh, Glasgow and Dundee for investment,\" said East Ayrshire Council leader Douglas Reid. "
            "\"A fragmented approach doesn't serve our businesses or our communities. This changes that.\"\n\n"
            "The shared service will be based across both council areas, with staff working from existing offices in "
            "Kilmarnock and Irvine. A recruitment process for the Regional Economic Director is expected to begin in March."
        ),
    },
    {
        "title": "CoRE project launches first net-zero retrofit in Cumnock with £24.5m investment",
        "deck": "Three blocks of flats at Meagher Court are being retrofitted with insulation, solar PV and ground-source heat pumps in a project funded by £17m from the UK Government.",
        "category": "business",
        "towns": ["cumnock"],
        "days_ago": 8,
        "body": (
            "The Community Renewable Energy (CoRE) project has launched its first demonstrator in Cumnock, beginning the "
            "transformation of three blocks of flats at Meagher Court into net-zero homes.\n\n"
            "The ambitious retrofit programme includes external insulation, internal upgrades, rooftop solar PV panels "
            "and ground-source heat pumps — a comprehensive package designed to eliminate fuel poverty and slash "
            "carbon emissions.\n\n"
            "The project is backed by £17 million from the UK Government and £7.5 million from East Ayrshire Council, "
            "making it one of the largest social housing retrofit programmes in Scotland.\n\n"
            "Work at Meagher Court is the first phase of a wider programme that will continue through 2027, with "
            "additional properties across the former coalfield communities scheduled for upgrade.\n\n"
            "\"Fuel poverty is a reality for too many families in East Ayrshire,\" said the council's sustainability lead. "
            "\"This project tackles it at source — by making the homes themselves fundamentally more efficient.\""
        ),
    },
    {
        "title": "East Ayrshire brings education and business together with new skills hubs",
        "deck": "Reorganised employability services and new local hubs in Cumnock, Doon Valley and Galston aim to improve job training and tackle skills shortages.",
        "category": "business",
        "towns": ["cumnock", "galston", "kilmarnock"],
        "days_ago": 50,
        "body": (
            "East Ayrshire Council has reorganised its employability services under a single Education & Skills directorate, "
            "creating a more joined-up approach to job training and career support.\n\n"
            "New local hubs — SL66 in Cumnock, SL99 in the Doon Valley, and an upcoming hub in Galston Town Hall — "
            "will provide holistic support including careers advice, skills assessment, training referrals and "
            "employer connections.\n\n"
            "Among the headline initiatives is an EV/Hydrogen Automotive Sector Skills programme, designed to address "
            "the growing shortage of technicians trained in electric and hydrogen vehicle technology.\n\n"
            "\"The economy is changing fast,\" said the council's director of education and skills. \"We need to make sure "
            "our residents have access to the training that leads to actual jobs — not just qualifications.\""
        ),
    },
    # ── COMMUNITY ───────────────────────────────────────────────────────
    {
        "title": "Kilmarnock Farmers Market returns to The Cross with 30 local producers",
        "deck": "The monthly market brings Aberdeen Angus beef, artisan cheeses, fresh fish, handmade crafts and local beers to the heart of the town centre.",
        "category": "community",
        "towns": ["kilmarnock"],
        "days_ago": 0,
        "section_lead": True,
        "body": (
            "Kilmarnock Farmers Market is back at The Cross this Saturday, with up to 30 producers offering everything "
            "from Aberdeen Angus beef and fresh-caught fish to award-winning cheeses and handmade crafts.\n\n"
            "The market, held on the third Saturday of each month, has become a fixture of town centre life — drawing "
            "shoppers from across East Ayrshire and beyond.\n\n"
            "Regular stallholders include livestock farmers from the Irvine Valley, fish merchants from the Ayrshire coast, "
            "artisan bakers, craft brewers and makers of everything from soap to woodwork.\n\n"
            "Upcoming dates are 21 February, 21 March and 18 April. The market runs from 9am to 1pm regardless of weather.\n\n"
            "Organiser Fiona MacLeod said footfall has grown steadily over the past year. \"People want to know where their "
            "food comes from and who made it. That's exactly what we offer.\""
        ),
    },
    {
        "title": "Give to Gain events celebrate International Women's Day across East Ayrshire",
        "deck": "Free family-friendly events in Cumnock, Kilmarnock and Stewarton will feature mocktail masterclasses, health checks and information markets.",
        "category": "community",
        "towns": ["kilmarnock", "cumnock", "stewarton"],
        "days_ago": 3,
        "body": (
            "East Ayrshire Health & Social Care Partnership is hosting three free events across the region to mark "
            "International Women's Day, under the banner \"Give to Gain.\"\n\n"
            "The celebrations will take place on 10 March in Cumnock, 11 March at The Howard Centre in Kilmarnock, "
            "and 12 March in Stewarton — each running from 11am to 1pm.\n\n"
            "Events will feature mocktail masterclasses, health checks, an information market with local services "
            "and organisations, and light refreshments. All events are free but registration is required.\n\n"
            "\"We wanted to create something that was genuinely welcoming and useful,\" said partnership coordinator "
            "Sarah Mitchell. \"It's about celebrating women and girls, but also connecting people with support "
            "and services they might not know about.\""
        ),
    },
    {
        "title": "Killie Beer Festival returns to Rugby Park with craft brewers and live music",
        "deck": "The popular beer festival is back on 30 May, showcasing Scottish craft brewers alongside local food vendors and artists. Tickets go on sale 26 February.",
        "category": "community",
        "towns": ["kilmarnock"],
        "days_ago": 2,
        "body": (
            "The Kilmarnock Beer Festival — affectionately known as the Killie Beer Festival — will return to Rugby Park "
            "on 30 May 2026, promising an afternoon of craft beer, local food and live music.\n\n"
            "The festival, which runs from noon until 7pm, showcases beers from Scottish brewers alongside food vendors "
            "and local artists. It is strictly over-18s only.\n\n"
            "Tickets will first go on sale at the Park Hotel on 26 February before being released online — a nod to "
            "the organisers' commitment to giving locals first pick.\n\n"
            "Last year's event sold out within three weeks, and organisers are expecting similar demand. \"It's become "
            "one of the highlights of the Kilmarnock calendar,\" said festival director Jamie Ross. \"People plan "
            "their weekends around it.\""
        ),
    },
    {
        "title": "Monster Truck MotorFest brings Slingshot shows and stunt displays to Ayr Racecourse",
        "deck": "A two-day family motor show on 21-22 March features monster truck displays, motorbike stunts, a funfair, food village and character meet-and-greets.",
        "category": "community",
        "towns": ["ayr"],
        "days_ago": 4,
        "body": (
            "Ayr Racecourse will host Monster Truck MotorFest Scotland on 21-22 March, a two-day family event "
            "combining monster truck shows, motorbike stunt displays and a funfair.\n\n"
            "The headline attraction is Slingshot, a full-size monster truck performing crushing and freestyle displays "
            "throughout both days. The event also features a food village, character meet-and-greets for younger visitors, "
            "and a range of automotive displays.\n\n"
            "Saturday hours run from 10am to 10:30pm, with Sunday finishing at 7:30pm. Tickets are available online "
            "with family packages offering savings on individual admission.\n\n"
            "The event is expected to draw visitors from across the west of Scotland, with Ayr Racecourse providing "
            "ample parking and easy access from the A77."
        ),
    },
    {
        "title": "Bounce in the Park inflatable theme park coming to Eglinton Country Park",
        "deck": "The touring attraction for children aged 3-14 arrives in Kilwinning from 1-4 May with unlimited play sessions, giant slides and assault courses.",
        "category": "community",
        "towns": ["kilwinning"],
        "days_ago": 5,
        "body": (
            "Bounce in the Park, a touring inflatable theme park, will set up at Eglinton Country Park in Kilwinning "
            "from 1-4 May 2026.\n\n"
            "The attraction is designed for children aged 3 to 14 and features giant slides, assault courses and "
            "unlimited play sessions. Tickets cost approximately £10 per child.\n\n"
            "The event has proved hugely popular at venues across Scotland, with sessions regularly selling out. "
            "Parents are advised to book early to secure preferred time slots.\n\n"
            "Eglinton Country Park provides a natural setting for the event, with its 400 acres of parkland, "
            "woodland walks and the restored Eglinton Castle ruins offering additional activities for families "
            "making a day of it."
        ),
    },
    {
        "title": "Troon Wedding Fayre offers free admission and local inspiration",
        "deck": "Troon Concert Hall hosts a free wedding show on 8 March featuring local vendors, fashion, food tastings and freebies.",
        "category": "community",
        "towns": ["troon"],
        "days_ago": 7,
        "body": (
            "Couples planning their wedding can find local inspiration at the Troon Wedding Fayre on 8 March, "
            "held at Troon Concert Hall from 11:30am to 3pm.\n\n"
            "Admission is free, and the event features a curated selection of local wedding vendors — from florists "
            "and photographers to venues and caterers — alongside fashion shows, food tastings and giveaways.\n\n"
            "The fayre is particularly popular with couples looking to keep their celebrations local, with many "
            "of the exhibitors based in Ayrshire.\n\n"
            "\"There's a real trend towards local, personal weddings,\" said organiser Claire Thompson. \"People want "
            "to work with suppliers they can meet face to face and who know the area.\""
        ),
    },
    # ── CULTURE ─────────────────────────────────────────────────────────
    {
        "title": "Dick Institute celebrates Scottish cartoonist Malky McCormick in major retrospective",
        "deck": "Two linked exhibitions at the Dick Institute and Baird Institute explore the life and work of one of Scotland's best-loved satirical artists.",
        "category": "culture",
        "towns": ["kilmarnock", "cumnock"],
        "days_ago": 2,
        "section_lead": True,
        "body": (
            "The Dick Institute in Kilmarnock is hosting \"Discovering Malky McCormick,\" a retrospective of the Scottish "
            "cartoonist whose satirical drawings have appeared in newspapers and galleries for over four decades.\n\n"
            "The exhibition, which runs until 30 April 2026, features a comprehensive collection of McCormick's work — "
            "from sharp political cartoons to affectionate portraits of Scottish life. Admission is free.\n\n"
            "A companion exhibition at the Baird Institute in Cumnock, \"The Wee Man and The Big Yin,\" explores "
            "McCormick's celebrated collaborations with comedian Billy Connolly. That show runs until 16 May.\n\n"
            "A further retrospective, \"Malky McCormick: A Life in Colour,\" is being prepared as a major expansion "
            "of the current exhibit. Dates are still to be confirmed.\n\n"
            "The Dick Institute is also showing \"Killie-catures!\" — football-inspired caricatures by local artists — "
            "until 15 March. Meanwhile, Time Travel Trails are running at various East Ayrshire museums through "
            "February and March, offering interactive puzzle trails for children exploring local history."
        ),
    },
    {
        "title": "Dean Castle tours offer a glimpse into Kilmarnock's restored medieval landmark",
        "deck": "Daily guided tours of the newly restored Dean Castle run until 20 March, with tickets at £6 per person.",
        "category": "culture",
        "towns": ["kilmarnock"],
        "days_ago": 9,
        "body": (
            "Dean Castle in Kilmarnock is welcoming visitors for daily guided tours of the restored medieval fortress, "
            "which reopened following a major restoration programme.\n\n"
            "Tours run at noon each day until 20 March 2026, taking visitors through the castle's great hall, "
            "the armoury and the keep, with guides bringing the building's 600-year history to life.\n\n"
            "Tickets are approximately £6 per person and can be booked through the East Ayrshire Leisure Trust website.\n\n"
            "The castle sits within the 200-acre Dean Castle Country Park, making it an easy half-day outing for "
            "families. The park itself is free to enter and features woodland walks, a burns heritage trail and "
            "a visitor centre with a cafe."
        ),
    },
    {
        "title": "CentreStage Kilmarnock announces packed spring season from musicals to comedy",
        "deck": "Guys and Dolls, Joseph and the Amazing Technicolor Dreamcoat, and an 80s/90s nostalgia night headline a busy few weeks at Kilmarnock's community theatre.",
        "category": "culture",
        "towns": ["kilmarnock"],
        "days_ago": 1,
        "body": (
            "CentreStage in Kilmarnock has a packed spring programme, with three major productions running through "
            "February and March.\n\n"
            "First up is **Guys and Dolls**, performed by the venue's S4-6 musical theatre group from 19-21 February. "
            "Thursday and Friday performances start at 7pm, with Saturday offering both a 2pm matinee and 7pm evening show. "
            "Tickets are £8-£10.\n\n"
            "On 7 March, **Boots, Boybands & Belters** brings an evening of 80s and 90s nostalgia with live band "
            "RockitMen recreating the decade's biggest hits. Tickets are £10-£12.\n\n"
            "The highlight of the season is **Joseph and the Amazing Technicolor Dreamcoat**, staged by Kilmarnock Amateur "
            "Operatic Society from 10-14 March. The full-scale production features matinee performances on 13-14 March. "
            "Tickets are around £23.\n\n"
            "Also in March, comedian **Tom Stade** performs at the Park Hotel on 7 March (7:30pm, tickets via Eventbrite), "
            "and psychic medium **Fiona Stewart Williams** brings her \"Hello from Heaven\" show to the Park Hotel on 25 March."
        ),
    },
    {
        "title": "Troon Concert Hall hosts comedy, Elvis and the return of the Mod Rally",
        "deck": "Gary Meikle, an Elvis tribute act and the annual Friday Street Mod Rally are among the highlights at Troon's main venue this spring.",
        "category": "culture",
        "towns": ["troon"],
        "days_ago": 3,
        "body": (
            "Troon Concert Hall has a varied spring programme spanning comedy, music and subculture.\n\n"
            "**Gary Meikle: Yer Maw** kicks things off on 7 March at 6:30pm, with the Scottish comedian bringing his "
            "trademark irreverent humour. Tickets are approximately £27.50.\n\n"
            "On 21 March, **Absolute Elvis** starring Johnny Lee Memphis delivers what's billed as one of the UK's "
            "most authentic Elvis tribute performances. Tickets are £20.\n\n"
            "Looking further ahead, the **Friday Street 2026 Troon Mod Rally** returns on 2 May, taking over both "
            "Troon Concert Hall and the South Beach Hotel. Guest DJs Bill Kealy and Bob Gordon will spin Northern Soul, "
            "R&B and ska vinyl from 7:30pm until half past midnight. The event has become a pilgrimage for mod culture "
            "enthusiasts from across Scotland."
        ),
    },
    {
        "title": "Dance Fest 2026 brings 900 dancers to the Gaiety Theatre in Ayrshire's largest showcase",
        "deck": "Over 40 dance groups, including East Ayrshire Youth Dance Company, perform across two days at Ayr's historic theatre.",
        "category": "culture",
        "towns": ["ayr"],
        "days_ago": 4,
        "body": (
            "Dance Fest 2026, Ayrshire's largest annual dance showcase, returns to the Gaiety Theatre in Ayr on "
            "9 and 11 March.\n\n"
            "The event features over 900 dancers from 40 groups performing across two days, with shows at 4pm and "
            "7pm on each date. Styles range from ballet and contemporary to street dance and Highland.\n\n"
            "Among the featured groups is the East Ayrshire Youth Dance Company, which has been developing its "
            "programme over the past two years under the guidance of professional choreographers.\n\n"
            "The Gaiety Theatre, one of Scotland's finest Edwardian theatres, provides a spectacular setting "
            "for the showcase. Tickets are available through the venue's box office."
        ),
    },
    {
        "title": "Scottish Maritime Museum opens Tides of Time exhibition and spring glass workshops",
        "deck": "A Royal Scottish Academy exhibition exploring maritime heritage and hands-on glassblowing sessions led by Robert McLeod run through spring in Irvine.",
        "category": "culture",
        "towns": ["irvine"],
        "days_ago": 8,
        "body": (
            "The Scottish Maritime Museum in Irvine has two major draws this spring: a prestigious art exhibition and "
            "a series of hands-on glass workshops.\n\n"
            "**Tides of Time**, which opened on 9 February, celebrates the Royal Scottish Academy's 200th anniversary "
            "with artworks by nine Royal Scottish Academicians exploring Scotland's relationship with the sea. "
            "The exhibition runs daily from 10am at the Linthouse Building on Harbour Road.\n\n"
            "Meanwhile, **Spring Glass Workshops** run every Wednesday and Saturday from 4 March to 11 April. "
            "Wednesday sessions (2 hours, starting at 2pm) and Saturday sessions (4 hours, 10am-2pm) are led by "
            "glassblower Robert McLeod, who guides participants through creating their own decorative glass pieces.\n\n"
            "Sessions are limited to just two participants at a time, making them an intimate and focused experience. "
            "Booking is essential."
        ),
    },
    {
        "title": "Booze Bingo and club nights bring nightlife to Stewarton and Ayr",
        "deck": "An adult bingo night at Stewarton's Saya Centre, a house music session at Printhouse Ayr, and the return of STREETrave offer something for every taste.",
        "category": "culture",
        "towns": ["stewarton", "ayr"],
        "days_ago": 5,
        "body": (
            "Ayrshire's nightlife scene is showing signs of life this spring, with a range of events catering to "
            "different tastes across the region.\n\n"
            "In Stewarton, **Booze Bingo** takes over the Saya Centre on 14 March — an adult bingo night combining "
            "the classic game with drinks and entertainment. Details and tickets are available via Skiddle.\n\n"
            "Ayr offers two contrasting nights out. **AyrBiza — Spring Session** at Printhouse Ayr on 21 March "
            "promises long house-music DJ sets and a relaxed atmosphere from 6pm until midnight. Tickets are "
            "approximately £8 via Skiddle.\n\n"
            "For those with a taste for nostalgia, **STREETrave — The Legends Return 2026** revives the legendary "
            "90s rave brand at Ayr Pavilion on 7 March, running from 1pm to midnight with a lineup of DJs. "
            "Tickets range from £30 to £45."
        ),
    },
    # ── SPORT ───────────────────────────────────────────────────────────
    {
        "title": "Kilmarnock FC face crucial away double before Hearts visit Rugby Park",
        "deck": "Killie travel to Dundee United and Falkirk before hosting Hearts on 14 March in what could be a defining run of fixtures.",
        "category": "sport",
        "towns": ["kilmarnock"],
        "days_ago": 0,
        "section_lead": True,
        "body": (
            "Kilmarnock FC face a testing run of three fixtures that could shape their Premiership season.\n\n"
            "First up is an away trip to **Dundee United** at Tannadice Park on 21 February (3pm kick-off), followed by "
            "a visit to **Falkirk** on 28 February (3pm).\n\n"
            "The run culminates with **Heart of Midlothian** visiting Rugby Park on 14 March for an 8pm kick-off under "
            "the floodlights — one of the most anticipated home fixtures of the spring.\n\n"
            "Manager Derek McInnes will be looking for consistency after a mixed run of results. \"Every game in this "
            "league is tough,\" he said. \"But the boys know what's at stake. These are the fixtures that define "
            "where you finish.\"\n\n"
            "Tickets for the Hearts match are expected to sell quickly and will go on sale to season ticket holders first."
        ),
    },
    {
        "title": "Kilmarnock RFC youth sides in cup action as senior squad eyes league push",
        "deck": "The Boys U14 and Girls U17 teams face cup ties on 22 February, while the first XV have Dunfermline, Stewartry and West of Scotland on the horizon.",
        "category": "sport",
        "towns": ["kilmarnock"],
        "days_ago": 1,
        "body": (
            "Kilmarnock RFC has a busy spring ahead, with youth cup ties and senior league fixtures filling the calendar "
            "at Bellsland.\n\n"
            "This weekend sees double cup action on 22 February, with the **Boys U14** facing Biggar in Cup Round 4 "
            "at 2pm, and the **Girls U17** taking on Oban Lorne in their own fourth-round tie at the same time.\n\n"
            "The senior squad returns to National League Division 4 action on 28 February with a home match against "
            "**Dunfermline RFC** (3pm), while the reserves host Dumfries Saints 2nd XV on the same day.\n\n"
            "Looking ahead, the first XV travel to **Stewartry RFC** on 21 March before a significant home fixture "
            "against **West of Scotland** on 4 April.\n\n"
            "Club president Alan Drummond said the breadth of fixtures reflected the health of the club. \"From our "
            "youngest players to the first XV, there's real momentum at Bellsland right now.\""
        ),
    },
    {
        "title": "Bowie Park training ground on schedule as Kilmarnock FC's £7m facility takes shape",
        "deck": "The new complex will feature full-size artificial pitches, a nine-a-side pitch and a 250-seat stand for the academy, women's team and community groups.",
        "category": "sport",
        "towns": ["kilmarnock"],
        "days_ago": 10,
        "body": (
            "Kilmarnock FC has confirmed that construction of the Bowie Park training complex is on schedule, with the "
            "£7 million-plus facility expected to transform the club's development infrastructure.\n\n"
            "The complex will include full-size artificial pitches, a nine-a-side pitch and a 250-seat stand, "
            "primarily serving the club's academy and women's team.\n\n"
            "Crucially, the facility will also be available for community groups, schools and grassroots football "
            "organisations — a commitment that was central to the project's planning approval.\n\n"
            "\"This is about more than just Kilmarnock FC,\" said chief executive Phyllis McLeish. \"It's about "
            "giving young people in this area world-class facilities to develop their talent, regardless of which "
            "team they play for.\"\n\n"
            "The project represents one of the largest investments in football infrastructure in the west of Scotland "
            "outside the Old Firm clubs."
        ),
    },
    {
        "title": "Spring Saturday Raceday opens Ayr Racecourse jump-racing season",
        "deck": "The first major meeting of the spring features the Ayrshire Premier Handicap Steeplechase on 7 March, with student tickets at £10 and under-18s free.",
        "category": "sport",
        "towns": ["ayr"],
        "days_ago": 6,
        "body": (
            "Ayr Racecourse kicks off its spring jump-racing season with the Spring Saturday Raceday on 7 March.\n\n"
            "Gates open at 11:50am, with the first race at 1:50pm and the last at 5:20pm. The feature race is the "
            "**Ayrshire Premier Handicap Steeplechase**, which regularly attracts runners from some of Scotland and "
            "northern England's leading yards.\n\n"
            "Ticket prices are: Single Enclosure £29 (full price), £24 for advance group bookings, £24 concession. "
            "Students pay just £10, and under-18s go free.\n\n"
            "The racecourse is also the venue for the Monster Truck MotorFest Scotland later in March, making it "
            "a busy spring for Ayrshire's premier sporting venue."
        ),
    },
]
# fmt: on


class Command(BaseCommand):
    help = "Seed the site with articles from the local events research."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing articles before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Article.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing article(s).")

        author = Author.objects.first()
        if not author:
            self.stderr.write("No authors found. Create an author first.")
            return

        town_map = {t.slug: t for t in Town.objects.all()}
        now = timezone.now()
        created = 0

        for data in ARTICLES:
            slug_base = data["title"]
            if Article.objects.filter(title=data["title"]).exists():
                self.stdout.write(f"  SKIP (exists): {data['title'][:60]}")
                continue

            article = Article(
                title=data["title"],
                deck=data.get("deck", ""),
                body_markdown=data.get("body", ""),
                category=data["category"],
                author=author,
                status="published",
                published_at=now - timedelta(days=data.get("days_ago", 0)),
                is_featured=data.get("is_featured", False),
                homepage_secondary=data.get("homepage_secondary", False),
                secondary_priority=data.get("secondary_priority", 0),
                section_lead=data.get("section_lead", False),
            )
            article.save()

            towns = [town_map[slug] for slug in data.get("towns", []) if slug in town_map]
            if towns:
                article.towns.set(towns)

            created += 1
            self.stdout.write(f"  OK: {data['title'][:60]}")

        self.stdout.write(self.style.SUCCESS(f"\nSeeded {created} article(s)."))
