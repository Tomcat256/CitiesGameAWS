import re
import random
from enum import Enum
from copy import deepcopy
import json

from typing import List, Dict

KNOWN_CITIES = {
    'А': ['АРМАВИР', 'АФРИН', 'АЛЬБУКЕРКЕ', 'АЛУШТА', 'АСЬЮТ', 'АКТАУ', 'АТЫРАУ', 'АКТОБЕ', 'АБАКАН', 'АЛЕППО',
          'АРЗАМАС', 'АМРИТСАР', 'АРТЕМ', 'АНКАРА', 'АНАДЫРЬ', 'АДЕН', 'АНГАРСК', 'АЛЬМЕТЬЕВСК', 'АРАМИЛЬ', 'АРМЯНСК',
          'АВГУСТОВ', 'АМСТЕРДАМ', 'АНТАНАНАРИВУ', 'АЛЖИР', 'АЙДАХО-ФОЛС', 'АБУДЖА', 'АБУ-ДАБИ', 'АСУАН', 'АММАН',
          'АКЕРАБАТ', 'АПАТИТЫ', 'АФИНЫ', 'АУГСБУРГ', 'АНТРАЦИТ', 'АЛМА-АТА', 'АЧИНСК', 'АХАЛЦИХ', 'АРСЕНЬЕВ',
          'АЙН-ЭЛЬ-АРАБ', 'АСБЕСТ', 'АБИДЖАН', 'АТЛАНТА', 'АККРА', 'АДЕЛАИДА', 'АЛИТУС', 'АНАХАЙМ', 'АЛАПАЕВСК',
          'АРХАНГЕЛЬСК', 'АШХАБАД', 'АБЕРДИН', 'АХАЛКАЛАКИ', 'АГРА', 'АСТРАХАНЬ', 'АЗОВ', 'АКСАЙ', 'АХТУБИНСК',
          'АДДИС-АБЕБА', 'АНАПА', 'АСУНСЬОН', 'АНТВЕРПЕН'],
    'Б': ['БЕСЛАН', 'БУХАРА', 'БУХАРЕСТ', 'БИР-ЛЕЛУ', 'БЕРЛИН', 'БЕРЕСТЕЧКО', 'БОХТАР', 'БРАТСК', 'БАТ', 'БЕРГЕН',
          'БАТАЙСК', 'БЕЛГОРОД', 'БРАЗИЛИА', 'БАЛАШИХА', 'БЕРДЯНСК', 'БУГУЛЬМА', 'БОРОДИНО', 'БАРАНОВИЧИ', 'БАКУ',
          'БРАТИСЛАВА', 'БОБРУЙСК', 'БРЕСТ', 'БЕНДЕРЫ', 'БОСТАД', 'БУИНСК', 'БЕЛОСТОК', 'БЕЛЬФОР', 'БРИСБЕН',
          'БОГОРОДИЦК', 'БАНДАР-СЕРИ-БЕГАВАН', 'БЫХОВ', 'БЕЛУ-ОРИЗОНТИ', 'БАНГАЛОР', 'БЕЙРУТ', 'БУРОС', 'БЕРЕЗОВСКИЙ',
          'БХУБАНЕШВАР', 'БОРИСОВ', 'БРЕМЕН', 'БИРОБИДЖАН', 'БАРТЛСВИЛЛ', 'БАЛТИМОР', 'БРАНДОН', 'БАТОН-РУЖ',
          'БАЛАКОВО', 'БОНН', 'БРЕЙНТРИ', 'БРАУНАУ-АМ-ИНН', 'БАНГКОК', 'БАХЧИСАРАЙ', 'БАЛАКЛАВА', 'БУЭНОС-АЙРЕС',
          'БИЙСК', 'БЛАНТАЙР', 'БАГДАД', 'БУКА', 'БЕРДСК', 'БЕЛАЯ КАЛИТВА', 'БИШКЕК', 'БАЛТИЙСК', 'БУДАПЕШТ',
          'БЕРЕЗНИКИ', 'БОСТОН', 'БЕРЕЗИНО', 'БОГОТА', 'БУДЕННОВСК', 'БРЮССЕЛЬ', 'БОГОРОДСК', 'БЛАГОВЕЩЕНСК', 'БРНО',
          'БЕЛОРЕЦК', 'БЕЛФАСТ', 'БРАЙЗАХ-НА-РЕЙНЕ', 'БАРНАУЛ', 'БРАЗЗАВИЛЬ', 'БАГРАТИОНОВСК', 'БАНЖУЛ', 'БРЯНСК',
          'БЫДГОЩ'],
    'В': ['ВЕРХНЕДНЕПРОВСК', 'ВЫШНИЙ ВОЛОЧЕК', 'ВЕТКА', 'ВЕЛЬСК', 'ВЕЛИКИЕ ЛУКИ', 'ВИЛЮЙСК', 'ВЛАДИКАВКАЗ', 'ВОЛЬСК',
          'ВОЛЖСКИЙ', 'ВИШАКХАПАТНАМ', 'ВОТКИНСК', 'ВИФЛЕЕМ', 'ВОСКРЕСЕНСК', 'ВИНДХУК', 'ВОЛОЧИСК', 'ВАНКУВЕР', 'ВАРНА',
          'ВЛАДИМИР-ВОЛЫНСКИЙ', 'ВЕНА', 'ВАДУЦ', 'ВАЛМИЕРА', 'ВЕЛЬС', 'ВРОЦЛАВ', 'ВИКТОРИЯ', 'ВОЛГОДОНСК', 'ВЛАДИМИР',
          'ВИЛЬНЮС', 'ВИННИЦА', 'ВИЛЕЙКА', 'ВЕНЕРСБОРГ', 'ВЫБОРГ', 'ВЕРХНЕДВИНСК', 'ВАЛДАЙ', 'ВЯЗЬМА', 'ВЬЕНТЬЯН',
          'ВОРКУТА', 'ВАШИНГТОН', 'ВЛАДИВОСТОК', 'ВИДНОЕ', 'ВЕЙМАР', 'ВАРШАВА', 'ВОЛОКОЛАМСК', 'ВОЛГОГРАД', 'ВОЛОГДА',
          'ВОРОНЕЖ', 'ВЫСОЦК', 'ВЕЛИКИЙ НОВГОРОД', 'ВЕЛЛИНГТОН'],
    'Г': ['ГРОДНО', 'ГВАДАЛАХАРА', 'ГАБОРОНЕ', 'ГАБАЛА', 'ГВАДАР', 'ГОРИ', 'ГДАНЬСК', 'ГАМБУРГ', 'ГДОВ', 'ГУКОВО',
          'ГАОСЮН', 'ГОРОДОК', 'ГРОЗНЫЙ', 'ГААГА', 'ГОМЕЛЬ', 'ГУАНЧЖОУ', 'ГОРКИ', 'ГЛАЗОВ', 'ГЕРАТ', 'ГРАЦ', 'ГАЛАЦ',
          'ГАННОВЕР', 'ГАЛЛЕ', 'ГРЕЙТ-ДАНМОУ', 'ГЛАЗГО', 'ГАВАНА', 'ГОНОЛУЛУ', 'ГИЛРОЙ', 'ГИСКАР', 'ГАЗНИ', 'ГУСЕВ',
          'ГОРНО-АЛТАЙСК', 'ГАТЧИНА', 'ГВАТЕМАЛА', 'ГЕТЕБОРГ', 'ГОРОХОВ', 'ГАГРА', 'ГЕЛЬЗЕНКИРХЕН', 'ГОЛД-КОСТ'],
    'Д': ['ДЖИДДА', 'ДАР-ЭС-САЛАМ', 'ДУРБАН', 'ДАЙР-ЭЗ-ЗАУР', 'ДУЙСБУРГ', 'ДАКАР', 'ДУВР', 'ДЗЕРЖИНСК', 'ДУБРОВНО',
          'ДОРТМУНД', 'ДАРЪА', 'ДОЛГОПРУДНЫЙ', 'ДОБРУШ', 'ДАНИДИН', 'ДЕЛФТ', 'ДАЛЬНЕРЕЧЕНСК', 'ДЕРБЕНТ', 'ДЖЕЛАЛАБАД',
          'ДРОГОБЫЧ', 'ДЖИБУТИ', 'ДЮРТЮЛИ', 'ДНЕПР', 'ДЕНВЕР', 'ДЖВАРИ', 'ДЕЛИ', 'ДЫРЕ-ДАУА', 'ДЮССЕЛЬДОРФ', 'ДУШАНБЕ',
          'ДЖЕКСОНВИЛЛ', 'ДРУЖКОВКА', 'ДЕТРОЙТ', 'ДЖАНКОЙ', 'ДУМА', 'ДУБАЙ', 'ДЕРА-ИСМАИЛ-ХАН', 'ДЭБРЭ-ЗЭЙТ',
          'ДЖОХОР-БАРУ', 'ДУБНА', 'ДУАЛА', 'ДАЛЛАС', 'ДУМЬЯТ', 'ДРЕЗДЕН', 'ДАМАСК', 'ДЖЕРАБУЛУС', 'ДОНЕЦК',
          'ДОМОДЕДОВО', 'ДЖАКАРТА', 'ДУБОССАРЫ', 'ДУБЛИН', 'ДАЛМАТОВО', 'ДОХА'],
    'Е': ['ЕВПАТОРИЯ', 'ЕЛЕЦ', 'ЕЛАБУГА', 'ЕНИСЕЙСК', 'ЕВЛАХ', 'ЕКАТЕРИНБУРГ', 'ЕВЛЕ', 'ЕЛЬНЯ', 'ЕССЕНТУКИ',
          'ЕНАКИЕВО'],
    'Ж': ['ЖЕШУВ', 'ЖОДИНО', 'ЖЕНЕВА', 'ЖЛОБИН', 'ЖУКОВСКИЙ', 'ЖЕЛЕЗНОГОРСК', 'ЖИТОМИР', 'ЖЕЗКАЗГАН'],
    'З': ['ЗЕЛЕНОГРАД', 'ЗЕЛЕНОГРАДСК', 'ЗЛАТОУСТ', 'ЗАГАТАЛА', 'ЗАПОРОЖЬЕ', 'ЗАГРЕБ', 'ЗОЛОТОЕ', 'ЗЕЛЬДЕН',
          'ЗЕЛЕНОДОЛЬСК', 'ЗВЕНИГОРОД', 'ЗАВОДОУКОВСК', 'ЗЕФЕЛЬД-ИН-ТИРОЛЬ', 'ЗАСЛАВЛЬ'],
    'И': ['ИНДИАН-УЭЛЛС', 'ИЗМИР', 'ИШИМБАЙ', 'ИВАНО-ФРАНКОВСК', 'ИОКОГАМА', 'ИЛАМ', 'ИВАНТЕЕВКА', 'ИЖЕВСК',
          'ИЕРУСАЛИМ', 'ИСЛАМАБАД', 'ИГАРКА', 'ИРКУТСК', 'ИВАНОВО', 'ИЧНЯ', 'ИШИМ', 'ИДЛИБ', 'ИЗМАИЛ', 'ИНЧХОН', 'ИЗЮМ',
          'ИРБИТ'],
    'Й': ['ЙОШКАР-ОЛА', 'ЙОХАННЕСБУРГ', 'ЙОРК', 'ЙЕЗД', 'ЙЕНА', 'ЙЁНЧЁПИНГ', 'ЙЕР', 'ЙЕХУД-МОНОССОН', 'ЙЕШИЛКЁЙ',
          'ЙИРГА-АЛЕМ', 'ЙОДЕМИШ', 'ЙОЗГАТ', 'ЙОКНЕАМ', 'ЙОЛ', 'ЙОМРА', 'ЙОНКЕРС', 'ЙОЭНСУУ', 'ЙЫГЕВА', 'ЙЫЛДЫЗЕЛИ',
          'ЙЫХВИ'],
    'К': ['КОВРОВ', 'КАЛУГА', 'КРЕМЕНЧУГ', 'КОШИЦЕ', 'КИРОВ', 'КАМБАРКА', 'КИГАЛИ', 'КЕЛЬМЕ', 'КОРДОВА', 'КЛИМОВИЧИ',
          'КРАМАТОРСК', 'КИНГИСЕПП', 'КАЛИНИНГРАД', 'КАРЛОВЫ ВАРЫ', 'КИНШАСА', 'КАМЕНКА', 'КУЛЯБ', 'КЕМЕРОВО',
          'КАМЫШЛОВ', 'КАТМАНДУ', 'КОНОТОП', 'КЭРНС', 'КАИР', 'КАНДАГАР', 'КИНГСТОН', 'КОЛОМЫЯ', 'КИСМАЙО', 'КОЛОМНА',
          'КАРЛСРУЭ', 'КУКУТА', 'КАСАБЛАНКА', 'КРОПИВНИЦКИЙ', 'КСТОВО', 'КИРКЕНЕС', 'КИРКУК', 'КУЗНЕЦК', 'КУРСК',
          'КАТАЙСК', 'КРАСНОДАР', 'КАРАКАС', 'КИРОВО-ЧЕПЕЦК', 'КАМЫШИН', 'КАБО-САН-ЛУКАС', 'КОНСТАНТИНА', 'КИТО',
          'КИРЬЯТ-ШМОНА', 'КИВЕРЦЫ', 'КУРИТИБА', 'КЕТЧИКАН', 'КРАСНОПЕРЕКОПСК', 'КРОНШТАДТ', 'КИСЛОВОДСК',
          'КРАСНОКАМСК', 'КЕЛЬН', 'КАТАВ-ИВАНОВСК', 'КАМЕНСК-ШАХТИНСКИЙ', 'КРАСНОТУРЬИНСК', 'КАЛУШ',
          'КОМСОМОЛЬСК-НА-АМУРЕ', 'КОНДОПОГА', 'КРАСНОУФИМСК', 'КЕЛОУНА', 'КОСТЮКОВИЧИ', 'КОРОЛЕВ', 'КАБУЛ', 'КАГАРЛЫК',
          'КИЦБЮЭЛЬ', 'КРУ', 'КУТАИСИ', 'КРАКОВ', 'КАРДИФФ', 'КАСПИЙСК', 'КИТЧЕНЕР', 'КРАСНОАРМЕЙСК', 'КОЧАБАМБА',
          'КАЛГАРИ', 'КАРПИНСК', 'КАНЗАС-СИТИ', 'КОБЛЕНЦ', 'КОПЕЙСК', 'КЛИН', 'КАМПАЛА', 'КЕМБРИДЖ', 'КИЕВ', 'КИРОВСК',
          'КОЗЬМОДЕМЬЯНСК', 'КЕРЧЬ', 'КАУНАС', 'КИШИНЕВ', 'КАЛИНКОВИЧИ', 'КОСТОМУКША', 'КРАСНОГОРСК', 'КОЛОМБО',
          'КОВЕЛЬ', 'КУБИНКА', 'КОТОНУ', 'КОНАКОВО', 'КЫЗЫЛ', 'КОНАКРИ', 'КИРОВГРАД', 'КУРГАН', 'КОСТРОМА',
          'КРАЙСТЧЕРЧ', 'КОБЕ', 'КОПЕНГАГЕН', 'КУНГУР', 'КВАНДЖУ', 'КАМЕНСК-УРАЛЬСКИЙ', 'КАЛАМАЗУ', 'КАЛЬКУТТА',
          'КУАЛА-ЛУМПУР', 'КЕЙПТАУН', 'КРАСНОЯРСК', 'КАМЕНЬ-КАШИРСКИЙ', 'КРИВОЙ РОГ', 'КАЗАНЬ', 'КРИЧЕВ', 'КИЗЛЯР',
          'КЛАГЕНФУРТ-АМ-ВЕРТЕРЗЕ'],
    'Л': ['ЛИАКВАТПУР', 'ЛАБЫТНАНГИ', 'ЛЮБЕРЦЫ', 'ЛЕВЕРКУЗЕН', 'ЛЮБЛИН', 'ЛЮБЛЯНА', 'ЛОЗОВАЯ', 'ЛЬЕЙДА', 'ЛОМЕ',
          'ЛИБРЕВИЛЬ', 'ЛА-ПАС', 'ЛАГОС', 'ЛАЭ', 'ЛИДС', 'ЛИВЕРПУЛЬ', 'ЛУКСОР', 'ЛУАНДА', 'ЛЮКСЕМБУРГ', 'ЛОДЗЬ',
          'ЛЮНЕБУРГ', 'ЛАШКАРГАХ', 'ЛОС-АНДЖЕЛЕС', 'ЛА-ГУАЙРА', 'ЛЕКСАНД', 'ЛЬВОВ', 'ЛИОН', 'ЛЕЙПЦИГ', 'ЛОБАМБА',
          'ЛОНГЙИР', 'ЛЬЕЖ', 'ЛЮБОМЛЬ', 'ЛИДЧЕПИНГ', 'ЛИССАБОН', 'ЛИНЦ', 'ЛУЦК', 'ЛЕСТЕР', 'ЛИПЕЦК', 'ЛЕПЕЛЬ', 'ЛУНД',
          'ЛУСАКА', 'ЛИМА', 'ЛАТАКИЯ', 'ЛУГАНСК', 'ЛАС-ВЕГАС', 'ЛОНДОН', 'ЛЮДИНОВО', 'ЛАХОР', 'ЛЕСНОЙ', 'ЛОМОНОСОВ',
          'ЛОБНЯ', 'ЛУГА'],
    'М': ['МАРАВИ', 'МЕДИНА', 'МАЛЬМЕ', 'МБАБАНЕ', 'МАХАЧКАЛА', 'МУРОМ', 'МОСУЛ', 'МИНУСИНСК', 'МАЛАЯ ВИШЕРА',
          'МИРНОГРАД', 'МИННЕАПОЛИС', 'МУМБАИ', 'МУРМАНСК', 'МАГАС', 'МОЛОДЕЧНО', 'МЮНХЕН', 'МАНГЕЙМ', 'МАГНИТОГОРСК',
          'МОМБАСА', 'МАНИЛА', 'МСТИСЛАВЛЬ', 'МАРТУНИ', 'МАНЗИНИ', 'МЕХИКО', 'МИЧУРИНСК', 'МАНАУС', 'МЫТИЩИ',
          'МАРАКАЙБО', 'МАСКАТ', 'МОГИЛЕВ', 'МЕДВЕЖЬЕГОРСК', 'МЕЛИТОПОЛЬ', 'МОНТЕРРЕЙ', 'МАЙАМИ', 'МАНБИДЖ', 'МАНАМА',
          'МОНТЕВИДЕО', 'МИНСК', 'МОСКВА', 'МАЙДУГУРИ', 'МАЙКОП', 'МУР', 'МАГАДАН', 'МОЖАЙСК', 'МИАСС', 'МАРРАКЕШ',
          'МЕЛЬБУРН', 'МАНАГУА', 'МАЗАРИ-ШАРИФ', 'МЕККА', 'МАРЬИНА ГОРКА', 'МАПУТУ', 'МАРСЕЛЬ', 'МОНКТОН', 'МОДЕНА',
          'МАНЧЕСТЕР', 'МОГАДИШО'],
    'Н': ['НЕВИННОМЫССК', 'НЬЮ-ДЕЛИ', 'НОВОВОЛЫНСК', 'НУР-СУЛТАН', 'НОВОСИБИРСК', 'НАНКИН', 'НЬЮПОРТ', 'НАЙРОБИ',
          'НДЖАМЕНА', 'НЕГОМБО', 'НИЖНЕВАРТОВСК', 'НЬЮ-ЙОРК', 'НЭШВИЛЛ', 'НАЗРАНЬ', 'НЕВЬЯНСК', 'НОВОШАХТИНСК',
          'НЕФТЕКАМСК', 'НОРТКЛИФФ', 'НОВОРОССИЙСК', 'НОВОКУЙБЫШЕВСК', 'НОРМАН', 'НОВОЧЕРКАССК', 'НАРО-ФОМИНСК',
          'НУАЙОН', 'НИЖНИЙ НОВГОРОД', 'НАГАНО', 'НЮЧЕПИНГ', 'НОВОКУЗНЕЦК', 'НЕСВИЖ', 'НИЖНИЙ ТАГИЛ', 'НУРВИК',
          'НОВОПОЛОЦК', 'НАБЕРЕЖНЫЕ ЧЕЛНЫ', 'НИКОСИЯ', 'НЕФТЕЮГАНСК', 'НОТТИНГЕМ', 'НОВЕ-МЕСТО-НА-МОРАВЕ', 'НОГИНСК',
          'НУАКШОТ', 'НИАМЕЙ', 'НОВЫЙ ОРЛЕАН', 'НАХОДКА', 'НОВОЧЕБОКСАРСК', 'НОРИЛЬСК', 'НИКЕЯ', 'НЕАПОЛЬ', 'НЮРНБЕРГ',
          'НАССАУ', 'НИКОЛАЕВСК-НА-АМУРЕ', 'НОВЫЙ УРЕНГОЙ', 'НИНОЦМИНДА', 'НИКОЛАЕВ', 'НИЖНЕКАМСК', 'НАРЬЯН-МАР',
          'НОЯБРЬСК', 'НОВОМОСКОВСК'],
    'О': ['ОРХУС', 'ОРСК', 'ОРЕХОВО-ЗУЕВО', 'ОСТРАВА', 'ОЧАКОВ', 'ОМСК', 'ОРЕНБУРГ', 'ОТТАВА', 'ОСЛО', 'ОРЕ',
          'ОКТЯБРЬСКИЙ', 'ОЛЬГИН', 'ОПА-ЛОКА', 'ОМАХА', 'ОКЛЕНД', 'ОБНИНСК', 'ОРША', 'ОДЕССА', 'ОРЛАНДО', 'ОБЕРСТДОРФ',
          'ОКЛАХОМА-СИТИ', 'ОСИПОВИЧИ', 'ОРЕЛ', 'ОШМЯНЫ', 'ОШ', 'ОЛЕНЕГОРСК', 'ОДИНЦОВО'],
    'П': ['ПАНКАЛПИНАНГ', 'ПИТЕРБОРО', 'ПАРИЖ', 'ПУНА', 'ПЕВЕК', 'ПЕНЗА', 'ПРАГА', 'ПЕТРИКОВ', 'ПИВДЕННОЕ', 'ПУШКИН',
          'ПОРТ-О-ПРЕНС', 'ПАНАМА', 'ПОДПОРОЖЬЕ', 'ПОРТ-ОФ-СПЕЙН', 'ПЛОЦК', 'ПАГАН', 'ПЛЕЙНО', 'ПОДГОРИЦА',
          'ПАНАМА-СИТИ', 'ПОЗНАНЬ', 'ПОДОЛЬСК', 'ПЕРВОУРАЛЬСК', 'ПАЛУ', 'ПРИОЗЕРСК', 'ПОРТ-ЛУИ',
          'ПЕТРОПАВЛОВСК-КАМЧАТСКИЙ', 'ПЯТИГОРСК', 'ПИТТСБУРГ', 'ПЕТРОПАВЛОВСК', 'ПАЛЬМИРА', 'ПАТТАЙЯ', 'ПИЗА',
          'ПАВЛОДАР', 'ПРИНС-АЛЬБЕРТ', 'ПРОКОПЬЕВСК', 'ПУЛИ-ХУМРИ', 'ПАЛЕМБАНГ', 'ПЕТРОЗАВОДСК', 'ПУШКИНО', 'ПУСАН',
          'ПОЛТАВА', 'ПЕРЕСЛАВЛЬ-ЗАЛЕССКИЙ', 'ПЛАНТЕЙШЕН', 'ПНОМПЕНЬ', 'ПСКОВ', 'ПЕКИН', 'ПАЛМ-СПРИНГС', 'ПЛЕС',
          'ПРЕТОРИЯ', 'ПАВЛОВСКИЙ ПОСАД', 'ПОРТО-НОВО', 'ПЕТЕРГОФ', 'ПОЛОЦК', 'ПИНСК', 'ПЕРМЬ', 'ПАРАДАЙС'],
    'Р': ['РЕДИНГ', 'РУБЦОВСК', 'РАМАЛЛА', 'РОТТЕРДАМ', 'РЯЗАНЬ', 'РЫБИНСК', 'РИО-ДЕ-ЖАНЕЙРО', 'РАМЕНСКОЕ', 'РИЕКА',
          'РОСТОВ-НА-ДОНУ', 'РЕУТОВ', 'РОССОШЬ', 'РАНН', 'РИГА', 'РИЧМОНД', 'РОСТОВ', 'РЕЙКЬЯВИК', 'РАВАЛПИНДИ',
          'РОГАЧЕВ', 'РОВНО', 'РЕЧИЦА', 'РЖЕВ', 'РОЖИЩЕ', 'РАБАТ', 'РИЗЕ', 'РИМ'],
    'С': ['СНЕЖНОЕ', 'СНЕЖИНСК', 'СЕВЕРОУРАЛЬСК', 'САНТА-ФЕ', 'СТАРЫЙ ОСКОЛ', 'САРАПУЛ', 'СТРУМИЦА', 'САН-ПАУЛУ',
          'СУХУМ', 'САН-АНТОНИО', 'СУРАБАЯ', 'СТОЛБЦЫ', 'САМАРРА', 'СТЕРЛИТАМАК', 'САРИ-ПУЛЬ', 'САРОВ', 'СКОПЬЕ',
          'СОЛФОРД', 'СМОЛЕВИЧИ', 'СУДАК', 'СИЛЬКЕБОРГ', 'СЛУЦК', 'СЕЙНЯЙОКИ', 'САН-ФРАНЦИСКО', 'САЗЕРЛЕНД-СПРИНГС',
          'СЕУЛ', 'САРАГОСА', 'СОВЕТСК', 'САНТА-ЭЛЕНА-ДЕ-УАЙРЕН', 'СЕНТ-ДЖОН', 'САН-САЛЬВАДОР', 'СОЛСБЕРИ', 'СТАМБУЛ',
          'САНТО-ДОМИНГО', 'СЕВЕРОДВИНСК', 'САСКАТУН', 'САНТА-МОНИКА', 'САН-ДИЕГО', 'САН-АНТОНИО-ДЕЛЬ-ТАЧИРА', 'СЕННО',
          'СЕКЕШФЕХЕРВАР', 'САНКТ-ПЕТЕРБУРГ', 'СОЧИ', 'СПИРМЕН', 'САРАЕВО', 'СЕМИКАРАКОРСК', 'СИДНЕЙ', 'САНТЬЯГО',
          'СУКРЕ', 'СОЛИГОРСК', 'САМАРКАНД', 'СУХОЙ ЛОГ', 'СЕРПУХОВ', 'СОФИЯ', 'САРАНСК', 'СУРГУТ', 'САНТА-КЛАРА',
          'САМАРА', 'САЛАВАТ', 'СМОЛЕНСК', 'САКРАМЕНТО', 'СЫКТЫВКАР', 'САЛОНИКИ', 'СВЕБОДЗИН', 'СЕВЕРСК', 'СЕВАСТОПОЛЬ',
          'СИБАЙ', 'САН-ХУАН', 'САРАТОВ', 'СРЕДНЕУРАЛЬСК', 'СТАРЫЕ ДОРОГИ', 'СЕНТ-ЛУИС', 'СЫЗРАНЬ', 'СЛАВЯНСК',
          'СВЕТЛОГОРСК', 'СОЛНЕЧНОГОРСК', 'СТАВРОПОЛЬ', 'САНА', 'СЕВЕРОМОРСК', 'СЕСТРОРЕЦК', 'САЛЕХАРД', 'СТЕПАНАКЕРТ',
          'СТЕРЛИНГ', 'САН-ХОСЕ', 'САФОНОВО', 'СЕРГИЕВ ПОСАД', 'СЕРОВ', 'СОЛТ-ЛЕЙК-СИТИ', 'СУМЫ', 'СЕВЕРНЫЙ ОГДЕН',
          'СИЭТЛ', 'СИМФЕРОПОЛЬ'],
    'Т': ['ТАЙБЭЙ', 'ТАУЗАНД-ОКС', 'ТИРАСПОЛЬ', 'ТОРОНТО', 'ТАГАНРОГ', 'ТРИПОЛИ', 'ТРИР', 'ТОРЕЦК', 'ТЕГЕРАН', 'ТАРТУ',
          'ТОКИО', 'ТРНАВА', 'ТАИЗ', 'ТРШИНЕЦ', 'ТИЛБУРГ', 'ТУЛУН', 'ТАЛЛИН', 'ТАМПЕРЕ', 'ТАМАНРАССЕТ', 'ТАЙЧЖУН',
          'ТИРАНА', 'ТЕМРЮК', 'ТРЕХГОРНЫЙ', 'ТОСНО', 'ТРУСКАВЕЦ', 'ТУАПСЕ', 'ТОЛЬЯТТИ', 'ТЭГУ', 'ТАРАПОТО', 'ТУВУМБА',
          'ТУЛА', 'ТАШКЕНТ', 'ТБИЛИСИ', 'ТВЕРЬ', 'ТУНИС', 'ТЕГУСИГАЛЬПА', 'ТЭДЖОН', 'ТЕЛЬ-АВИВ', 'ТЮМЕНЬ', 'ТЕРНОПОЛЬ',
          'ТОМСК', 'ТУРКУ', 'ТАМБОВ', 'ТАРРАГОНА', 'ТУРИН'],
    'У': ['УРАЛЬСК', 'УМЕО', 'УФА', 'УМАГ', 'УРЮПИНСК', 'УГЛИЧ', 'УХТА', 'УСТЬ-КАТАВ', 'УЛЬЯНОВСК', 'УОРИК', 'УАГАДУГУ',
          'УЛАН-БАТОР', 'УСТИЛУГ', 'УЭСТ-ПАЛМ-БИЧ', 'УММ-ЭЛЬ-БАВАКИ', 'УОТЕРТАУН', 'УССУРИЙСК', 'УСТЬ-КАМЕНОГОРСК',
          'УЛАН-УДЭ', 'УОЛТЕМ'],
    'Ф': ['ФРАНКФУРТ-НА-МАЙНЕ', 'ФАНИПОЛЬ', 'ФАРАХ', 'ФРЯЗИНО', 'ФЕОДОСИЯ', 'ФИЕРИ', 'ФУЧЖОУ', 'ФОРТ-ЛОДЕРДЕЙЛ',
          'ФИНИКС'],
    'Х': ['ХАРАРЕ', 'ХИХОН', 'ХОД-ХА-ШАРОН', 'ХЕЛЬСИНКИ', 'ХОШИМИН', 'ХАЛА', 'ХАБАРОВСК', 'ХУДЖАНД', 'ХАНТЫ-МАНСИЙСК',
          'ХАЙДАРАБАД', 'ХАЙФА', 'ХАСАВЮРТ', 'ХАШУРИ', 'ХОТОРН', 'ХУАХИН', 'ХАРТУМ', 'ХАРБИН', 'ХОНИАРА', 'ХАРЬКОВ',
          'ХЕРСОНЕС ТАВРИЧЕСКИЙ', 'ХЕРСОН', 'ХМЕЛЬНИЦКИЙ', 'ХОХФИЛЬЦЕН', 'ХАНОЙ', 'ХОДЕЙДА', 'ХАРЛЕМ', 'ХИМКИ', 'ХАМА',
          'ХИРОСИМА', 'ХОБАРТ', 'ХЬЮСТОН'],
    'Ц': ['ЦУГ', 'ЦЕЛЕ', 'ЦЮРИХ', 'ЦХИНВАЛИ', 'ЦИНЦИННАТИ'],
    'Ч': ['ЧИАНГМАЙ', 'ЧИКАГО', 'ЧОЛПОН-АТА', 'ЧАУСЫ', 'ЧЕБОКСАРЫ', 'ЧИПРОВЦИ', 'ЧЕРНОВЦЫ', 'ЧЕРНИГОВ', 'ЧЕРКАССЫ',
          'ЧЕННАИ', 'ЧЕРИКОВ', 'ЧЭНДУ', 'ЧЕРЕПОВЕЦ', 'ЧУГУЕВ', 'ЧИТА', 'ЧЕЛЯБИНСК', 'ЧАСОВ ЯР', 'ЧИКО', 'ЧЕРВЕНЬ',
          'ЧУСОВОЙ', 'ЧЬЕРНА-НАД-ТИСОУ', 'ЧЕРКЕССК', 'ЧЕРНОБЫЛЬ', 'ЧЕБАРКУЛЬ'],
    'Ш': ['ШАЦК', 'ШАДРИНСК', 'ШАРЛОТТ', 'ШАРМ-ЭШ-ШЕЙХ', 'ШАТУРА', 'ШКЛОВ', 'ШАНХАЙ', 'ШТУТГАРТ', 'ШЕФФИЛД', 'ШАХТЫ',
          'ШАМОРИН', 'ШИБАРГАН', 'ШИХАНЫ', 'ШИНДАНД', 'ШАЛИ', 'ШЭНЬЧЖЭНЬ', 'ШЕМАХЫ', 'ШЫМКЕНТ'],
    'Щ': ['ЩАВНИЦА', 'ЩАВНО-ЗДРУЙ', 'ЩЕЛКОВО', 'ЩЕЦИН'],
    'Э': ['ЭРФУРТ', 'ЭСТЕРСУНД', 'ЭР-РАККА', 'ЭЛИСТА', 'ЭСПОО', 'ЭВЕРЕТТ', 'ЭЛЕКТРЕНАЙ', 'ЭЛЬ-АЮН', 'ЭРНШЕЛЬДСВИК',
          'ЭЛЬ-ХИЛЛА', 'ЭЛЬ-ГИЗА', 'ЭЛЬ-ПАСО', 'ЭЙНДХОВЕН', 'ЭДИНБУРГ', 'ЭР-РИЯД', 'ЭЛЬ-КАМЫШЛЫ', 'ЭЙЛАТ', 'ЭШБОРН',
          'ЭЛЬ-КУВЕЙТ', 'ЭЙМСБЕРИ', 'ЭЛЬ-АРИШ', 'ЭЛЕКТРОСТАЛЬ', 'ЭКЛСХОЛЛ', 'ЭДМОНТОН', 'ЭНГЕЛЬС', 'ЭРБИЛЬ'],
    'Ю': ['ЮЖНАЯ ТАРАВА', 'ЮМА', 'ЮЖНО-САХАЛИНСК', 'ЮРМАЛА', 'ЮРЮЗАНЬ'],
    'Я': ['ЯБЛАНИЦА', 'ЯНГОН', 'ЯМБОЛ', 'ЯМУСУКРО', 'ЯУНДЕ', 'ЯБИНГ', 'ЯЛУТОРОВСК', 'ЯЛТА', 'ЯКУТСК', 'ЯРОСЛАВЛЬ'],
}

STORAGE_STUB = {}


class ResponseCode(Enum):
    ANSWER_TO_USER = "Город '{}' принят. Мой ход."
    INVALID_CITY = "Слово '{}' не похоже на название города - попробуйте ещё раз!"
    UNKNOWN_CITY = "Я ничего не знаю про город '{}'. Давайте договоримся, что вы называете только те города, которые я знаю?"
    CITY_ALREADY_USED = "Город '{}' уже был. Второй раз называть один и тот же город нельзя. Правила такие."
    CITY_WRONG_FIRST_LETTER = "Город '{}' не подходит. Он должен начинаться на букву '{}'."
    GAME_OVER = "Я не знаю больше городов :( Вы выиграли! Примите мои поздравления!"


class IncorrectCityName(Exception):
    pass


class IncorrectUserSession(Exception):
    pass


class MovementInfo():
    def __init__(self, response_code: ResponseCode, city: str = "", last_letter: str = ""):
        self.response_code = response_code
        self.city = city
        self.last_letter = last_letter

    def __repr__(self):
        return f"{self.response_code}: {self.city} / {self.last_letter}"


def normalize_city_name(city_name: str) -> str:
    normalized = city_name.upper().replace("Ё", "Е")
    return normalized


def validate_city_name(city_name: str) -> (bool, str):
    # ['Аньадырь', '', 'fsdkj', 'мяу1243sefjsdf', 'Ростов-на-Дону', 'Ростов-на-', '-на-Дону',
    # 'Посторонним-В', 'марий-эл', 'Нижний Новгород', 'Нижний Новгород  ', 'Нижний Новгород-с-дефисом',
    # 'Новгород-с-дефисом', 'ьгород', 'Ъ', 'Королёв']

    if len(city_name) == 0:
        return False, "Вы не ввели имя города"

    if city_name[0] in ['ь', 'Ь', 'ъ', 'Ъ']:
        return False, "Имя города не может начинаться с мягкого или твёрдого знака"

    if not re.match("^([а-яА-ЯёЁ]+([- ][а-яА-ЯёЁ])*)+$", city_name):
        return False, "Имя города должно содержать только русские буквы, пробел или дефис"

    return True, None


def get_last_letter(city_name: str) -> str:
    purified = city_name.upper().replace('-', '').replace('Ь', '').replace('Ъ', '').replace('Ы', '')

    if len(purified) == 0:
        raise IncorrectCityName("Incorrect city name")

    return purified[-1]


class CitiesGameSession():
    def __init__(self, user_session_id: str):
        if not user_session_id:
            raise IncorrectUserSession("User session is not set")

        self.cities_available: Dict[str, List[str]] = {}
        self.cities_used: List[str] = []
        self.current_last_letter: str = ""
        self.current_city_entered = ""
        self.dictionary_size = 20

        if self.game_exists(user_session_id):
            self.user_session_id = user_session_id
            self.load_game()
        else:
            self.create_new_game(user_session_id)

    def create_new_game(self, user_session_id: str) -> None:
        self.user_session_id = user_session_id

        self.cities_available = self.__generate_cities_list()
        self.cities_used = []
        self.current_last_letter = ""
        self.current_city_entered = ""

        self.save_game()

    def game_exists(self, user_session_id) -> bool:
        result = user_session_id in STORAGE_STUB
        return result

    def save_game(self) -> None:
        serialized = {
            "cities_available": self.cities_available,
            "cities_used": self.cities_used,
            "current_last_letter": self.current_last_letter,
            "current_city_entered": self.current_city_entered,
            "dictionary_size": self.dictionary_size
        }

        STORAGE_STUB[self.user_session_id] = serialized

    def load_game(self) -> None:
        serialized = STORAGE_STUB[self.user_session_id]

        self.cities_available: Dict[str, List[str]] = serialized["cities_available"]
        self.cities_used: List[str] = serialized["cities_used"]
        self.current_last_letter: str = serialized["current_last_letter"]
        self.current_city_entered: str = serialized["current_city_entered"]
        self.dictionary_size = serialized["dictionary_size"]

    def do_move(self, input_city: str = "") -> MovementInfo:

        if input_city:
            is_success, movement_info = self.__process_input_city(input_city)
            if not is_success:
                return movement_info

        result = self.__answer_to_user()

        return result

    def __process_input_city(self, input_city: str) -> (bool, MovementInfo):
        city_name_normalized = normalize_city_name(input_city)

        is_name_valid, err = validate_city_name(city_name_normalized)
        if not is_name_valid:
            return False, MovementInfo(response_code=ResponseCode.INVALID_CITY,
                                       last_letter=self.current_last_letter)

        if city_name_normalized[0] not in KNOWN_CITIES \
                or city_name_normalized not in KNOWN_CITIES[city_name_normalized[0]]:
            return False, MovementInfo(response_code=ResponseCode.UNKNOWN_CITY,
                                       last_letter=self.current_last_letter)

        if self.__is_city_redeemed(city_name_normalized):
            return False, MovementInfo(response_code=ResponseCode.CITY_ALREADY_USED,
                                       last_letter=self.current_last_letter)

        if self.current_last_letter and city_name_normalized[0] != self.current_last_letter:
            return False, MovementInfo(response_code=ResponseCode.CITY_WRONG_FIRST_LETTER,
                                       last_letter=self.current_last_letter)

        self.current_city_entered = city_name_normalized
        self.__redeem_city(city_name_normalized)

        return True, None

    def __answer_to_user(self) -> MovementInfo:
        city = self.__pick_random_city(self.current_last_letter)

        if not city:
            self.save_game()
            return MovementInfo(response_code=ResponseCode.GAME_OVER)

        self.__redeem_city(city)

        self.save_game()
        return MovementInfo(city=city, last_letter=self.current_last_letter, response_code=ResponseCode.ANSWER_TO_USER)

    def __generate_cities_list(self) -> Dict[str, List[str]]:
        all_cities = deepcopy(KNOWN_CITIES)

        letter_samples = []

        # step 1 sample all letters
        for key in all_cities.keys():
            city = random.choice(all_cities[key])
            letter_samples.append(city)
            all_cities[key].remove(city)

        # step 2 add random cities
        if self.dictionary_size > len(letter_samples):
            tmp_array = []
            for key in all_cities:
                tmp_array += all_cities[key]

            available_cities = random.sample(tmp_array,
                                             k=min(self.dictionary_size - len(letter_samples), len(tmp_array)))
            available_cities += letter_samples
        else:
            available_cities = letter_samples

        result: Dict[str, List[str]] = {}

        for city in available_cities:
            first_letter = city[0].upper()
            if first_letter not in result:
                result[first_letter] = [city.upper()]
            else:
                result[first_letter].append(city.upper())

        return result

    def __pick_random_city(self, letter: str) -> str:
        if not letter:
            key = random.choice(list(self.cities_available))
        else:
            key = letter

        if (key not in self.cities_available) or (self.cities_available[key] == []):
            return ""

        return random.choice(self.cities_available[key])

    def __is_city_redeemed(self, city_name_normalized: str) -> bool:
        if not city_name_normalized:
            raise IncorrectCityName("City name should not be empty!")

        return city_name_normalized in self.cities_used

    def __redeem_city(self, city_name_normalized: str) -> None:
        if not city_name_normalized:
            raise IncorrectCityName("City name should not be empty!")

        first_letter = city_name_normalized[0].upper()
        if first_letter in self.cities_available:
            if city_name_normalized in self.cities_available[first_letter]:
                self.cities_available[first_letter].remove(city_name_normalized)

        self.cities_used.append(city_name_normalized)
        self.current_last_letter = get_last_letter(city_name_normalized)


class CitiesResponseBuilder:
    def __init__(self, user_session_id: str):
        self.user_session_id = user_session_id

    def movement_response(self, movement_info: MovementInfo, user_input: str = "") -> dict:

        if movement_info.response_code == ResponseCode.ANSWER_TO_USER:
            is_result_correct = True
            city_name = movement_info.city
        elif movement_info.response_code == ResponseCode.GAME_OVER:
            is_result_correct = True
            city_name = ""
        else:
            is_result_correct = False
            city_name = ""

        last_letter = movement_info.last_letter

        return self.__create_response(is_result_correct=is_result_correct,
                                      response_code=movement_info.response_code.name,
                                      city_name=city_name,
                                      last_letter=last_letter,
                                      last_user_input=user_input)

    def __create_response(self,
                          is_result_correct: bool,
                          response_code: str = "",
                          city_name: str = "",
                          last_letter: str = "",
                          last_user_input: str = ""):
        response = {
            "userSessionId": self.user_session_id,
            "isCorrect": is_result_correct,
            "ResponseCode": response_code,
            "CityName": city_name,
            "LastLetter": last_letter,
            "LastUserInput": last_user_input
        }

        return response


class CitiesRequestParser:
    def __init__(self, event: object):
        data_object = event
        self.user_session_id = data_object["userSessionId"]
        self.city = data_object["requestText"]


def lambda_handler(event, context):
    parser = CitiesRequestParser(event)
    game_session = CitiesGameSession(parser.user_session_id)
    result = game_session.do_move(parser.city)

    handler = CitiesResponseBuilder(parser.user_session_id)
    response = handler.movement_response(result, parser.city)

    return response
