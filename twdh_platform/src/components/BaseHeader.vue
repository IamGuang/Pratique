<template>
  <header class="header header--bg">
    <div class="container">
      <div class="navbar">
        <div class="navbar__row">
          <div
            class="navbar__items"          
          >
            <ul class="navbar__ul">
              <li class="navbar__item">
                <router-link
                  :to="{ name: 'Home' }"
                  class="navbar__link navbar__link--is-active"
                  >首頁</router-link
                >
              </li>
              <li class="navbar__item">
                <router-link :to="{ name: 'About' }" class="navbar__link"
                  >平台介紹</router-link
                >
              </li> 
               <li class="navbar__item">
                <router-link :to="{ name: 'System' }" class="navbar__link"
                  >臺灣史料脈絡分析系統</router-link
                >
              </li>
              <li class="navbar__item">
                <router-link :to="{ name: 'OpendataIndex' }" class="navbar__link"
                  >Open Data</router-link
                >
              </li>   
              <li class="navbar__item">
                <router-link :to="{ name: 'TdocuSkyIndex' }" class="navbar__link"
                  >T-DocuSky</router-link
                >
              </li>  
              <li class="navbar__item">
                <router-link :to="{ name: 'RelatedLink' }" class="navbar__link"
                  >相關連結</router-link
                >
              </li>      
            </ul>
          </div>

          <div>
            <div class="showUser">{{ showLoginUser }}</div>
          </div>

          <div class="header__account">
            <span
              class="header__account-icon"
              @click="showDropDownAccount"
            ></span>
            <div
              class="header__dropdown header__dropdown--w200"
              :class="{ 'header__dropdown--is-active': isAccountDropDown }"
            >
              <div class="header__dropdown-content" v-if="this.$store.state.user.userName">
                <div class="header__account-link" v-on:click="handleLogout">登 出</div>        
              </div>
              <div class="header__dropdown-content" v-else="this.$store.state.user.userName">
                <router-link
                  :to="{ name: 'Login' }"
                  class="header__account-link"
                  @click="showDropDownAccount"
                  >登 入</router-link
                >         
              </div>
            </div>
          </div>
         
        </div>    
      </div>
    </div>
  </header>
</template>

<script>
import VueSimpleAlert from "vue3-simple-alert";
import VueCookies from 'vue-cookies';
import axios from 'axios';


export default {
  name: 'BaseHeader',
  
  data: () => ({
    isAccountDropDown: false,
  }),

  computed: {
    showLoginUser() {
      return  this.$store.state.user.userName;
    },
  },

  methods: {
    showDropDownAccount() {
      this.isAccountDropDown = !this.isAccountDropDown
    },
    handleLogout() {
      this.showDropDownAccount();
      
      VueSimpleAlert.confirm("請問您確定要登出嗎？").then(() => {
        let formData = new FormData();
        formData.append("DocuSky_SID", $cookies.get("DocuSky_SID"));
        formData.append("loginName", $cookies.get("username"));

        axios({
          credentials: "include",
          method: "post",
          url: "https://skolem.csie.ntu.edu.tw/DocuSky/webApi/userLogoutJson.php",
          data: formData,
          headers: { "Content-Type": "multipart/form-data" },
        });   
        this.$store.commit('user/clearUserName');
      
        // 清空 Cookie
        $cookies.remove("username");
        $cookies.remove("display_name");
        $cookies.remove("DocuSky_SID");
        
        // 轉址到首頁
        this.$router.push("/");
      });
    },
  },

  mounted() {
  },

  unmounted() {
  }
}
</script>

<style></style>
