// Terra X - Location System
// المرحلة الأولى: اختبار الحصول على موقع المستخدم

function getMyLocation() {
    if (!navigator.geolocation) {
        alert("هذا الجهاز أو المتصفح لا يدعم تحديد الموقع.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("Terra X Location:");
            console.log("Latitude:", latitude);
            console.log("Longitude:", longitude);

            alert(
                "تم الحصول على موقعك بنجاح 📍\n\n" +
                "Latitude: " + latitude + "\n" +
                "Longitude: " + longitude
            );
        },

        function (error) {
            console.log("Location Error:", error);

            alert(
                "لم نتمكن من الحصول على موقعك.\n" +
                "تأكد من أنك سمحت لـ Terra X باستخدام الموقع."
            );
        }
    );
}
