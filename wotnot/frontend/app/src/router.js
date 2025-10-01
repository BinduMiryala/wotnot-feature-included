import { createRouter, createWebHistory } from "vue-router";
import BroadCast1 from "./components/broadcast/broadcast1.vue";
import BroadCast2 from "./components/broadcast/broadcast2.vue";
import BroadCast3 from "./components/broadcast/broadcast3.vue";
import ContActs1 from "./components/contacts/contacts1.vue";
import ContActs2 from "./components/contacts/contacts2.vue";
import AppIntegration from "./components/integration/integration.vue";
import LoginPage from "./components/login/login.vue";
import AIagent from "./components/AIagent/AIagent.vue";
import BasicSignupPage from "./components/signup/basic_signup.vue";
import DashboardView from "./views/dashboardview.vue";
import Profile from "./views/profile.vue";
import Settings from "./views/profileSettings.vue";
import ChatbotView from "./components/chatbot/chatbotview.vue"; // Ensure this path is correct
import CostAnalytics from "./components/PurchaseHistory/CostDashboard.vue";
import Analytics from "./components/analytics/Analytics.vue";

import TermsAndPrivacy from "./views/TermsAndPrivacy.vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const routes = [
  // Public routes
  { path: "/", component: LoginPage },
  { path: "/signup", component: BasicSignupPage },

  // { path: '/', component: PublicView },

  {
    path: "/terms-and-privacy",
    component: TermsAndPrivacy,
    name: "TermsAndPrivacy",
  },

  // Protected routes within the dashboard
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
    children: [
      { path: "/agent", component: AIagent, name: "AIagent" },
      {
        path: "/analytics/cost",
        component: CostAnalytics,
        name: "Costanalytics",
      },
      {
        path: "/analytics/conversations",
        component: Analytics,
        name: "DataAnalytics",
      },
      {
        path: "/broadcast/broadcast1",
        component: BroadCast1,
        name: "Broadcast1",
      },
      {
        path: "/broadcast/broadcast2",
        component: BroadCast2,
        name: "Broadcast2",
      },
      {
        path: "/broadcast/broadcast3",
        component: BroadCast3,
        name: "Broadcast3",
      },
      { path: "/contacts/contacts1", component: ContActs1, name: "Contacts1" },
      { path: "/contacts/contacts2", component: ContActs2, name: "Contacts2" },
      {
        path: "/integration/integration1",
        component: AppIntegration,
        name: "Integration1",
      },
      { path: "/profile", component: Profile },
      { path: "/settings", component: Settings },
      { path: "", redirect: "/broadcast/broadcast2" },
      {
        path: "/chatbot/chatbotview",
        component: ChatbotView,
        name: "ChatbotView",
      }, // Updated path
      // Add more routes within the dashboard as needed
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for authentication
// Navigation guard to check for authentication and token expiration
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // No token = not logged in
      
      toast.error("Session expired. Please log in again.");
      return next("/");
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp < now) {
        // Token expired
        localStorage.removeItem("token");
        toast.error("Session expired. Please log in again.");
        return next("/");
      }
    } catch (error) {
      // Invalid token format or parsing error
      localStorage.removeItem("token");
      ("Invalid session. Please log in again.");
      return next("/");
    }
  }

  // If route doesn't require auth or token is valid
  next();
});


export default router;
