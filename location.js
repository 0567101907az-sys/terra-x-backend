// Terra X - Location System

const BACKEND_URL = "https://terra-x-backend.onrender.com";

let locationWatcher = null;

async function sendLocation(latitude, longitude, accuracy) {

    const accessToken =
        localStorage.getItem("terra_x_access_token");

    if (!accessToken) {
        document.getElementById("status").textContent =
            "يجب تسجيل الدخول إلى Terra X أولاً 🔐";
        return;
    }

    try {

        const response = await fetch(
            `${BACKEND_URL}/api/location`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },

                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude,
                    accuracy: accuracy
                })
            }
        );

        const text = await response.text();

        console.log("Terra X Backend:", response.status, text);

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}: ${text}`
            );
        }

        document.getElementById("status").textContent =
            "تم تحديث موقعك في Terra X 📍";

    } catch (error) {

        console.error("Location API Error:", error);

        document.getElementById("status").textContent =
            "خطأ: " + error.message;
    }
}


document.getElementById("allowLocation").addEventListener(
    "click",
    function () {

        if (!navigator.geolocation) {

            document.getElementById("status").textContent =
                "هذا الجهاز لا يدعم تحديد الموقع.";

            return;
        }

        document.getElementById("status").textContent =
            "جاري طلب إذن الموقع... 📍";

        locationWatcher =
            navigator.geolocation.watchPosition(

                function (position) {

                    const latitude =
                        position.coords.latitude;

                    const longitude =
                        position.coords.longitude;

                    const accuracy =
                        position.coords.accuracy;

                    console.log(
                        "Terra X GPS:",
                        latitude,
                        longitude,
                        accuracy
                    );

                    sendLocation(
                        latitude,
                        longitude,
                        accuracy
                    );
                },

                function (error) {

                    console.error("GPS Error:", error);

                    document.getElementById("status").textContent =
                        "خطأ GPS: " + error.message;
                },

                {
                    enableHighAccuracy: true,
                    maximumAge: 5000,
                    timeout: 10000
                }
            );
    }
);


document.getElementById("stopLocation").addEventListener(
    "click",
    function () {

        if (locationWatcher !== null) {

            navigator.geolocation.clearWatch(
                locationWatcher
            );

            locationWatcher = null;
        }

        document.getElementById("status").textContent =
            "تم إيقاف مشاركة الموقع 🔴";
    }
);
