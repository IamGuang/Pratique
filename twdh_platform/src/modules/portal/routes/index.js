export default [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/system',
    name: 'System',
    component: () => import(/* webpackChunkName: "system" */ '../views/System.vue')
  },
  {
    path: '/relatedlink',
    name: 'RelatedLink',
    component: () => import(/* webpackChunkName: "relatedlink" */ '../views/RelatedLink.vue')
  },
]