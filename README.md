### thunder
Инструмант для поиска фотографий гроз в Instagram
Для получений фотографий необходимо ввести долготу и широту. Затем происходит http-запрос к API Instagram, который содержит ключ доступа,
долготу, широту, радиус поиска геолокаций. Дальше вытягиваются фотографии по геолокациям. В описании к фотографиям происходит поиск слов, 
характерищыующих грозу. Если изображение нашлось, то название геолокации, ссылка на изображение и время сохраняются в бд. 