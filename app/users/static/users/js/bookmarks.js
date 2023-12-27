
  $(document).ready(function () {
    $("form.bookmark-form").submit(function (event) {
      event.preventDefault();

      var form = $(this);
      var url = form.attr("action");

      $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
          // Обновите отображаемые результаты на странице
          $("#bookmark-data").val(data.result);
          $("#bookmark-count").text(data.count); // Обновление количества

          // Обновите текст кнопки
          if (data.result) {
            $("#bookmark-button").text("Удалить из закладок");
          } else {
            $("#bookmark-button").text("Добавить в закладки");
          }
        }
      });
    });
  });
