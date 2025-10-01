<template>
  <div class="page-container">
    <header class="header">
      <!-- You can link back to your login page or home page here -->
      <router-link to="/" class="logo-link">
        <img
          src="/path/to/your/wotnot-logo.svg"
          alt="WotNot Logo"
          class="logo-icon"
        />
        <span class="logo-text">WotNot</span>
      </router-link>
    </header>

    <main class="content-wrapper">
      <div class="content-card">
        <h1 id="terms-and-conditions">Terms and Conditions</h1>
        <p class="last-updated">Last updated: May 25, 2025</p>

        <section class="section-content">
          <h2>1. Introduction</h2>
          <p>
            Welcome to WotNot! These Terms and Conditions ("Terms") govern your
            use of the WotNot website and any related services provided by us.
            By accessing or using our Service, you agree to be bound by these
            Terms. If you disagree with any part of the terms, then you may not
            access the Service.
          </p>
        </section>

        <section class="section-content">
          <h2>2. Account Terms</h2>
          <ul>
            <li>You must be at least 18 years old to use this Service.</li>
            <li>
              You are responsible for maintaining the security of your account
              and password.
            </li>
            <li>
              You agree to provide true, accurate, current, and complete
              information when registering for an account.
            </li>
            <li>
              You may not use the Service for any illegal or unauthorized
              purpose.
            </li>
          </ul>
        </section>

        <section class="section-content">
          <h2>3. Intellectual Property</h2>
          <p>
            The Service and its original content, features, and functionality
            are and will remain the exclusive property of WotNot and its
            licensors. Our trademarks and trade dress may not be used in
            connection with any product or service without the prior written
            consent of WotNot.
          </p>
        </section>

        <section class="section-content">
          <h2>4. Termination</h2>
          <p>
            We may terminate or suspend your account immediately, without prior
            notice or liability, for any reason whatsoever, including without
            limitation if you breach the Terms. Upon termination, your right to
            use the Service will immediately cease.
          </p>
        </section>

        <section class="section-content">
          <h2>5. Governing Law</h2>
          <p>
            These Terms shall be governed and construed in accordance with the
            laws of [Your Country/State], without regard to its conflict of law
            provisions.
          </p>
        </section>

        <hr class="section-divider" />

        <h1 id="privacy-policy">Privacy Policy</h1>
        <p class="last-updated">Last updated: May 25, 2025</p>

        <section class="section-content">
          <h2>1. Introduction</h2>
          <p>
            Your privacy is important to us. This Privacy Policy describes how
            WotNot ("we," "us," or "our") collects, uses, and discloses your
            personal information when you use our website (the "Service").
          </p>
        </section>

        <section class="section-content">
          <h2>2. Information We Collect</h2>
          <h3>Personal Information:</h3>
          <p>
            When you register for an account or interact with our Service, we
            may collect personally identifiable information, such as:
          </p>
          <ul>
            <li>Email address</li>
            <li>Name (optional, if collected)</li>
            <li>Password (stored securely, typically as a hash)</li>
          </ul>
          <h3>Usage Data:</h3>
          <p>
            We may also collect information that your browser sends whenever you
            visit our Service ("Usage Data"). This Usage Data may include
            information such as your computer's Internet Protocol address (e.g.,
            IP address), browser type, browser version, the pages of our Service
            that you visit, the time and date of your visit, the time spent on
            those pages, unique device identifiers, and other diagnostic data.
          </p>
        </section>

        <section class="section-content">
          <h2>3. How We Use Your Information</h2>
          <p>WotNot uses the collected data for various purposes:</p>
          <ul>
            <li>To provide and maintain the Service</li>
            <li>To notify you about changes to our Service</li>
            <li>
              To allow you to participate in interactive features of our Service
              when you choose to do so
            </li>
            <li>To provide customer support</li>
            <li>To monitor the usage of the Service</li>
            <li>To detect, prevent, and address technical issues</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>4. Disclosure of Your Information</h2>
          <p>
            We may share your information with trusted third parties who assist
            us in operating our website, conducting our business, or serving our
            users, so long as those parties agree to keep this information
            confidential. We may also release your information when we believe
            release is appropriate to comply with the law, enforce our site
            policies, or protect ours or others' rights, property, or safety.
          </p>
        </section>

        <section class="section-content">
          <h2>5. Your Data Protection Rights</h2>
          <p>
            Depending on your location, you may have the following data
            protection rights:
          </p>
          <ul>
            <li>
              The right to access, update, or delete the information we have on
              you.
            </li>
            <li>The right of rectification.</li>
            <li>The right to object.</li>
            <li>The right of restriction.</li>
            <li>The right to data portability.</li>
            <li>The right to withdraw consent.</li>
          </ul>
          <p>
            To exercise any of these rights, please contact us at [Your Contact
            Email Address].
          </p>
        </section>

        <section class="section-content">
          <h2>6. Changes to This Privacy Policy</h2>
          <p>
            We may update our Privacy Policy from time to time. We will notify
            you of any changes by posting the new Privacy Policy on this page.
            You are advised to review this Privacy Policy periodically for any
            changes.
          </p>
        </section>

        <div class="back-link">
          <!-- Link back to your login page or home page -->
          <router-link to="/" class="button">Back to Login</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "TermsAndPrivacy",
};
</script>

<style scoped>
/* Define your color variables based on the WotNot image */
:root {
  --primary-green: #38a169; /* Based on the login button/logo */
  --dark-text: #2d3748; /* Dark grey for text */
  --light-grey-background: #f7fafc; /* Very subtle off-white background */
  --border-color: #e2e8f0; /* Subtle border for elements */
  --shadow-color: rgba(0, 0, 0, 0.08); /* Slightly more pronounced shadow */
  --light-text-color: #6b7280; /* For less emphasized text like date */
}

.page-container {
  display: flex;
  flex-direction: column;
  /* Crucial change: Set height to 100% or 100vh */
  height: 100vh; /* Use 100vh to ensure it fills the viewport exactly */
  /* OR height: 100%; IF html, body, and #app are also height: 100% */

  background-color: var(--light-grey-background);
  font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
  color: var(--dark-text);
  line-height: 1.7;
  font-size: 16px;
  /* If you don't want the global scrollbar, you can hide overflow here, 
       but ensure your content-wrapper is scrollable. */
  overflow: hidden; /* Hides global scrollbar, forces inner scroll */
}

.header {
  padding: 20px 40px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  flex-shrink: 0; /* Prevents header from shrinking */
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--dark-text);
}

.logo-icon {
  height: 30px;
  width: auto;
  margin-right: 10px;
}

.logo-text {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--primary-green);
}

.content-wrapper {
  flex-grow: 1; /* Takes available vertical space */
  display: flex;
  justify-content: center;
  /* Crucial change: align-items to flex-start allows content to overflow vertically */
  align-items: flex-start; /* Ensures content starts from the top within the flex container */
  padding: 50px 20px;
  overflow-y: auto; /* This makes the content-wrapper scrollable */
  /* Add scrollbar styling for better aesthetics if needed */
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: var(--primary-green) var(--light-grey-background); /* Firefox */
}

/* For Webkit browsers (Chrome, Safari) */
.content-wrapper::-webkit-scrollbar {
  width: 8px;
}

.content-wrapper::-webkit-scrollbar-track {
  background: var(--light-grey-background);
  border-radius: 4px;
}

.content-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--primary-green);
  border-radius: 4px;
  border: 2px solid var(--light-grey-background);
}

.content-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 6px 15px var(--shadow-color);
  border: 1px solid var(--border-color);
  padding: 50px;
  max-width: 850px;
  width: 100%;
  box-sizing: border-box;
  /* No fixed height here, let content dictate height, 
       and content-wrapper's overflow will handle it */
}

h1 {
  font-size: 2.5rem;
  color: var(--primary-green);
  margin-bottom: 25px;
  text-align: center;
  border-bottom: 2px solid var(--primary-green);
  padding-bottom: 20px;
  position: relative;
}

h1::after {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -2px;
  width: 60px;
  height: 4px;
  background-color: var(--primary-green);
  border-radius: 2px;
}

h2 {
  font-size: 2rem;
  color: var(--dark-text);
  margin-top: 45px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

h3 {
  font-size: 1.5rem;
  color: var(--dark-text);
  margin-top: 30px;
  margin-bottom: 15px;
}

p {
  font-size: 1.05rem;
  margin-bottom: 18px;
}

ul {
  list-style-type: disc;
  margin-left: 30px;
  margin-bottom: 20px;
}

li {
  margin-bottom: 10px;
  line-height: 1.7;
}

a {
  color: var(--primary-green);
  text-decoration: none;
  transition: color 0.2s ease-in-out, text-decoration 0.2s ease-in-out;
}

a:hover {
  color: #2f855a;
  text-decoration: underline;
}

.last-updated {
  font-size: 0.95rem;
  color: var(--light-text-color);
  text-align: center;
  margin-bottom: 40px;
}

.section-divider {
  border: none;
  border-top: 2px dashed var(--border-color);
  margin: 60px 0;
  opacity: 0.7;
}

.back-link {
  margin-top: 50px;
  text-align: center;
}

.button {
  display: inline-block;
  padding: 14px 30px;
  background-color: var(--primary-green);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: background-color 0.2s ease-in-out, transform 0.1s ease-out;
}

.button:hover {
  background-color: #2f855a;
  transform: translateY(-2px);
}

.button:active {
  transform: translateY(0);
}

/* Responsive adjustments for smaller screens */
@media (max-width: 768px) {
  .header {
    padding: 15px 20px;
  }

  .logo-text {
    font-size: 1.3rem;
  }

  .content-wrapper {
    padding: 30px 15px;
  }

  .content-card {
    padding: 30px;
    border-radius: 8px;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 20px;
    padding-bottom: 15px;
  }

  h1::after {
    width: 40px;
  }

  h2 {
    font-size: 1.6rem;
    margin-top: 35px;
    margin-bottom: 15px;
  }

  h3 {
    font-size: 1.3rem;
    margin-top: 25px;
    margin-bottom: 10px;
  }

  p,
  ul,
  li {
    font-size: 1rem;
    margin-bottom: 15px;
  }

  .last-updated {
    margin-bottom: 30px;
  }

  .section-divider {
    margin: 40px 0;
  }

  .button {
    padding: 12px 25px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px 15px;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .content-wrapper {
    padding: 20px 10px;
  }

  .content-card {
    padding: 20px;
  }

  h1 {
    font-size: 1.6rem;
  }

  h2 {
    font-size: 1.3rem;
  }

  h3 {
    font-size: 1.1rem;
  }

  p,
  ul,
  li {
    font-size: 0.95rem;
  }
}
</style>
