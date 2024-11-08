* Напишете context manager с името ProtectedSection, който да има два опционални параметъра - log и suppress.
  И двата параметъра приемат като стойност tuple от изключения. Искаме ако при изпълнение на кода в блока след 
  отваряне на контекстният мениджър се възбуди грешка, която е в списъка на log - тя да бъде подтисната (не искаме 
  да се прекъсва изпълнението на програмтата) и да бъде записана и да бъде достъпна по следния начин:

  with ProtectedSection(log=(ZeroDivisionError, IndexError)) as err:
      x = 1 / 0

  print(err.exception)
  division by zero
  print(type(err.exception))
  <class 'ZeroDivisionError'>
  Забележете, че обектът зад err.exception е изключение - ZeroDivisionError, а не просто някакъв стринг.

  Ако пък при изпълнение се хвърли грешка, която е в списъка на suppress - тя ще бъде подтисната, но няма да бъде 
  записана:

  with ProtectedSection(suppress=(ZeroDivisionError, IndexError)) as err:
    x = 1 / 0

  print(err.exception)
  None
  Както е видно, в случай, че изключение, което е само "подтиснато", но не и "логнато" - в err.exception ще има 
  None. Същото важи и когато изключение не се е хвърлило.

  И финално, двете могат да съществуват заедно, като приоритет имат грешките описани в log, пред тези в suppress:

  with ProtectedSection(log=(ZeroDivisionError, IndexError), suppress=(TypeError, ZeroDivisionError, Exception)) 
  as err:
      x = 1 / 0

  print(err.exception)
  division by zero
  print(type(err.exception))
  <class 'ZeroDivisionError'>
  
* Уговорки
  Няма да хвърляме изключения, които не са от тип Exception (например KeyboardInterrupt).
  Не се притеснявайте за traceback-а, не ни вълнува за целите на домашното.
  Hint: Не е необходимо да правите нищо специално за да имате поведението str(err.exception) == "division by zero" 
  (или както по-горе е написано - print(err.exception), което всъщност имплицитно вика str), това е поведение по подразбиране на всичко, което наследява от Exception.
