document.addEventListener('DOMContentLoaded', function() {
    // 获取存储在 <script> 标签中的 JSON 数据
    const eventDataElement = document.getElementById('eventData');
    const eventData = JSON.parse(eventDataElement.textContent);

    const bookNowBtn = document.getElementById('bookNowBtn');
    const loginModal = document.getElementById('loginModal');
    const confirmEventBookingModal = document.getElementById('confirmEventBookingModal');
    const confirmEventBookingBtn = document.getElementById('confirmEventBookingBtn');
    const cancelEventBookingBtn = document.getElementById('cancelEventBookingBtn');

    // 添加以下代码来处理购买数量的增减
    const decreaseBtn = document.getElementById('decreaseQuantity');
    const increaseBtn = document.getElementById('increaseQuantity');
    const ticketCount = document.getElementById('ticket-count');

    let pendingBookingInfo = null;

    decreaseBtn.addEventListener('click', function() {
        if (parseInt(ticketCount.value) > 1) {
            ticketCount.value = parseInt(ticketCount.value) - 1;
        }
    });

    increaseBtn.addEventListener('click', function() {
        ticketCount.value = parseInt(ticketCount.value) + 1;
    });

    bookNowBtn.addEventListener('click', function() {
        // 每次调用时检查登录状态
        fetch('/check_login')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const ticketCount = document.getElementById('ticket-count').value;
                const totalPrice = (eventData.eventPrice * ticketCount).toFixed(2);
                if (data.is_logged_in) {
                    showConfirmEventBookingModal(ticketCount, totalPrice);
                } else {
                    pendingBookingInfo = { ticketCount, totalPrice };
                    loginModal.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while checking login status: ' + error.message);
            });
    });

    function showConfirmEventBookingModal(ticketCount, totalPrice) {
        const eventDetails = `
            <p><strong>${eventData.translations.event}:</strong> ${eventData.eventTitle}</p>
            <p><strong>${eventData.translations.date}:</strong> ${eventData.eventDate}</p>
            <p><strong>${eventData.translations.location}:</strong> ${eventData.eventLocation}</p>
            <p><strong>${eventData.translations.quantity}:</strong> ${ticketCount}</p>
            <p><strong>${eventData.translations.totalPrice}:</strong> $${totalPrice}</p>
        `;
        
        document.getElementById('eventDetails').innerHTML = eventDetails;
        confirmEventBookingModal.style.display = 'block';
    }

    confirmEventBookingBtn.addEventListener('click', function() {
        const ticketCount = document.getElementById('ticket-count').value;
        fetch('/book_ticket', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event_id: eventData.eventId,
                quantity: ticketCount
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = `/booking_success/${data.booking_id}`;
            } else {
                alert(`${eventData.translations.bookingFailed}: ` + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred during booking');
        });
        confirmEventBookingModal.style.display = 'none';
    });

    cancelEventBookingBtn.addEventListener('click', function() {
        confirmEventBookingModal.style.display = 'none';
    });

    window.onLoginSuccess = function() {
        loginModal.style.display = 'none';
        if (pendingBookingInfo) {
            showConfirmEventBookingModal(pendingBookingInfo.ticketCount, pendingBookingInfo.totalPrice);
            pendingBookingInfo = null;
        }
    };
});