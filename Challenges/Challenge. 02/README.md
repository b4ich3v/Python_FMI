  Напишете клас HauntedMansion, който има малко по… Хелоуински достъп до атрибутите си:

* Инициализация
  HauntedMansion се инициализира с произволен набор от именувани аргументи:

  haunted_mansion = HauntedMansion(butler="Alfred", rooms=10, basement=True)
  Всеки от тези именувани аргументи следва да бъде достъпен в последствие като аргумент, т.е.:

  print(haunted_mansion.butler)
  Би ни върнало "Alfred"...
  Ако не беше следващата част от условието
  
* Достъп до атрибутите
  Искаме достъпът до атрибутите да работи по следния начин:
  Всеки от наличните атрибути ще може да се достъпва само ако е prefix-нат от spooky_. С други думи ще имаме spooky_butler, spooky_rooms и 
  прочие. Атрибутите няма да бъдат достъпни чрез стандартните си имена! При опит за достъп, вместо това ще получаваме като резултат (не принт, 
  резултат) низът "Booooo, only ghosts here!". Динамично добавените атрибути трябва да работят по същия начин.
  Това не важи за дъндър атрибути, с други думи достъпът до __dict__, __class__, например следва да работи нормално.
  Няма да тестваме с private атрибути (горното все пак важи), но може да тестваме с protected такива.
  haunted_mansion = HauntedMansion(butler="Alfred", rooms=10, basement=True)

  print(haunted_mansion.butler)
  Booooo, only ghosts here!
  
  print(haunted_mansion.spooky_butler)
  Alfred

  haunted_mansion.friendly_ghost = "Your favourite HP ghost - Nearly Headless Nick"
  print(haunted_mansion.friendly_ghost)
  Booooo, only ghosts here!

  print(haunted_mansion.spooky_friendly_ghost)
  Your favourite HP ghost - Nearly Headless Nick

  print(haunted_mansion.__class__)
  <class '__main__.HauntedMansion'>
