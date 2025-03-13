import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/Signin.vue';
import Register from '../components/Register.vue';
import EnergyDashboard from '../components/Dashboard.vue';
import RoomPage from '../components/Room.vue';
import NotificationPage from '../components/Notification.vue';
import ReportPage from '../components/Report.vue';

const routes = [
  { path: '/login',
     name: 'SignIn',
    component: SignIn 
  },
  { path: '/',
    name: 'Register', 
    component: Register 
  },
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: EnergyDashboard,
    meta: { requiresAuth: true }
  },
  { 
    path: "/room/:room", 
    component: RoomPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/notification", 
    component: NotificationPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/report", 
    component: ReportPage,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

//ตรวจtokenก่อนloadหน้าอื่นๆ
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  if (to.meta.requiresAuth && !token) {
    console.log("ผู้ใช้ยังไม่ได้เข้าสู่ระบบ")
    next('/login');
  } else {
    next();
  }
});

export default router;