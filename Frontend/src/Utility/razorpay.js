import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL;
// onst BASE_URL = import.meta.env.VITE_API_URL;
console.log("API Base URL:", BASE_URL);
const csrfToken = window.csrfToken;
const keyId = import.meta.env.VITE_RAZORPAY_KEY_ID;

function pay(plan, refreshSubscription) {
    const userEmail = localStorage.getItem("userEmail");
    const token = localStorage.getItem("token");

    if (!userEmail) {
        alert("Please log in to proceed.");
        return;
    }

    const authConfig = {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        withCredentials: !token
    };

    // Handle Free Plan
    if (plan === "free") {
        axios.post(`${BASE_URL}/api/update-plan/`, {
            plan: 'free',
            email: userEmail
        }, authConfig)
        .then(res => {
            if (res.data.success) {
                if (typeof refreshSubscription === "function") refreshSubscription();
                alert("Free plan activated!");
                window.location.href = "/inputMain";
            } else {
                alert("Failed to activate free plan.");
            }
        })
        .catch(err => {
            console.error("Update plan error:", err.response?.data || err.message);
            alert("Server error during free plan activation.");
        });
        return;
    }

    // Handle Paid Plan
    axios.post(`${BASE_URL}/create_order/`, new URLSearchParams({ amount: plan }), {
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        withCredentials: true
    })
    .then(res => {
        const data = res.data;
        if (!data || !data.id) throw new Error("Order creation failed.");

        const options = {
            key: keyId,
            amount: data.amount,
            currency: "INR",
            order_id: data.id,
            handler: function (response) {
                axios.post(`${BASE_URL}/api/verify-payment/`, response, authConfig)
                .then(() => {
                    let planName = "basic";
                    const amt = parseInt(plan);
                    if (amt === 899) planName = "premiumelite";
                    else if (amt === 1299) planName = "premium";

                    return axios.post(`${BASE_URL}/api/update-plan/`, {
                        plan: planName,
                        email: userEmail
                    }, authConfig);
                })
                .then(result => {
                    if (result.data.success) {
                        if (typeof refreshSubscription === "function") refreshSubscription();

                        axios.get(`${BASE_URL}/auth/api/get-subscription/`, authConfig)
                            .then(response => {
                                const { tier, submissions_remaining } = response.data;
                                localStorage.setItem("userPlan", tier);
                                localStorage.setItem("submissionCount", submissions_remaining);
                                alert("Plan activated!");
                                window.location.href = "/inputMain";
                            })
                            .catch(fetchErr => {
                                console.error("Subscription fetch failed:", fetchErr);
                                alert("Plan activated, but unable to refresh submission info.");
                                window.location.href = "/inputMain";
                            });
                    } else {
                        alert("Plan activation failed.");
                    }
                })
                .catch(err => {
                    console.error("Update plan error:", err.response?.data || err.message);
                    alert("Error updating plan: " + (err.response?.data?.error || "unknown"));
                });
            },
            prefill: { email: userEmail },
            theme: { color: "#3399cc" }
        };

        const razor = new window.Razorpay(options);
        razor.open();
    })
    .catch(err => {
        console.error("Payment initiation failed:", err);
        alert("Payment initiation failed.");
    });
}

export default pay;
