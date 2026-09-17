// Terra X - Login System

const SUPABASE_URL =
    "https://grukcfpwadjcqyzqztvg.supabase.co";

const SUPABASE_ANON_KEY =
    "sb_publishable_1vNcKPD-9OWU8KCedv8LHA_wHqko4Ha";


const emailInput =
    document.getElementById("email");

const passwordInput =
    document.getElementById("password");

const loginButton =
    document.getElementById("loginButton");

const statusText =
    document.getElementById("status");


loginButton.addEventListener(
    "click",
    async function () {

        const email =
            emailInput.value.trim();

        const password =
            passwordInput.value;


        if (!email || !password) {

            statusText.textContent =
                "أدخل البريد الإلكتروني وكلمة المرور.";

            return;
        }


        statusText.textContent =
            "جاري تسجيل الدخول... 🔐";


        try {

            const response = await fetch(
                `${SUPABASE_URL}/auth/v1/token?grant_type=password`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "apikey": SUPABASE_ANON_KEY
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error_description ||
                    data.msg ||
                    data.message ||
                    "فشل تسجيل الدخول"
                );
            }


            if (!data.access_token) {

                throw new Error(
                    "لم يتم الحصول على Access Token"
                );
            }


            // حذف أي جلسة قديمة
            localStorage.removeItem(
                "terra_x_access_token"
            );

            localStorage.removeItem(
                "terra_x_refresh_token"
            );


            // حفظ الجلسة الجديدة
            localStorage.setItem(
                "terra_x_access_token",
                data.access_token
            );


            if (data.refresh_token) {

                localStorage.setItem(
                    "terra_x_refresh_token",
                    data.refresh_token
                );
            }


            console.log(
                "Terra X login successful"
            );


            statusText.textContent =
                "تم تسجيل الدخول بنجاح ✅";


            setTimeout(function () {

                window.location.href =
                    "index.html";

            }, 500);


        } catch (error) {

            console.error(
                "Terra X Login Error:",
                error
            );

            statusText.textContent =
                "فشل تسجيل الدخول: " +
                error.message;
        }

    }
);
