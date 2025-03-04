import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/Signin.vue';
import Register from '../components/Register.vue';
import EnergyDashboard from '../components/Dashboard.vue';
import RoomPage from '../components/Room.vue';
import NotificationPage from '../components/Notification.vue';
import ReportPage from '../components/Report.vue';

const routes = [
  { path: '/login', name: 'SignIn', component: SignIn },
  { path: '/', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: EnergyDashboard },
  { path: "/room/:room", component: RoomPage },
  { path: "/notification", component: NotificationPage },
  { path: "/report", component: ReportPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
