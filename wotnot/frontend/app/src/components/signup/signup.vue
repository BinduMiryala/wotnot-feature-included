<template>
  <div class="bg-container">
    <div class="max-w-md w-full bg-white p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center text-gray-800 mb-4">Get started with Wotnot</h2>




      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700">Business Name</label>
          <input type="text" id="username" placeholder="Your Business Name"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700">Business Email Address</label>
          <input type="email" id="email" placeholder="Your Business Email Address"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" placeholder="Set Password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="WABAID" class="block text-sm font-medium text-gray-700">WhatsApp Business Account ID</label>
          <input type="text" id="WABAID" placeholder="Your WhatsApp Business Account ID"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="PAccessToken" class="block text-sm font-medium text-gray-700">Permanent Access Token</label>
          <input type="text" id="PAccessToken" placeholder="Your Permanent Access Token"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="Phone_id" class="block text-sm font-medium text-gray-700">Phone Number ID</label>
          <input type="text" id="Phone_id" placeholder="Your Phone Number ID"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>
      </div>

      <div class="mt-4 text-sm text-center">
        <p class="mb-2 text-sm">
          By signing up you agree to the
          <a href="#" class="text-[#075e54] font-semibold">Terms</a> and
          <a href="#" class="text-[#075e54] font-semibold">Privacy Policy</a>
        </p>
      </div>

      <button
        class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        @click.prevent="handleSubmit">
        Get Account
      </button>

      <p class="mt-4 text-center text-sm">
        Already have an account?
        <a href="" class="text-[#075e54] font-semibold mb-4" @click="redirectLogin">Login</a>
      </p>
    </div>
  </div>
</template>



<script>
/* global FB */
import { useToast } from 'vue-toastification';

export default {

  data() {
    return {

      apiUrl: process.env.VUE_APP_API_URL,
      
      sessionInfoResponse: "",
      sdkResponse: "",
    };
  },

  mounted() {
    // Initialize the Facebook SDK
    window.fbAsyncInit = () => {
      FB.init({
        appId: "2621821927998797", // Replace with your App ID
        autoLogAppEvents: true,
        xfbml: true,
        version: "v21.0",
      });
    };

    // Dynamically load the Facebook SDK
    const script = document.createElement("script");
    script.src = "https://connect.facebook.net/en_US/sdk.js";
    script.async = true;
    script.defer = true;
    script.crossOrigin = "anonymous";
    document.body.appendChild(script);

    // Set up an event listener for messages from Facebook
    window.addEventListener("message", (event) => {
      if (
        event.origin !== "https://www.facebook.com" &&
        event.origin !== "https://web.facebook.com"
      ) {
        return;
      }

      try {
        const data = JSON.parse(event.data);
        if (data.type === "WA_EMBEDDED_SIGNUP") {
          if (data.event === "FINISH") {
            const { phone_number_id, waba_id } = data.data;
            console.log(
              "Phone number ID:",
              phone_number_id,
              "WhatsApp business account ID:",
              waba_id
            );
          } else if (data.event === "CANCEL") {
            const { current_step } = data.data;
            console.warn("Cancelled at step:", current_step);
          } else if (data.event === "ERROR") {
            const { error_message } = data.data;
            console.error("Error:", error_message);
          }
        }
        this.sessionInfoResponse = JSON.stringify(data, null, 2);
      } catch {
        console.log("Non-JSON Response:", event.data);
      }
    });
  },
  name: 'SignUpForm',
  methods: {


    fbLoginCallback(response) {
      if (response.authResponse) {
        const code = response.authResponse.code;
        console.log("Auth Response Code:", code);
        // Handle the code by sending it to your backend server for further processing.
      }
      this.sdkResponse = JSON.stringify(response, null, 2);
    },

    launchWhatsAppSignup() {
      FB.login(
        this.fbLoginCallback,
        {
          config_id: "951833230236631", // Replace with your configuration ID
          response_type: "code", // Must be 'code' for System User access token
          override_default_response_type: true,
          extras: {
            setup: {},
            featureType: "",
            sessionInfoVersion: "2",
          },
        }
      );
    },

    loadFacebookSDK() {
      if (!document.getElementById('facebook-jssdk')) {
        const script = document.createElement('script');
        script.id = 'facebook-jssdk';
        script.src = "https://connect.facebook.net/en_US/sdk.js";
        script.async = true;
        script.defer = true;
        script.onload = this.initializeFacebookSDK; // Ensure SDK is initialized once loaded
        document.body.appendChild(script);
      } else {
        this.initializeFacebookSDK(); // SDK is already loaded
      }
    },

    initializeFacebookSDK() {
      window.fbAsyncInit = () => {
        FB.init({
          appId: '2621821927998797',  // Replace with your actual Facebook app ID
          cookie: true,
          xfbml: true,
          version: 'v20.0',
        });
        this.renderFacebookButton();
      };
    },

    loginWithFacebook() {
      // Ensure the FB object is available
      if (window.FB) {
        window.FB.login(response => {
          if (response.authResponse) {
            console.log('User logged in:', response.authResponse);
            this.fetchUserDetails();
          } else {
            console.log('User cancelled login or did not fully authorize.');
          }
        }, { scope: 'email' });
      } else {
        console.error('Facebook SDK not loaded.');
      }
    },

    renderFacebookButton() {
      // Render the button manually after the SDK has loaded
      FB.XFBML.parse(document.getElementById('fb-login-btn'));
      console.log("run")
    },

    checkLoginState() {
      FB.getLoginStatus((response) => {
        if (response.status === 'connected') {
          // User is logged in and authenticated
          console.log('User is logged in and authenticated:', response);
          this.getUserInfo(); // Call a method to fetch user info
        } else if (response.status === 'not_authorized') {
          // User is logged into Facebook but has not authenticated your app
          console.log('User is logged into Facebook but not authenticated your app.');
        } else {
          // User is not logged into Facebook
          console.log('User is not logged into Facebook.');
        }
      });
    },
    fetchUserDetails() {
      window.FB.api('/me', { fields: 'id,name,email' }, userDetails => {
        console.log('User details:', userDetails);
      });
    },

    handleSubmit() {
      const toast = useToast();
      // Get the form data
      const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        WABAID: document.getElementById('WABAID').value,
        PAccessToken: document.getElementById('PAccessToken').value,
        Phone_id: document.getElementById('Phone_id').value,
      };

      // Check for required fields
      if (!formData.username || !formData.email || !formData.password || !formData.WABAID || !formData.PAccessToken || !formData.Phone_id) {
        
        toast.error('Please fill in all required fields.');
        
        return;
      }

      // Send a request to your FastAPI endpoint
      fetch(`${this.apiUrl}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // console.log(response)
            toast.success('Account created successfully!');
            
            // Clear the form fields
            document.querySelectorAll('input').forEach(input => input.value = '');
          } else if (data.detail) {
             // Show the error message from the API
            toast.error(data.detail);
          } else {
            toast.error('Failed to create account. Please try again.');
            
          }
        })
        .catch(error => console.error(error));
    },
    redirectLogin() {

      this.$router.push('/');
    },


  },
};
</script>


<style scoped>
.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  /* equivalent to min-h-screen */

  background-image: url("@/assets/LoginPage.png");
  background-position: center;
  /* equivalent to bg-gray-100 */
  padding: 0 16px;
  /* equivalent to px-4 */
}

/* Responsive padding for different screen sizes */
@media (min-width: 640px) {

  /* equivalent to sm:px-6 */
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {

  /* equivalent to lg:px-8 */
  .container {
    padding: 0 32px;
  }
}
</style>