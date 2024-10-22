*  Напишете декоратор type_check, който да може да се използва по следния начин:

   @type_check("in")(int, float, complex)
   def power(num, power):
       return num ** power

   @type_check("in")(str)
   @type_check("out")(str)
   def concatenate(*strings, separator=' beep boop '):
       return separator.join(strings)
       
   При валидни типове, както в горните два примера - очакваме функцията да се изпълни безпроблемно, връщайки коректния резултат. При невалидни…

*  type_check("in")
   При извикване на функция, декорирана с type_check("in")(<типове>), следва да бъдат проверени типовете на всички аргументи. Ако някой от тях не е сред изброените такива, 
   функцията трябва да принтира следния стринг:

*  "Invalid input arguments, expected <типове>!"
   Където вместо <типове> имате стринговите репрезентаци на типовете, изброени при декорирането на функцията, съединени с ", " (запетая и интервал). Например "Invalid input 
   arguments, expected <class 'dict'>, <class 'set'>!".
   Стрингът се принтира само веднъж за дадено извикване на декорираната функция, независимо от броят аргументи, които не отговарят на условието за тип.

*  type_check("out")
   При извикване на функция, декорирана с type_check("out")(<типове>), следва да бъде проверен резултатът от изпълнението ѝ. Ако той не е сред изброените такива, функцията 
   трябва да принтира следния стринг:

*  "Invalid output value, expected <типове>!"
   Съдържанието на <типове> е същото като по-горе, но за "out" типовете.

   Резултат от изпълнението
   Дори и двете условия да са нарушени (или пък само едното), все пак искаме функцията да се изпълни - независимо дали това е да се "счупи" или да върне коректен резултат. 
   Очевидно, ако функцията се счупи по средата на изпълнението си - няма как тя да върне резултат, така че ще принтираме само информация за входните аргументи.

  Уговорки:

*  Принтирането става с print. Не ползвайте нищо езотерично, просто функцията print.
  
*  Стрингова репрезентация на типовете, за консистентност и простота ще рече резултатът от str извикан върху конкретния тип, напр. str(dict) -> "<class 'dict'>".
  
*  Спазвайте шаблонът на съобщението, упоменат по-горе, колкото и да ви се иска да принтирате нещо по-готино. Готиното можете да го сложите в коментар.
  
*  Трите уговорки са доста важни, иначе има немалък шанс да ви фейлнат тестовете.
  
*  Резултат от изпълнението на функция е само един обект. Дори когато тя връща "множество" стойности (return a, b, c) - функцията отново връща само един обект и той е tuple. *
  
*  Проверката за тип се извършва само върху този обект.
  
*  Този път задължително не оставяйте хвърчащи print-ове из решението си, тъй като могат да афектират резултата от тестовете.
  
*  Ако бяхме една идея по-напред с материала - щяхме да предложим по-шукаритетен вариант да менажираме съобщенията, но за момента ще трябва да се задоволим с print.