* Напишете клас Santa
  Дядо Коледа е само един, така че класът трябва да е singleton.

  santa1 = Santa()
  santa2 = Santa()
  santa1 is santa2  # True
  Дядо Коледа може да получи желания за подаръци по два начина:

  Чрез обаждане по телефона:

  santa = Santa()
  santa(<дете>, <желание>)
  Тук "<дете>" е инстанция на клас, чийто метаклас дефинираме по-долу. "<желание>" е от тип str и съдържа текст, в който детето описва колко 
  е било послушно и какво иска да получи в замяна. По-долу описваме формата на желанието.

  Чрез писмо:

  santa = Santa()
  santa @ <писмо>
  Тук "<писмо>" е от тип str и съдържа текст, в който детето описва колко е било послушно и какво иска да получи в замяна. Освен това писмото 
  съдържа подпис на детето. По-долу описваме формата на писмото.

  Независимо дали съобщението е получено като писмо или чрез обаждане, текстът, който описва съобщението, може да съдържа произволно 
  съдържание. Ако съобщението е в писмо, очаква се някъде в писмото да има подпис. Независимо дали съобщението е от писмо или от обаждане, 
  някъде в него очакваме да има дефинирано желание за подарък.

  Подписът се дефинира като ред, в който има само цифри, които могат да са обградени от интервали, табулации и други whitespace символи. 
  Цифрите представляват идентитетът (резултатът от функцията id()) на детето, което е изпратило писмото.
  Желанието за подарък се дефинира като текст, който е обграден от кавички (") или апострофи (') и съдържа само букви от латинската азбука и/ 
  или цифри (може и интервали, разбира се). Няма да тестваме с текст, който има повече от една такава дефиниция, нито с такъв, в който тя 
  липсва.
  Примерно писмо:

  Скъпи Дядо Коледа,

  През по-голямата част от тази година бях много послушен!
  Понякога бях само леко "послушен", но т'ва не е никакъв проблем, защото всички сме хора и понякога искаме да теглим една '...' на всичко.
  Life is tough!
  Моля те донеси ми "Nimbus 2000".

  С много обич,
      2945526885456    
  Тук идентитетът на детето е 2945526885456, а подаръкът, който иска, е Nimbus 2000. Ако съобщението е получено като обаждане, за подаръка 
  важи същото, а подписът не е нужен, защото Дядо Коледа очаква обектът дете да влезе като отделен аргумент.

  Дядо Коледа е итерируем и може да се обходи с for. При това повече от веднъж. Всяко обхождане на Дядо Коледа трябва да върне подаръците, 
  които са му били поръчани за идващата Коледа. В реда, в който са били заявени.

  santa = Santa()
  santa @ <писмо, в което някое дете иска doll>
  santa(<дете>, <съобщение, което иска ball>)
  for present in santa:
      print(present)

  Горният код извежда:
  doll
  ball
  Дядо Коледа има публичен метод xmas, който не очаква аргументи. Извикването на метода раздава подаръци на децата. Правилата за раздаване на 
  подаръци:

  Дете получава подарък, като просто бъде извикано с един аргумент от тип str, който дефинира подаръка.

  santa = Santa()
  kid = <някаква инициализация на дете, която не зависи от вас>
  santa(kid, <писмо, в което детето иска drums>)
  santa.xmas()  # Очаква се детето `kid` да бъде извикано с очаквания подарък: kid('drums')
  Всяко дете получава това, което е поискало (с някои изключения):

  Ако детето е на повече от 5 години, Дядо Коледа спира да му дава подаръци. Как знаем кое дете на колко години е? Дядо Коледа магически 
  знае за всяко едно съществуващо дете. Когато след създаване на дете изминат 5 Коледи (5 извиквания на xmas), Дядо Коледа спира да се 
  занимава с него и не му праща нищо, независимо дали е получил писмо/обаждане от детето. Дядо Коледа се интересува от едно дете само в 
  продължение на 5 Коледи. На шестата вече го отсвирва.

  Дядо Коледа раздава подаръци само на послушните деца. Деца, които са хвърлили изключение в някой от публичните си методи през изминалата 
  година, са непослушни. Вместо подарък, те получават въглен, т.е. са извикани така: kid('coal'). Публичен метод дефинираме като метод, който 
  не започва с долна черта. Няма да тестваме с публични методи, които са декорирани с classmethod, staticmethod, property и подобни. Само с 
  нормални методи.

  Дядо Коледа раздава подаръци дори на деца, които не са му пратили писмо и не са се обадили. Подаръците, които Дядо Коледа раздава на такива 
  деца, съвпадат с най-желания подарък през изминалата година. Ако не е ясно кой е най-желан (има няколко желания с равен брой искания), 
  взима се един от най-желаните на случаен принцип.

  santa = Santa()
  kid1 = <някаква инициализация на дете, която не зависи от вас>
  kid2 = <някаква инициализация на дете, която не зависи от вас>
  kid3 = <някаква инициализация на дете, която не зависи от вас>
  santa @ <писмо от kid1, в което се иска tablet>
  santa @ <писмо от kid2, в което се иска tablet>
  santa.xmas()  # и трите деца получават tablet-и
  Ако през изминалата година (т.е. след последното извикване на xmas) Дядо Коледа не е получил нито едно желание (с писмо или с обаждане), 
  той не раздава нищо на никого. Явно магията на Коледа е отминала и всички са забравили за него.

  Ако през изминалата година (т.е. след последното извикване на xmas) Дядо Коледа е получил повече от едно желание от дадено дете, използва 
  се последното.

  На този етап сигурно се чудите как Дядо Коледа ще знае за всички деца, които казахме, че се инстанцират отвъд вашия контрол.

* Напишете метаклас Kid
  Всички деца, които ние ще създаваме, ще бъдат създадени от класове, които използват този метаклас. От вас зависи как ще го имплементирате. 
  За него има само едно единствено условие:

  Всеки клас, който използва Kid като свой метаклас, трябва да имплементира метод, с който инстанциите му да са callable. Ако се опитаме да 
  дефинираме клас, чиито инстанции не могат да се извикват, очакваме да се възбуди NotImplementedError с произволен текст, който можете да 
  използвате, за да ни покажете колко ни обичате/мразите.

  class BulgarianKid(metaclass=Kid):
      pass

  Това ще хвърли NotImplementedError
