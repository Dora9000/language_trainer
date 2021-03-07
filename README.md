# language_trainer

The repository was created in the process of working on a course project

Минимальные требования:
# Таблицы
  Слово: Текст слова
  Предложение: Слова, Порядковые номера слов
  Ошибка: Предложение, Слова, Порядковые номера слов, Сложность задания

# Интерфейс
  Экран «Предложения»: позволяет редактировать список предложений, которые будут использоваться
для генерации контрольных предложений – добавление, удаление, изменение. Напротив каждого
элемента списка отображается количество допущенных ошибок

  Экран «Тренировка»: содержит настройку «Сложность» и кнопку «Начать тренировку». После нажатия
«Начать тренировку» отображаются задание и кнопка «Проверить». Задание – из базы выбирается
предложение, на экране появляется предложение с пропусками и неразмещённые слова. «Сложность»
определяет количество слов, которые нужно разместить. Кнопка «Проверить» проверяет расстановку,
при наличии ошибок создаёт запись «Ошибка» в базе.

  Виджеты «Ячейка» и «Слово»: концепция Dran-n-Drop, «Слово» должно иметь возможность
свободного перемещения по экрану с помощью мыши, «Ячейка» должна иметь возможность привязки 
к себе виджета «Слово» при наведении на него мыши с «захваченным» «Словом». Если курсор мыши
с захваченным «Словом» был отпущен не в области «Ячейки», то «Слово» автоматически обратно
перемещается в последнюю «Ячейку», в которой находилось.

# Рекомендации к усложнению
  Добавить возможность проведения тренировки по записям ошибок – по тем же предложениям и на
той же сложности. Реализовать сохранение целиком задания, которое было выполнено с ошибкой – с
учётом того, какие слова были размещены заранее, а какие не были.