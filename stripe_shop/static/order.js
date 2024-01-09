document.addEventListener('DOMContentLoaded', function () {
    // Получение публичного ключа Stripe из /config/
    fetch("/config/")
      .then((result) => result.json())
      .then((data) => {
        var stripe = Stripe(data.publicKey);
        var elements = stripe.elements();
  
        var cardElement = elements.create('card', {
          style: {
            base: {
              fontSize: '16px',
              color: '#32325d',
            },
          },
        });
  
        cardElement.mount('#card-element');
  
        var form = document.getElementById('payment-form');
        var cardholderName = document.getElementById('cardholder-name');
        var submitButton = document.getElementById('submit-button');
        var cardErrors = document.getElementById('card-errors');
  
        // Получение orderID из атрибута data-order-id
        var orderID = form.getAttribute('data-order-id');
  
        form.addEventListener('submit', function (event) {
          event.preventDefault();
  
          // Заблокировать кнопку во время обработки
          submitButton.disabled = true;
  
          // Очистить предыдущие ошибки
          cardErrors.textContent = '';
  
          stripe.createPaymentMethod({
            type: 'card',
            card: cardElement,
            billing_details: {
              name: cardholderName.value,
            },
          }).then(function (result) {
            if (result.error) {
              // Ошибка при вводе данных карты
              cardErrors.textContent = result.error.message;
              // Разблокировать кнопку после ошибки
              submitButton.disabled = false;
            } else {
              // Создание PaymentIntent на сервере
              fetch('/create_order_session/' + orderID + '/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  payment_method: result.paymentMethod.id,
                }),
              })
              .then(function (response) {
                return response.json();
              })
              .then(function (session) {
                // Подтверждение оплаты
                console.log(session.clientSecret);
                return stripe.confirmCardPayment(session.clientSecret, {
                  payment_method: result.paymentMethod.id,
                });

              })
              .then(function (confirmResult) {
                if (confirmResult.error) {
                    // Ошибка при подтверждении оплаты
                    cardErrors.textContent = confirmResult.error.message;
                    // Разблокировать кнопку после ошибки
                    submitButton.disabled = false;
                } else {
                    // Оплата успешна
                    console.log(confirmResult.paymentIntent);
            
                    // Перенаправление на страницу "success"
                    window.location.href = '/success/';
                }
            });
            }
          });
        });
      });
  });
  