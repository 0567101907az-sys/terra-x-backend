// Terra X - Location System

let locationWatcher = null;

// زر السماح بالموقع
document.getElementById("allowLocation").addEventListener("click", function () {

    if (!navigator.geolocation) {
        document.getElementById("status").textContent =
            "هذا الجهاز لا يدعم تحديد الموقع.";
        return;
    }

    document.getElementById("status").textContent =
        "جاري طلب إذن الموقع... 📍";

    locationWatcher = navigator.geolocation.watchPosition(

        function (position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("Terra X Location:");
            console.log("Latitude:", latitude);
            console.log("Longitude:", longitude);

            document.getElementById("status").textContent =
                "تم تفعيل مشاركة الموقع 📍";
        },

        function (error) {

            console.log("Location Error:", error);

            document.getElementById("status").textContent =
                "لم يتم السماح بالوصول إلى الموقع.";
        },

        {
            enableHighAccuracy: true,
            maximumAge: 5000,
            timeout: 10000
        }
    );
});


// زر إيقاف مشاركة الموقع
document.getElementById("stopLocation").addEventListener("click", function () {

    if (locationWatcher !== null) {
        navigator.geolocation.clearWatch(locationWatcher);
        locationWatcher = null;
    }

    document.getElementById("status").textContent =
        "تم إيقاف مشاركة الموقع 🔴";
});
