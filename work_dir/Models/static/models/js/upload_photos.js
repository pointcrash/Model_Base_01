// Получаем поле выбора файлов
var input = document.querySelector('input[type="file"]');

// Обрабатываем изменение в поле выбора файлов
input.addEventListener('change', function(event) {
  // Получаем выбранные файлы
  var files = event.target.files;

  // Очищаем предыдущее содержимое предпросмотра
  document.querySelector('#preview').innerHTML = '';

  // Отображаем выбранные файлы на странице
  for (var i = 0; i < files.length; i++) {
    var file = files[i];

    // Проверяем, что выбранный файл - изображение
    if (!file.type.match('image.*')) {
      continue;
    }

    var reader = new FileReader();

    // Создаем элемент img для отображения изображения
    var img = document.createElement('img');
    img.file = file;
    img.style.maxWidth = '200px';
    img.style.maxHeight = '200px';
    img.style.marginRight = '10px'; // добавляем отступ между изображениями
    img.style.borderRadius = '5px'; // скругляем углы изображений
    document.querySelector('#preview').appendChild(img);

    // Читаем выбранный файл и отображаем его на странице
    reader.onload = (function(aImg) {
      return function(e) {
        aImg.src = e.target.result;
      };
    })(img);

    reader.readAsDataURL(file);
  }
});
