* Tone
  Напишете клас Tone, който да описва понятието за музикален тон. Искаме да може да се инстанцира по следния начин:
  
  c_sharp = Tone("C#") # At least not Java
  Искаме да имаме стрингова репрезентация на тоновете, работеща по следния начин:
  
  print(str(c_sharp))
  # "C#"
  Уговорка: Както споменахме по-горе - за целите на домашното няма да се занимаваме с октавите на дадените тонове, приемаме, че всички тонове 
  C са едно и също.

* Interval
  Напишете клас Interval, който да описва понятието за интервал. Искаме да може да се инстанцира по следния начин:

  number_of_semitones = 3 # Където 3 е брой полутонове разстояние или "стъпки" според горните обяснения
  minor_third = Interval(number_of_semitones)
  Искаме да имаме стрингова репрезентация на интервалите, работеща по следния начин:

  print(str(minor_third))
  # "minor 3rd"
  # С малки букви
  Уговорка: Интервалите могат да приемат произволни естествени числа, като Interval(13) е същото като Interval(1) и неговата репрезентация би 
  била minor 2nd. С други думи отново се абстрахираме от октавите.

* Chord
  Напишете клас Chord, който да описва понятието за акорд. Искаме да може да се инстанцира по следния начин:

  c, d_sharp, g = Tone("C"), Tone("D#"), Tone("G")
  c_minor_chord = Chord(c, d_sharp, g)
  Имаме следните уговорки:

  Първият параметър при инстанциране винаги е основния тон (позиционен).
  Останалите тонове са произволен брой и с произволна подредба. За подредбата повече информация малко по-надолу.
  Повторенията на тоновете не се отразяват. С други думи дори да имате 10 пъти C - пази се единствено информация за тона C (важно за долната 
  подточка). Приемаме опит за създаване на акорд от 1 тон за недефинирано поведение и искаме да се възбуди TypeError с текст "Cannot have a 
  chord made of only 1 unique tone".
  Още един пример:

  c, another_c = Tone("C"), Tone("C")
  sissy_chord = Chord(c, another_c)
  Traceback (most recent call last):
  File ...
    ...
  TypeError: Cannot have a chord made of only 1 unique tone
  Искаме да имаме стрингова репрезентация на акордите, работеща по следния начин:

  print(str(c_minor_chord))
  # "C-D#-G"
  # Описание на всички съдържащи се тонове, започващи от "root"-а,
  # подредени по редът си в хроматичната скала (C, C#, D, D#... B), разделени от тире
  # Както казахме по-горе - повторения няма

  c, another_c, f = Tone("C"), Tone("C"), Tone("F")
  csus4_chord = Chord(c, f, another_c) # Спокойно, не е важно какъв точно е този акорд
  print(str(csus4_chord))
  # "C-F"

  f, c, d, a, g = Tone("F"), Tone("C"), Tone("D"), Tone("A"), Tone("G")
  f_sixth_ninth_chord = Chord(f, c, d, a, g)
  print(str(f_sixth_ninth_chord))
  # "F-G-A-C-D"
  # Root-ът е водещ, оттам насетне всички са подредени спрямо редът си в скалата
  # релативно спрямо основния тон
  За да не навлизаме в дълбините на "качествата" на акордите, ще се ограничим до следните 3 качества - "минорен", "мажорен" и "power" (ако 
  някой знае как е на български - да каже) акорди, определени от следните методи:

* Chord.is_minor
  Ако акордът има в себе си тон, който заедно с основният (root) образува "minor 3rd" - той е минорен и функцията трябва да ни върне True. В 
  противен случай - False:

  c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
  print(c_minor_chord.is_minor())
  # True
  # Тонът D# и root-ът C са на разстояние един от друг, образуващо интервал "minor 3rd"

  c_not_minor_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
  print(c_not_minor_chord.is_minor())
  # False
  # Няма тон, който заедно с root-а да образува "minor 3rd", така че приемаме, че акордът не е минорен
  
* Chord.is_major
  Ако акордът има в себе си тон, който заедно с основният (root) образува "major 3rd" - той е мажорен и функцията трябва да ни върне True. В 
  противен случай - False:

  c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
  print(c_major_chord.is_major())
  # True
  # Тонът E и root-ът C са на разстояние един от друг, образуващо интервал "major 3rd"

  c_not_major_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
  print(c_not_major_chord.is_major())
  # False
  # Няма тон, който заедно с root-а да образува "major 3rd", така че приемаме, че акордът не е мажорен
  
* Chord.is_power_chord
  Ако акордът няма в себе си тон, който заедно с основният (root) образува "minor 3rd", нито пък "major 3rd" - той е power акорд и функцията 
  трябва да ни върне True. В противен случай - False:

  c_power_chord = Chord(Tone("C"), Tone("F"), Tone("G"))
  print(c_power_chord.is_power_chord())
  # True
  # Нямаме нито "minor 3rd", нито "major 3rd" интервал спрямо основния тон

  # И преди някой, който е бил в дебрите на музикалната теория да ни направи забележка,
  # че въпросният акорд всъщност не е power chord, а суспендиран (или там както се води
  # на български) - искате ли да ви караме да отбелязвате и суспендираните акорди? :D

* c_not_power_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
  print(c_not_power_chord.is_power_chord())
  # False
  # Тонът E и root-ът C са на разстояние един от друг, образуващо интервал "major 3rd", следователно нямаме power chord
  
* Операции
  Искаме да имаме възможност да извършваме следните операции с обектите от горните класове:

* Събиране на тонове
  Искаме да можем да събираме обекти от клас Tone и резултат от операцията да бъде обект от клас Chord:

  c, g = Tone("C"), Tone("G")
  result_chord = c + g # result_chord е обект от тип Chord
  print(result_chord)
  # "C-G"
  
* Изваждане на тонове
  Искаме да можем да изваждаме обекти от клас Tone и резултат от операцията да бъде обект от клас Interval:

  c, g = Tone("C"), Tone("G")
  result_interval = g - c # result_interval е обект от тип Interval
  print(result_interval)
  # "perfect 5th"
  
* Събиране на тон с интервал
  Искаме да можем да събираме тонове с интервали и резултат от операцията да бъде нов тон с променена височина:

  c = Tone("C")
  perfect_fifth = Interval(7)
  result_tone = c + perfect_fifth
  print(result_tone)
  # "G"

  c = Tone("C")
  result_tone = c + Interval(12)
  print(result_tone)
  # "C"
  # Тук забелязваме "цикличността" на 12-те тона - тонът е отново C, тъй като не се
  # ангажираме с концепцията за октави

  g = Tone("G")
  perfect_fifth = Interval(7)
  result_tone = g + perfect_fifth
  print(result_tone)
  # "D"
  Забележка: Искаме това да работи само когато тонът е отляво. Когато тонът е отдясно, го приемаме за недефинирано поведение и искаме да се 
  възбуди TypeError с текст "Invalid operation". Семпло, но няма да ви вгорчаваме живота… Повече.

* Изваждане на интервал от тон
  Искаме да можем да изваждаме интервал от тон и резултат от операцията да бъде нов тон с променена височина, но този път в обратна посока, 
  т.е. "надолу":

  c = Tone("C")
  perfect_fifth = Interval(7)
  result_tone = c - perfect_fifth
  print(result_tone)
  # "F"
  # Тук отново забелязваме "цикличността" на 12-те тона
  Забележка: Искаме това да работи само когато тонът е отляво. Когато тонът е отдясно, го приемаме за недефинирано поведение и искаме да се 
  възбуди TypeError с текст "Invalid operation". Ако искате може и друг… Просто ще ви фейлнат тестовете.

* Събиране на интервали
  Искаме да можем да събираме обекти от клас Interval и резултат от операцията да бъде нов обект от клас Interval:

  perfect_fifth = Interval(7)
  minor_third = Interval(3)
  result_interval = perfect_fifth + minor_third
  print(result_interval)
  # "minor 7th"
  
* Събиране на акорд с тон
  Искаме да можем да събираме акорди с тонове и резултат от операцията да бъде нов акорд:

  c5_chord = Chord(Tone("C"), Tone("G"))
  result_chord = c5_chord + Tone("E")
  print(result_chord)
  # C-Е-G
  
* Изваждане на тон от акорд
  Искаме да можем да изваждаме тон от акорд. Ако акордът съдържа три или повече, тона ще се върне нов акорд, в противен случай ще го 
  третираме като недефинирано поведение и искаме да се възбуди TypeError с текст "Cannot have a chord made of only 1 unique tone".

  c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
  result_chord = c_major_chord - Tone("E")
  print(result_chord)
  # C-G

  c_power_chord = Chord(Tone("C"), Tone("G"))
  result_chord = c_power_chord - Tone("G")
  Traceback (most recent call last):
  File ...
    ...
  TypeError: Cannot have a chord made of only 1 unique tone
  Изваждането на несъществуващ тон също е недефинирано поведение, отново искаме TypeError, но този път искаме текстът да бъде "Cannot remove 
  tone <Tone> from chord <Chord>", където <Tone> и <Chord> са съотвените стрингови репрезентации на тона и акорда:

  c_power_chord = Chord(Tone("C"), Tone("G"))
  result_chord = c_power_chord - Tone("E")
  Traceback (most recent call last):
  File ...
    ...
  TypeError: Cannot remove tone C from chord C-G
  
* Събиране на акорди
  Искаме да можем да събираме обекти от клас Chord и резултат от операцията да бъде нов обект от клас Chord:

  c5_chord = Chord(Tone("C"), Tone("G"))
  this_other_chord = Chord(Tone("A"), Tone("B"))
  result_chord = c5_chord + this_other_chord
  print(result_chord)
  # "C-G-A-B"
  И финално
  
* Chord.transposed
  Умишлено оставихме този метод за накрая, тъй като горните операции описват поведението на тоновете когато ги "изместваме" нагоре или 
  надолу, което е важно за финалната ни функция.

  Последен термин, обещавам… Искаме да можем да "транспонираме" даден акорд, т.е. да изместим всеки един от тоновете му с един и същ 
  интервал. Интервалът в нашият случай ще бъде обект от тип Interval, а промяната на тоновете следва да може да се случва както нагоре, така 
  и надолу, определено от знака пред интервала. Тъй като методът е transposed - искаме като резултат да ни връща нов обект от тип Chord.

  Ето и пример:

  print(str(c_minor_chord))
  # "C-D#-G"
  d_minor_chord = c_minor_chord.transposed(Interval(2))
  print(str(d_minor_chord))
  # "D-F-A"

  a_sharp_minor_chord = d_minor_chord.transposed(-Interval(4))
  print(str(a_sharp_minor_chord))
  # "A#-C#-F"
