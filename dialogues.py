# Приветствия и знакомство
greetings = [
    "Привет",
    "Здравствуй",
    "Ты кто такой?",
    "Как тебя зовут?",
    "Рад познакомиться",
    "Давно ты здесь?",
    "Чем ты здесь занимаешься?"
]

# О себе и биографии
about_self = [
    "Расскажи о себе",
    "Откуда ты родом?",
    "Как ты сюда попал?",
    "Расскажи свою историю",
    "У тебя есть семья?",
    "Ты один живёшь?",
    "Чем ты славишься?",
    "Как долго ты здесь?"
]

# О локации
about_location = [
    "Что это за место?",
    "Что здесь происходит?",
    "Опасно ли здесь?",
    "Кто здесь главный?",
    "Как тут вообще жить?",
    "Что интересного есть в этих краях?",
    "Какие здесь есть достопримечательности?"
]

# Квесты и задания
quests = [
    "Есть для меня работа?",
    "Могу я тебе помочь?",
    "Нужно что-то сделать?",
    "Какие тут есть проблемы?",
    "Слышал, тут что-то случилось",
    "Мне нужно задание",
    "Чем я могу быть полезен?"
]

# Торговля и услуги
trade = [
    "Что ты продаёшь?",
    "Есть что-нибудь интересное?",
    "Сколько это стоит?",
    "Можешь что-нибудь починить?",
    "Нужен совет по крафту",
    "Где тут можно купить оружие или броню?",
    "Ты умеешь ковать?"
]

# Лор и мир
lore = [
    "Что думаешь об Империи?",
    "Как тебе Братья Бури?",
    "Что происходит в Скайриме?",
    "Слышал о драконах?",
    "Ты веришь в Драконорождённого?",
    "Что скажешь о магии?",
    "Как относишься к эльфам?",
    "Кто твой ярл?",
    "Война закончится когда-нибудь?"
]

# Советы и знания
advice = [
    "Что посоветуешь новичку?",
    "Куда мне отправиться?",
    "Есть опасные места поблизости?",
    "Где можно научиться магии?",
    "Кто лучший кузнец в округе?",
    "Где найти хороший лут?",
    "Как заработать золота?"
]

# Диалоги из игры (каноничные реплики)
canonical = [
    "Тебя послали боги?",
    "Ты из гильдии воров?",
    "Ты смотришь на меня как на врага",
    "У тебя есть что сказать?",
    "Не стой на пути",
    "Мне нужна твоя помощь",
    "Я ищу кое-кого",
    "Ты что-то знаешь об этом?"
]

# Негативные и агрессивные
negative = [
    "Убирайся с дороги",
    "Не лезь не в своё дело",
    "Ты мне надоел",
    "Отойди, пока цел",
    "Я тебе не верю",
    "Пошёл прочь",
    "Ещё слово и пожалеешь"
]

# Эмоциональные и личные
emotional = [
    "Выглядишь уставшим",
    "У тебя всё в порядке?",
    "Тебе нужна помощь?",
    "Почему ты такой хмурый?",
    "Ты чем-то расстроен?",
    "У тебя был тяжёлый день?"
]

# О других персонажах
# about_others = [
#     "Что скажешь о {name}?",
#     "Ты знаешь {name}?",
#     "Как тебе {name}?",
#     "Слышал что-нибудь о {name}?"
# ]

# Слухи и новости
rumors = [
    "Какие новости?",
    "Что слышно в городе?",
    "Говорят, тут появились вампиры",
    "Слышал о драконьей атаке?",
    "Правда, что война скоро кончится?"
]

# Короткие и простые
short = [
    "Да",
    "Нет",
    "Понятно",
    "Интересно",
    "Расскажи ещё",
    "Давай ближе к делу",
    "Так-так",
    "Хм"
]

# Саркастичные и дерзкие
# sarcastic = [
#     "Ого, как интересно",
#     "Ну ты и болтун",
#     "Кто тебя вообще спрашивал",
#     "Серьёзно?",
#     "Да ладно",
#     "И что мне с этого?"
# ]

# О погоде и окружении
weather = [
    "Холодно сегодня",
    "Ненавижу эту погоду",
    "Красивый вид отсюда",
    "Тишина здесь мрачная"
]

# Магия и навыки
magic = [
    "Ты знаешь магию?",
    "Где тут учат заклинаниям?",
    "Как улучшить навыки?",
    "Что сильнее - меч или магия?"
]

# Фракции
factions = [
    "Как вступить в Гильдию воров?",
    "Ты из Тёмного Братства?",
    "Доверяешь Лиге убийц?",
    "Что думаешь о Клинках?"
]

# Все вопросы в одном списке
all_questions = (
    greetings + about_self + about_location + quests + trade + lore +
    advice + canonical + negative + emotional + 
    rumors + short + weather + magic + factions
)


npc_names = [
    "Abelone", "Acolyte Jenssen", "Adara", "Addvar", "Addvild", "Adeber",
    "Adelaisa Vendicci", "Adisla", "Adonato Leotelli", "Adrianne Avenicci",
    "Adril Arano", "Aduri Sarethi", "Aela the Huntress", "Aeri", "Aerin",
    "Aeta", "Afflicted", "Agmaer", "Agni", "Agnis", "Agrius", "Ahjisi",
    "Ahkari", "Ahlam", "Ahtar", "Ahzidal (NPC)", "Aia Arria", "Aicantar",
    "Ainethach", "Akar", "Alain Dufont", "Alduin", "Alesan", "Alessandra",
    "Alethius", "Alfarinn", "Alfhild Battle-Born", "Alik'r", "Alva", "Alvor",
    "Amaund Motierre", "Ambarys Rendar", "Amren", "Anaya(OC)", "Ancano",
    "Ancarion", "Anders", "Andurs", "Angeline Morrard", "Angi",
    "Angrenor Once-Honored", "Angvid", "Anise", "Annekke Crag-Jumper",
    "Anoriath", "Anska", "Anton Virane", "Anuriel", "Anwen", "Aphia Velothi",
    "Aquillius Aeresius", "Aranea Ienith", "Arcadia", "Arch-Curate Vyrthur",
    "Argis the Bulwark", "Ari", "Aringoth", "Arivanya", "Arnbjorn", "Arngeir",
    "Arniel Gane", "Arnskar Ember-Master", "Arob", "Arondil", "Arrald Frozen-Heart",
    "Arvel the Swift", "Asbjorn Fire-Tamer", "Asgeir Snow-Shod", "Aslfur", "Assur",
    "Asta", "Astrid", "Ataf", "Atahbah", "Atar", "Athis", "Atmah", "Atub",
    "Augur of Dunlain", "Aval Atheron", "Aventus Aretino", "Avrusa Sarethi",
    "Avulstein Gray-Mane", "Azura", "Azzada Lylvieve", "Azzadal", "Babette",
    "Badnir", "Bagrak", "Balagog gro-Nolob", "Balbus", "Baldor Iron-Shaper",
    "Balgruuf the Greater", "Balimund", "Banning", "Barbas", "Barknar (ranger)",
    "Bashnag", "Bassianus Axius", "Batum gra-Bar", "Beem-Ja", "Beggars",
    "Beirand", "Beitild", "Belchimac", "Belethor", "Beleval", "Belrand",
    "Belyn Hlaalu", "Bendt", "Benor", "Bergritte Battle-Born", "Bersi Honey-Hand",
    "Betrid Silver-Blood", "Birna", "Bjorlam", "Blackblood Marauders", "Blaise",
    "Bodil", "Bolar", "Bolfrida Brandy-Mug", "Bolgeir Bearclaw", "Bolli", "Bolund",
    "Bor", "Borgakh the Steel Heart", "Borgny", "Borkul the Beast", "Borri",
    "Borvir", "Bothela", "Boti", "Bottar", "Bradyn", "Braig", "Braith",
    "Bralsa Drel", "Bran", "Brand-Shei", "Brelas", "Brelyna Maryon", "Brenuin",
    "Briehl", "Brill", "Brina Merilis", "Britte", "Brother Verulus",
    "Brunwulf Free-Winter", "Bryling", "Brynjolf", "Bujold the Unworthy",
    "Bulfrek", "Cairine", "Calcelmo", "Calder", "Calixto Corrium",
    "Camilla Valerius", "Captain Aldis", "Captain Avidius", "Captain Hargar",
    "Captain Lonely-Gale", "Captain Veleth", "Captain Wayfinder", "Carlotta Valentia",
    "Cedran", "Celann", "Chief Burguk", "Chief Larak", "Chief Mauhulakh",
    "Chief Yamarz", "Children", "Christer", "Cicero", "Cindiri Arano",
    "Clinton Lylvieve", "Colette Marence", "Commander Maro", "Constance Michel",
    "Corpulus Vinius", "Corsair", "Cosnach", "Crescius Caerellius",
    "Curwe", "CuSith", "Cynric Endell"
]

npcs = [
    "Dalan Merchad",
    "Danica Pure-Spring",
    "Dark Brotherhood Initiate",
    "Daughter of Coldharbour",
    "Daynas Valen",
    "Dealer",
    "Deeja",
    "Deekus",
    "Deep-In-His-Cups",
    "Degaine",
    "Delacourt",
    "Delphine",
    "Delvin Mallory",
    "Dengeir of Stuhn",
    "Deor Woodcutter",
    "Derkeethus",
    "Dervenin",
    "Dexion Evicus",
    "Dinya Balu",
    "Dirge",
    "Donnel",
    "Dorian",
    "Dorthe",
    "Drahff",
    "Drascua",
    "Dravin Llanith",
    "Dravynea the Stoneweaver",
    "Drevis Neloren",
    "Dreyla Alor",
    "Drifa",
    "Dro'marash",
    "Drokt",
    "Drovas Relvi",
    "Dryston",
    "Duach",
    "Dukaan (NPC)",
    "Dulug",
    "Durak",
    "Dushnamub",
    "Ebony Warrior (NPC)",
    "Edda",
    "Edith",
    "Edla",
    "Eimar",
    "Einarth",
    "Eirid",
    "Eisa Blackthorn",
    "Elda Early-Dawn",
    "Elder Othreloth",
    "Elenwen",
    "Elgrim",
    "Elisif the Fair",
    "Elmus",
    "Elrindir",
    "Eltrys",
    "Elvali Veren",
    "Elynea Mothren",
    "Embry",
    "Endarie",
    "Endon",
    "Endrast",
    "Engar",
    "Enmon",
    "Ennis",
    "Ennoc",
    "Ennodius Papius",
    "Enthir",
    "Eola",
    "Eorlund Gray-Mane",
    "Erandur",
    "Erdi",
    "Eriana",
    "Erik the Slayer",
    "Erikur",
    "Eris",
    "Erith",
    "Erj",
    "Erlendr",
    "Esbern",
    "Esmond Tyna",
    "Estormo",
    "Etienne Rarnis",
    "Ettiene",
    "Evette San",
    "Evul Seloth",
    "Eydis",
    "Faendal",
    "Faida",
    "Falas Selvayn",
    "Faleen",
    "Falion",
    "Falk Firebeard",
    "Fallaise",
    "Fanari Strong-Voice",
    "Faralda",
    "Farengar Secret-Fire",
    "Farkas",
    "Faryl Atheron",
    "Fastred",
    "Felldir the Old",
    "Fenrig",
    "Feran Sadri",
    "Festus Krex",
    "Fethis Alor",
    "Fianna",
    "Fihada",
    "Filnjar",
    "Finna",
    "Firir",
    "Fjola",
    "Fjotli",
    "Fjotra",
    "Florentius Baenius",
    "Frabbi",
    "Fralia Gray-Mane",
    "Francois Beaufort",
    "Frea",
    "Frida",
    "Fridrika",
    "Frodnar",
    "Frofnir Trollsbane",
    "Froki Whetted-Blade",
    "From-Deepest-Fathoms",
    "Frorkmar Banner-Torn",
    "Frothar",
    "Fruki",
    "Fultheim",
    "Fura Bloodmouth",
    "G",
    "Gabriella",
    "Gadba gro-Largash",
    "Gadnor",
    "Gaius Maro",
    "Galathil",
    "Galdrus Hlervu",
    "Gallus Desidenius",
    "Galmar Stone-Fist",
    "Ganna Uriel",
    "Garakh",
    "Garan Marethi",
    "Garmr",
    "Garthar",
    "Garvey",
    "Garyn Ienth",
    "Gat gro-Shargakh",
    "Gavros Plinius",
    "Geimund",
    "Geldis Sadri",
    "Gelebros",
    "Gemma Uriel",
    "General Falx Carius",
    "General Tullius",
    "Gerda",
    "Gerdur",
    "Gestur Rockbreaker",
    "Ghak",
    "Ghamorz",
    "Ghorbash the Iron Hand",
    "Ghorza gra-Bagol",
    "Ghost",
    "Ghunzul",
    "Gian the Fist",
    "Gianna",
    "Gilfre",
    "Giraud Gemane",
    "Girduin",
    "Gisli",
    "Gissur",
    "Gjak",
    "Gjalund Salt-Sage",
    "Gloth",
    "Glover Mallory",
    "Golldir",
    "Gorm",
    "Gormlaith",
    "Gort",
    "Gralnach",
    "Gratian Caerellius",
    "Gregor",
    "Grelka",
    "Grelod the Kind",
    "Greta",
    "Grete",
    "Grimvar Cruel-Sea",
    "Grisvar the Unlucky",
    "Grogmar gro-Burzag",
    "Grosta",
    "Guard",
    "Gul",
    "Gularzob",
    "Gulum-Ei",
    "Gunding",
    "Gunjar",
    "Gunmar",
    "Gwendolyn",
    "Gwilin",
    "H",
    "Hadring",
    "Hadvar",
    "Haelga",
    "Hafjorg",
    "Hafnar Ice-Fist",
]

all_npcs = npcs + npc_names


