import { useState, useEffect } from 'react';
import { processPayment } from '../../../Models/Requests/dbRequests';

//test AMEX card details: 340000000000009 12/29 1111 12312

const square_application_id = 'sandbox-sq0idb-6Z4GUWHM_8eZ4j3czBcPOw';
const square_location_id = 'L5S30KEFRY41W';

const SquarePaymentForm = () => {
  const [card, setCard] = useState(null);
  //const [message, setMessage] = useState('');

  useEffect(() => {
    async function initializeCard() {
      try {
        //configure a square_payment object that utilizes my square_application
        const payments = window.Square.payments(
          square_application_id,
          square_location_id
        );

        const card = await payments.card();
        await card.attach('#card-container');
        setCard(card);
      } catch (err) {
        console.error('Initializing Card failed', err);
      }
    }
    if (window.Square) {
      initializeCard();
      console.log('Card successfully initialized: ', card);
    } else {
      console.log('Square.js did not load properly');
    }
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const { token, errors } = await card.tokenize();
    //update this code later to be more representative of errors, maybe display some success/failure type of UI on payment success
    if (errors) {
      console.log('Error from Square/PaymentForm.jsx');
      return;
    }

    //token i.e nonce - a unique, one-time-use token that represents payment information securely.
    //basically security measures to mask credit card details being transferred to server
    await processPayment(token, 10000);
  };

  return (
    <>
      <form id="payment-form" onSubmit={handleSubmit}>
        <div id="card-container"></div>
        <button type="submit">Pay</button>
      </form>
    </>
  );
};

export default SquarePaymentForm;
