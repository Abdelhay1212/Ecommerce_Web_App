window.paypal
            .Buttons({
                async createOrder() {

                    const country = document.getElementById('country').value;
                    const city = document.getElementById('city').value;
                    const street = document.getElementById('street').value;
                    const home = document.getElementById('home').value;

                    try {
                        const response = await fetch("/api/orders", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                cart: {
                                        country: country,
                                        city: city,
                                        street: street,
                                        home: home
                                    },
                            }),
                        });
                
                        const orderData = await response.json();
                
                        if (response.ok) {
                            return orderData.id;
                        } else {
                            const errorDetail = orderData?.error;
                            const errorMessage = errorDetail
                                ? `${errorDetail}`
                                : JSON.stringify(orderData);
                
                            throw new Error(errorMessage);
                        }
                    } catch (error) {
                        console.error(error);
                        resultMessage(`Could not initiate PayPal Checkout...<br><br>${error}`);
                    }
                },
                async onApprove(data, actions) {
                    try {
                        const response = await fetch(`/api/orders/${data.orderID}/capture`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                        });
                        
                        const orderData = await response.json();
                        // Three cases to handle:
                        //   (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
                        //   (2) Other non-recoverable errors -> Show a failure message
                        //   (3) Successful transaction -> Show confirmation or thank you message
                        
                        const errorDetail = orderData?.details?.[0];
                        
                        if (errorDetail?.issue === "INSTRUMENT_DECLINED") {
                            // (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
                            // recoverable state, per https://developer.paypal.com/docs/checkout/standard/customize/handle-funding-failures/
                            return actions.restart();
                        } else if (errorDetail) {
                            // (2) Other non-recoverable errors -> Show a failure message
                            throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
                        } else if (!orderData.purchase_units) {
                            throw new Error(JSON.stringify(orderData));
                        } else {
                            // (3) Successful transaction -> Show confirmation or thank you message
                            // Or go to another URL:  actions.redirect('thank_you.html');
                            thankYou();
                        }
                    } catch (error) {
                        console.error(error);
                        transactionFailed();
                    }
                    },
                })
                .render("#paypal-button-container");


function resultMessage(message) {
    const container = document.querySelector("#result-message");
    container.innerHTML = message;
}


function thankYou() {
    const thank_you_container = document.getElementById('thankYou');
    const overlay = document.getElementById('overlay');

    thank_you_container.classList.remove('hide');
    overlay.classList.remove('hide');
}

function transactionFailed() {
    const failed_container = document.getElementById('transactionFailed');
    const overlay = document.getElementById('overlay_failed');

    failed_container.classList.remove('hide');
    overlay.classList.remove('hide');
}
