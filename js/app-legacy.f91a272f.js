(function(){"use strict";var e={454:function(e,t,r){r(6992),r(8674),r(9601),r(7727);var n=r(144),i=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-app",[r("v-main",[r("router-view")],1),r("v-footer",{attrs:{padless:""}},[r("v-card",{staticClass:"grey darken-2' text-center",attrs:{flat:"",tile:"",width:"100%"}},[r("v-card-text",[r("v-btn",{staticClass:"mx-4",attrs:{href:"https://github.com/arbakker/kook",target:"_blank",icon:""}},[r("v-icon",{attrs:{size:"24px"}},[e._v(" mdi-github ")])],1)],1),r("v-card-text",[e._v(" KOOK - "),r("a",{attrs:{href:"https://github.com/arbakker"}},[e._v("arbakker's")]),e._v(" persoonlijke kookboek ")])],1)],1)],1)},a=[],o={name:"App",components:{},data:function(){return{}}},s=o,c=r(1001),l=r(3453),u=r.n(l),p=r(7524),d=r(680),v=r(3237),m=r(7118),h=r(1966),f=r(6428),b=r(7877),g=(0,c.Z)(s,i,a,!1,null,null,null),Z=g.exports;u()(g,{VApp:p.Z,VBtn:d.Z,VCard:v.Z,VCardText:m.ZB,VFooter:h.Z,VIcon:f.Z,VMain:b.Z});var y=r(858);n.Z.use(y.Z);var k=new y.Z({}),V=r(8345),_=r(3800),x=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",[r("v-card",{staticClass:"mx-auto",attrs:{"max-width":"700"}},[r("v-card-title",[e._v(e._s(e.recipe.title))]),r("v-card-subtitle",[e._v(e._s(e.recipe.subtitle))]),r("v-subheader",{staticClass:"text-uppercase"},[e._v("Beschrijving")]),r("v-card-text",[e._v(e._s(e.recipe.description))]),r("v-subheader",{staticClass:"text-uppercase"},[e._v("Ingrediënten")]),r("v-card-actions",[r("v-btn",{directives:[{name:"clipboard",rawName:"v-clipboard",value:e.ingredients,expression:"ingredients"}],attrs:{small:"",title:"Kopieer ingrediënten naar klembord"}},[r("v-icon",{attrs:{small:""}},[e._v("mdi-clipboard-check-multiple")])],1)],1),r("v-list",{attrs:{dense:""}},[r("v-list-item-group",e._l(e.recipe.ingredients,(function(t,n){return r("v-list-item",{key:n},[r("v-list-item-content",[r("v-list-item-title",{domProps:{textContent:e._s(t)}})],1)],1)})),1)],1),r("v-subheader",{staticClass:"text-uppercase"},[e._v("Bereiding")]),r("v-expansion-panels",{attrs:{multiple:""}},e._l(e.recipe.steps,(function(t,n){return r("v-expansion-panel",{key:n},[r("v-expansion-panel-header",{staticClass:"font-weight-bold"},[e._v(e._s(t.title))]),r("v-expansion-panel-content",[e._v(" "+e._s(t.description)+" ")])],1)})),1),r("v-card-actions",[r("v-btn",{attrs:{href:"https://github.com/arbakker/kook/edit/main/webapp/public/recipes/"+this.recipeSlug+".json",target:"_blank",small:"",title:"Bewerk dit recept op Github"}},[r("v-icon",{attrs:{small:""}},[e._v("mdi-pencil")])],1)],1)],1),r("v-btn",{staticStyle:{top:"2em"},attrs:{color:"blue",fab:"",absolute:"",medium:"",dark:"",top:"",right:"",to:{name:"home"}}},[r("v-icon",[e._v("mdi-home")])],1)],1)},w=[],C=(r(1539),r(9600),r(1249),{name:"RecipePage",data:function(){return{recipe:{}}},mounted:function(){var e=this,t=this.recipeSlug;fetch("./recipes/".concat(t,".json")).then((function(e){return e.json()})).then((function(t){return e.recipe=t}))},computed:{ingredients:function(){return this.recipe.ingredients.map((function(e){return"- ".concat(e)})).join("\n")},recipeSlug:function(){return this.$route.params.recipeSlug}}}),S=C,O=r(247),L=r(6845),T=r(2443),j=r(1192),B=r(5630),P=r(6816),q=r(7620),I=r(2285),R=r(7874),E=r(5533),M=(0,c.Z)(S,x,w,!1,null,null,null),$=M.exports;u()(M,{VBtn:d.Z,VCard:v.Z,VCardActions:m.h7,VCardSubtitle:m.Qq,VCardText:m.ZB,VCardTitle:m.EB,VContainer:O.Z,VExpansionPanel:L.Z,VExpansionPanelContent:T.Z,VExpansionPanelHeader:j.Z,VExpansionPanels:B.Z,VIcon:f.Z,VList:P.Z,VListItem:q.Z,VListItemContent:I.km,VListItemGroup:R.Z,VListItemTitle:I.V9,VSubheader:E.Z});var A=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",[r("v-row",{staticClass:"text-center"},[r("v-col",[r("v-card",{staticClass:"mx-auto",attrs:{"max-width":"700"}},[r("v-toolbar",{attrs:{color:"blue",dark:""}},[r("v-text-field",{attrs:{label:"Zoek in "+e.nrOfRecipes+" recepten","prepend-icon":"mdi-magnify","hide-detailscyan":"","single-line":""},on:{keydown:e.search},model:{value:e.query,callback:function(t){e.query=t},expression:"query"}})],1),0===e.displayRecipes.length?r("v-subheader",{staticClass:"text-uppercase"},[e._v("Geen resultaten")]):e._e(),e.displayRecipes.length>0?r("v-list",{attrs:{"three-line":""}},[e._l(e.displayRecipes,(function(t,n){return[t.header?r("v-subheader",{key:t.header,domProps:{textContent:e._s(t.header)}}):t.divider?r("v-divider",{key:n,attrs:{inset:t.inset}}):r("v-list-item",{key:t.title,attrs:{to:{name:"recipe",params:{recipeSlug:t.slug}}}},[r("v-list-item-content",[r("v-list-item-title",{domProps:{innerHTML:e._s(t.title)}}),r("v-list-item-subtitle",{domProps:{innerHTML:e._s(t.subtitle)}})],1)],1)]}))],2):e._e()],1)],1)],1)],1)},F=[],K=(r(4916),r(4765),r(2707),JSON.parse('[{"title":"Bami goreng met garnalen","subtitle":"met paksoi en koriander","slug":"bami-goreng-met-garnalen"},{"title":"Vegan kipburger met sriracha-mayo","subtitle":"en geroosterde aardappels","slug":"vegan-kipburger-met-sriracha-mayo"}]')),z=r(4221),D={name:"LandingPage",data:function(){return{recipes:K,displayRecipes:[],query:"",fuse:"fuse"}},mounted:function(){this.init()},computed:{nrOfRecipes:function(){return this.recipes.length}},methods:{search:function(){var e=this;setTimeout((function(){if(""===e.query)console.log("search query empty"),e.displayRecipes=e.recipes;else{console.log("search query not empty");var t=e.fuse.search(e.query,{});console.log(t),e.displayRecipes=t.map((function(e){var t=e.item;return t})).sort(e.compare)}}))},init:function(){this.displayRecipes=this.recipes;var e={shouldSort:!0,threshold:.3,location:0,distance:100,minMatchCharLength:3,ignoreLocation:!0,keys:["title","subtitle"]};this.fuse=new z.Z(this.recipes,e),this.search()}}},G=D,H=r(2102),N=r(1418),J=r(2877),Q=r(896),W=r(7688),U=(0,c.Z)(G,A,F,!1,null,null,null),X=U.exports;u()(U,{VCard:v.Z,VCol:H.Z,VContainer:O.Z,VDivider:N.Z,VList:P.Z,VListItem:q.Z,VListItemContent:I.km,VListItemSubtitle:I.oZ,VListItemTitle:I.V9,VRow:J.Z,VSubheader:E.Z,VTextField:Q.Z,VToolbar:W.Z});var Y=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",[r("v-row",{staticClass:"text-center"},[r("v-col",[r("v-card",{staticClass:"mx-auto",attrs:{"max-width":"700"}},[r("v-card-text",[e._v("Deze applicatie is beveiligd met een wachtwoord")]),r("v-form",{ref:"form",staticStyle:{padding:"0.5em"},attrs:{"lazy-validation":""},on:{submit:function(t){return t.preventDefault(),e.validateBeforeSubmit.apply(null,arguments)}}},[r("v-text-field",{attrs:{type:"password",counter:"",label:"Wachtwoord",required:"",rules:e.rules},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),r("v-btn",{attrs:{color:"primary",type:"submit"},on:{click:e.validateBeforeSubmit}},[e._v(" OK ")])],1)],1)],1)],1)],1)},ee=[],te=(r(5505),r(7714),r(2801),r(1174),{data:function(){var e=this;return{password:null,rules:[function(t){return!!e.matchLogin(t)||"wachtwoord is niet correct"}]}},methods:{matchLogin:function(e){var t="a29va29vaw==",r=atob(t);return e===r},validateBeforeSubmit:function(){this.matchLogin(this.password)&&(localStorage.setItem("user-password",this.password),this.$router.push("home"))}}}),re=te,ne=r(6232),ie=(0,c.Z)(re,Y,ee,!1,null,null,null),ae=ie.exports;u()(ie,{VBtn:d.Z,VCard:v.Z,VCardText:m.ZB,VCol:H.Z,VContainer:O.Z,VForm:ne.Z,VRow:J.Z,VTextField:Q.Z}),n.Z.config.productionTip=!1,n.Z.use(V.Z),n.Z.use(_.Z);var oe=[{path:"/",component:X,name:"home",meta:{requiresAuth:!0}},{path:"/recipe/:recipeSlug",component:$,name:"recipe",meta:{requiresAuth:!0}},{path:"/protected",component:ae,name:"protected"},{path:"*",redirect:"/"}],se=new V.Z({routes:oe});se.beforeEach((function(e,t,r){e.meta.requiresAuth?localStorage.getItem("user-password")?r():r("/protected"):r()})),new n.Z({router:se,vuetify:k,render:function(e){return e(Z)}}).$mount("#app")}},t={};function r(n){var i=t[n];if(void 0!==i)return i.exports;var a=t[n]={exports:{}};return e[n](a,a.exports,r),a.exports}r.m=e,function(){var e=[];r.O=function(t,n,i,a){if(!n){var o=1/0;for(u=0;u<e.length;u++){n=e[u][0],i=e[u][1],a=e[u][2];for(var s=!0,c=0;c<n.length;c++)(!1&a||o>=a)&&Object.keys(r.O).every((function(e){return r.O[e](n[c])}))?n.splice(c--,1):(s=!1,a<o&&(o=a));if(s){e.splice(u--,1);var l=i();void 0!==l&&(t=l)}}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[n,i,a]}}(),function(){r.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return r.d(t,{a:t}),t}}(),function(){r.d=function(e,t){for(var n in t)r.o(t,n)&&!r.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})}}(),function(){r.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){r.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={143:0};r.O.j=function(t){return 0===e[t]};var t=function(t,n){var i,a,o=n[0],s=n[1],c=n[2],l=0;if(o.some((function(t){return 0!==e[t]}))){for(i in s)r.o(s,i)&&(r.m[i]=s[i]);if(c)var u=c(r)}for(t&&t(n);l<o.length;l++)a=o[l],r.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return r.O(u)},n=self["webpackChunkkook_webapp"]=self["webpackChunkkook_webapp"]||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))}();var n=r.O(void 0,[998],(function(){return r(454)}));n=r.O(n)})();