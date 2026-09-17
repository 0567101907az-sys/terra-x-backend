// Terra X - Login System

const SUPABASE_URL = "https://grukcfpwadjcqyzqztvg.supabase.co";

const SUPABASE_ANON_KEY = "sb_publishable_1vNcKPD-9OWU8KCedv8LHA_wHqko4Ha";


const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("loginButton");
const statusText = document.getElementById("status");


loginButton.addEventListener("click", async function () {

    const email = emailInput.value.trim();
    const password = passwordInput.value;

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


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.error_description ||
                data.msg ||
                "فشل تسجيل الدخول"
            );
        }


        const accessToken = data.access_token;


        localStorage.setItem(
            "terra_x_access_token",
            accessToken
        );


        statusText.textContent =
            "تم تسجيل الدخول بنجاح ✅";


        setTimeout(function () {

            window.location.href =
    "index.html";

        }, 1000);


    } catch (error) {

        console.error(
            "Login Error:",
            error
        );

        statusText.textContent =
            "بيانات الدخول غير صحيحة أو حدث خطأ.";
    }

});
